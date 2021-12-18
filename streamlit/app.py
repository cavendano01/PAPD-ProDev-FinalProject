# import pathlib
# import pydicom
import streamlit as st
import mysql.connector as connection
import pandas as pd


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

try:
    mydb = connection.connect(host="mysql_db", database = 'covid19',user="covid19", passwd="secretpass",use_pure=True)
    query = "Select * from covid19.global_data;"
    result_dataFrame = pd.read_sql(query,mydb)
    mydb.close() #close the connection
except Exception as e:
    mydb.close()
    print(str(e))


st.table(result_dataFrame)
