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
    page_title="Admission Form",
    page_icon=":sunny:",
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
st.write(tables)

# def admin():
#     username=st.sidebar.text_input('Username',key='user')
#     password=st.sidebar.text_input('Password',type='password',key='pass')
#     st.session_state.login=st.sidebar.checkbox('Login')
 
#     if st.session_state.login==True:
#         if username=="name" and password=='password':
#             st.sidebar.success('Login Success')

#             date1=st.date_input('Date1')
#             date2=st.date_input('Date2')
#             cursor.execute(f"select * from information where re_date between '{date1}' and '{date2}'")
#             # db.commit()
#             tables =cursor.fetchall()
#             # st.write(tables)
#             for i in tables:
#                 st.write(i[1])
#                 st.write(i[2])
#                 Accept=st.button('Accept',key=i[0])
#                 if Accept:
#                     st.write('Accepted')
#                     cursor.execute(f"Update information set status='Accepted' where id='{i[0]}'")
#                     db.commit()
#                 Reject=st.button('Reject',key=i[0])
#                 if Reject:
#                     st.write('Rejected')
#                     cursor.execute(f"Update information set status='Rejected' where id='{i[0]}'")
#                     db.commit()

#         else:
#             st.sidebar.warning('Wrong Credintials')


def form():
    id=uuid4()
    id=str(id)[:5]
    with st.form(key='member form'):
        sname=st.text_input('Student Name')
        s1name=st.text_input("Mother's Name")
        s2name=st.text_input("Father's Name")
        with st.container():
            col_1,col_2=st.columns((1,1))
            gen_name=col_1.selectbox("Gender",['Choose','Male','Female','Other'])
            Blood_group=col_2.selectbox('Blood Group',['Choose','O+','O-','A+','A-','AB+','AB-','B+','B-'])
        with st.container():
            c1,c2=st.columns((1,1))
            ph_num=c1.text_input('Number')
            email_n=c2.text_input('Email')
        Rel=st.selectbox('Religion',['Select Option','Islam','Hinduism','Buddhist','Christianity','Others'])
        nation=st.text_input('Nationality')
        Pre_add=st.text_input('Present Address')
        Perm_add=st.text_input('Permanent Address')
        re_date=st.date_input('Registration Date')
        # status='In Progress'
        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO KOTA (id,st_name,mother_name,father_name,Gender,Ph_Num,Email,Religion,BloodG,Nationality,
                                                Present_Add,Permmanent_Add,reg_date,status) VALUES ('{id}','{sname}','{s1name}',
                                                '{s2name}','{gen_name}','{ph_num}','{email_n}','{Rel}','{Blood_group}','{nation}',
                                                '{Pre_add}','{Perm_add}','{re_date}','In Progress')'''
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{sname}*! You have successfully Registered')
            st.code(id)
            st.warning("Please Store this code!!!")
        
# def info():
#     id=st.text_input('Your Code')
#     Submit=st.button(label='Search')
#     if Submit:
#         cursor.execute(f"select * from information where id='{id}'")
#         tables = cursor.fetchall()
#         st.write(tables)

def stat():
    id=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select status from KOTA where id='{id}'")
        table=cursor.fetchall()
        st.write(table)

def main():
    st.title('Diploma in Data Science Admission')
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
#     elif selected=='Information':
#         info()
    elif selected=='Status':
        stat()
if __name__=='__main__':
    main()
