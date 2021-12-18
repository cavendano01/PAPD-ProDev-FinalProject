import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector as connection


st.set_page_config(
     page_title="COVID19 Dashboard",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get help': 'https://cavendano01.notion.site/My-Dashboard-Help-Center-06578557c1674760ab4b84c068da4b6f',
         'About': "https://github.com/cavendano01/PAPD-ProDev-FinalProject"
     }
 )

st.title('COVID19 Dashboard')

# Creating Data Frame
mydb = connection.connect(host="mysql_db", database = 'covid19',user="covid19", passwd="secretpass",use_pure=True)
query = "Select * from covid19.data;"
df = pd.read_sql(query,mydb)
mydb.close() #close the connection

st.table(df.head(100))

def filter_df(df, start_date, end_date, countries, states):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    if len(countries) > 0:
        mask &= (df['country'].isin(countries))

    if len(states) > 0:
        mask &= (df['state'].isin(states))

    return df[mask]

def get_cases_count(df, grouby, status=["confirmed", "recovered","deaths"]):
    # delta_df = df[(df['status'] == status)].groupby(['country', 'state', 'lat', 'lon'], dropna=True)['count'].agg(['first', 'last']).reset_index()
    # delta_df['count'] = delta_df['last'] - delta_df['first']
    # delta_df["count_str"] = delta_df["count"].map('{:,d}'.format)
    # delta_df.drop(columns=['first', 'last'], inplace=True)
    count_df = df[(df['status'].isin(status))].groupby(grouby).agg({'cases_int': 'sum'}).reset_index()
    count_df["cases"] = count_df["cases_int"].map('{:,d}'.format)
    return count_df[(count_df["cases_int"] >= 0)]

covid_df = df