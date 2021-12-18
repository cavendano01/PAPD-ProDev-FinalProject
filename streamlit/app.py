import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector as connection

#Configuring Website High level features
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

# Filtering Lists
min_date = df['date'].min()
max_date = df['date'].max()
countries_list =pd.unique(df['country'].dropna()).tolist()
states_list = pd.unique(df['state'].dropna()).tolist()

#Sidebar  Filters
status_filter = st.sidebar.selectbox(
    "Status",
    ('confirmed', 'deaths', 'recovered')

)
start_date_filter = st.sidebar.date_input(
    "Start Date",
    min_date,
    min_value=min_date,
    max_value=max_date
)
end_date_filter = st.sidebar.date_input(
    "End Date",
    max_date,
    min_value=min_date,
    max_value=max_date
)
countries_filter = st.sidebar.multiselect(
    "Country",
    tuple(countries_list)
)
states_filter = st.sidebar.multiselect(
    "State",
    tuple(states_list)
)

#Aggregating Data By Category
def grouping_cases(df, grouby, status=["confirmed", "recovered","deaths"]):
    count_df = df[(df['status'].isin(status))].groupby(grouby).agg({'cases_int': 'sum'}).reset_index()
    count_df["cases"] = count_df["cases_int"].map('{:,d}'.format)
    return count_df[(count_df["cases_int"] >= 0)]

#Defining Right hand filters
def filters(df, start_date, end_date, countries, states):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    if len(countries) > 0:
        mask &= (df['country'].isin(countries))
    if len(states) > 0:
        mask &= (df['state'].isin(states))
    return df[mask]

#Creating Filtered Dataframe
filter_df = filters(df, start_date_filter, end_date_filter, countries_filter, states_filter)

col1, col2, col3 = st.columns([1, 1,1])
with col1:
    df_confirmed = filters(df, start_date_filter, end_date_filter, countries_filter, states_filter)
    df_confirmed.loc[df['status'] == 'confirmed'].sum()
    st.metric(label="Confirmed", value="100")
with col2:
    st.metric(label="Decesased", value="70 °F")
with col3:
    st.metric(label="Recovered", value="70 °F")

st.table(filter_df.head(8))

#Defining the Dashboard Layout
col1, col2 = st.columns([3, 1])
col2.subheader("Map of COVID prevalence")

#Populating Dashboard Layout
with col1:
    col1.subheader("Map of COVID prevalence")
    st.map(data=df, zoom=None, use_container_width=True)

with col2:
    col2.subheader("Map of COVID prevalence")
    st.area_chart(filter_df)













# Hasta aquí voy bien
