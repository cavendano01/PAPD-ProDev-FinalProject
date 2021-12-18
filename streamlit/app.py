# import pathlib
# import pydicom
import streamlit as st
import mysql.connector as connection
import pandas as pd

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")


mydb = connection.connect(host="mysql_db", database='padp_db', user="padp_user", passwd="padp_pw", use_pure=True)
query = "Select * from covid19.merged;"
df = pd.read_sql(query, mydb)
mydb.close()  # close the connection

st.table(df)
