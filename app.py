# heroku password 8Tn[+9%hG]^Y$M-
import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib
 
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
import yaml
from db_connection import get_database_connection

st.set_page_config(
    page_title="IIUC Data Science Admission Form",
    page_icon=":book:",
    # layout="wide",
    initial_sidebar_state="expanded",
)
# database localhost connection
# @st.cache()

# def get_database_connection():
#     db = mysql.connect(host = "localhost",
#                       user = "root",
#                       passwd = "root",
#                       database = "mydatabase",
#                       auth_plugin='mysql_native_password')
#     cursor = db.cursor()
#     return cursor, db
 
cursor, db = get_database_connection()
 
# cursor.execute("SHOW DATABASES")
 
# databases = cursor.fetchall() ## it returns a list of all databases present
 
# st.write(databases)
 
# cursor.execute('''CREATE TABLE KOTA (id varchar(255),
#                                               st_name varchar(255),
#                                               mother_name varchar(250),
#                                               father_name varchar(250),
#                                               Gender varchar(50),
#                                               Ph_Num varchar(50),
#                                               Email varchar(50),
#                                               Religion varchar(50),
#                                               BloodG varchar(10),
#                                               Nationality varchar(50),
#                                               Present_Add varchar(300),
#                                               Permmanent_Add varchar(300),
#                                               reg_date date,
#                                               status varchar(255))''')
cursor.execute("Select * from KOTA")
tables = cursor.fetchall()
#st.write(tables)

def admin():
    username=st.sidebar.text_input("Username",key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
 
    if st.session_state.login==True:
        if username=="sajeedreefy" and password=='123korlataki':
            st.sidebar.success('Login Successful')
            st.markdown("<h1 style='text-align:center;color:RoyalBlue;'>IIUC Admin Panel</h1>",unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.markdown("<h3 style='text-align:center;color:Snow;'>Choose the time period for registered applicants</h3>",unsafe_allow_html=True)
            date1=st.date_input('From')
            date2=st.date_input('To')
            cursor.execute(f"select * from KOTA where reg_date between '{date1}' and '{date2}' and status='In Progress'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            st.write("")
            st.write("")
            st.markdown("<h2 style='text-align:center;color:DarkTurquoise;'>List of Students Registered in this time period</h2>",unsafe_allow_html=True)
            st.write("")
            st.write("")
            with st.container():
            	for i in tables:
            		with st.container():
            			col1,col2=st.columns((.5,1))
            			col1.subheader("**Student Name: **")
            			col2.subheader(i[1])
            			col1.subheader("**Phone Number: **")
            			col2.subheader(i[5])
            		Accept=st.button('Accept',key=i[0])
            		Reject=st.button('Reject',key=i[0])
            		if Accept:
            			st.success('Applicant has been Accepted')
            			query=f"Update KOTA set status='Accepted' where id='{i[0]}'"
            			cursor.execute(query)
            			db.commit()
            		elif Reject:
            			st.warning('Applican has been Rejected')
            			cursor.execute(f"Update KOTA set status='Rejected' where id='{i[0]}'")
            			db.commit()
        elif(username=="sajeedreefy" and password!='123korlataki'):
        	st.sidebar.warning('Password is not correct')
        elif(username=="" or password==""):
        	st.sidebar.error("Fill all the requirments")
        else:
        	st.sidebar.warning("Incorrect Username/Password")


def form():
	st.markdown("<h1 style='text-align:center;color:DarkCyan;'>Applicant Registration Form</h1>",unsafe_allow_html=True)
	id=uuid4()
	id=str(id)[:5]
	with st.form(key='member form'):
		sname=st.text_input("Student Name",max_chars=50)
		s1name=st.text_input("Mother's Name",max_chars=50)
		s2name=st.text_input("Father's Name",max_chars=50)
		with st.container():
			col_1,col_2=st.columns((1,1))
			gen_name=col_1.selectbox("Gender",['Choose','Male','Female','Other'])
			Blood_group=col_2.selectbox('Blood Group',['Choose','O+','O-','A+','A-','AB+','AB-','B+','B-'])
		with st.container():
			c1,c2=st.columns((1,1))
			ph_num=c1.text_input('Number',max_chars=11)
			email_n=c2.text_input('Email')
		Rel=st.selectbox('Religion',['Select Option','Islam','Hinduism','Buddhist','Christianity','Others'])
		nation=st.text_input('Nationality')
		Pre_add=st.text_input('Present Address')
		Perm_add=st.text_input('Permanent Address')
		re_date=st.date_input('Registration Date')
		if st.form_submit_button('Submit'):
			query = f'''INSERT INTO KOTA (id,st_name,mother_name,father_name,Gender,Ph_Num,Email,Religion,BloodG,Nationality,
			Present_Add,Permmanent_Add,reg_date,status) VALUES ('{id}','{sname}','{s1name}',
			'{s2name}','{gen_name}','{ph_num}','{email_n}','{Rel}','{Blood_group}','{nation}',
			'{Pre_add}','{Perm_add}','{re_date}','In Progress')'''
			cursor.execute(query)
			db.commit()
			st.success(f"Congratulation **{sname}**! You have been *Registered* successfully")
			with st.container():
				c1,c2=st.columns((1.5,1))
				c1.markdown("<h4 style='color:Silver;'>Here is your Unique ID :</h4>",unsafe_allow_html=True)
				c2.code(id)
				st.warning("Please Store your **UNIQUE ID**!! You can track your current status using this code")
        
def info():
	st.markdown("<h1 style='text-align: center;color: MediumSeaGreen;'>Applicant's Information Panel</h1>",unsafe_allow_html=True)
	id=st.text_input('Enter your unique ID here')
	Submit=st.button(label='Search')
	if Submit:
		cursor.execute(f"select * from KOTA where id='{id}'")
		tables = cursor.fetchall()
		# st.write(tables)
		size=len(tables)
		if(size==0):
			st.error('Your ID is not correct, Try Again')
		else:
			for i in tables:
				st.markdown("<h4 style='text-align: center;'>Your Information</h4>",unsafe_allow_html=True)
				test=st.expander('',True)
				with test:
					col1,col2=st.columns((4,3))
					col1.write('Name : ')
					col2.write(i[1])
					col1.write("Mother Name: ")
					col2.write(i[2])
					col1.write('Father Name: ')
					col2.write(i[3])
					col1.write('Gender: ')
					col2.write(i[4])
					col1.write('Phone Number: ')
					col2.write(i[5])
					col1.write('Email Address: ')
					col2.write(i[6])
					col1.write('Religion: ')
					col2.write(i[7])
					col1.write('Blood Group: ')
					col2.write(i[8])
					col1.write('Nationality :')
					col2.write(i[9])
					col1.write('Present Address')
					col2.write(i[10])
					col1.write('Permanent Address')
					col2.write(i[11])
					col1.write("Applicant's Regestered Date: ")
					col2.write(i[12])
        # for i in tables:


def stat():
	st.markdown("<h2 style='text-align: center;color: IndianRed;'>Applicant's Status Bar</h2>",unsafe_allow_html=True)
	id=st.text_input('Search Your Unique ID')
	submit=st.button('Search',key='sub')
	if submit:
		cursor.execute(f"Select st_name,status from KOTA where id='{id}'")
		table=cursor.fetchall()
		size=len(table)
		if(size==0):
			st.error("Incorrect ID")
		else:
			with st.container():
				c1,c2,c3=st.columns((2.3,1,1))
				c1.subheader(f"{table[0][0]}'s current status is ")
				if(table[0][1]=='Accepted'):
					c2.success('Accepted')
				elif(table[0][1]=='Rejected'):
					c2.error('Rejected')
				else:
					c2.warning(f"In Progress")
		if(size!=0 and table[0][1]=='Accepted'):
			st.balloons()
			st.subheader('Congratulation You have been selected! Please Contact with our admin office at Kumira Campus')
		elif(size!=0 and table[0][1]=='Rejected'):
			st.markdown("<h3 style='color: OrangeRed;'>Sorry!! We couldn't select you for valid reason</h3>",unsafe_allow_html=True)
		elif(size!=0 and table[0][1]=='In Progress'):
			st.info("Please visit again later we are still validating")




       

def main():
    # st.markdown("<h1 style='text-align: center; color: Tomato;'>Admission Forum of Masters in Data Science</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center; color: Forestgreen;'>International Islamic University Chittagong</h3>",unsafe_allow_html=True)
    selected=st.sidebar.selectbox('Select Your Option',
                        ('Choose Any',
                        'Admin',
                        'Registration',
                        'Information',
                        'Status'
                        ))
    if selected=='Admin':
        admin()
    elif selected=='Registration':
        form()
    elif selected=='Information':
        info()
    elif selected=='Status':
        stat()
    else:
    	st.markdown("<h1 style='text-align: center; color: DodgerBlue;'>Admission Form of Masters in Data Science</h1>", unsafe_allow_html=True)
    	st.markdown("<h3 style='text-align: center; color: Forestgreen;'>International Islamic University Chittagong</h3>",unsafe_allow_html=True)
if __name__=='__main__':
    main()
