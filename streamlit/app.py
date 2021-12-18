import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector as connection
import pydeck as pdk
import plotly.express as px


# Configuring Website High level features
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
# @st.cache(allow_output_mutation=True) Convertir a función que permita uso de cache
mydb = connection.connect(host="mysql_db", database='covid19', user="covid19", passwd="secretpass", use_pure=True)
query = "Select * from covid19.data;"
df = pd.read_sql(query, mydb)
mydb.close()  # close the connection

# Filtering Lists
min_date = df['date'].min()
max_date = df['date'].max()
countries_list = pd.unique(df['country'].dropna()).tolist()
states_list = pd.unique(df['state'].dropna()).tolist()

# Sidebar  Filters
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


# Aggregating Data By Category
def get_cases_count(df, grouby, status=["confirmed", "recovered", "deaths"]):
    # delta_df = df[(df['status'] == status)].groupby(['country', 'state', 'lat', 'lon'], dropna=True)['count'].agg(['first', 'last']).reset_index()
    # delta_df['count'] = delta_df['last'] - delta_df['first']
    # delta_df["count_str"] = delta_df["count"].map('{:,d}'.format)
    # delta_df.drop(columns=['first', 'last'], inplace=True)
    count_df = df[(df['status'].isin(status))].groupby(grouby).agg({'cases_int': 'sum'}).reset_index()
    count_df["cases"] = count_df["cases_int"].map('{:,d}'.format)
    return count_df[(count_df["cases_int"] >= 0)]


# Defining Right hand filters
def filters(df, start_date, end_date, countries, states):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    if len(countries) > 0:
        mask &= (df['country'].isin(countries))
    if len(states) > 0:
        mask &= (df['state'].isin(states))
    return df[mask]


# Creating Filtered Dataframe
filter_df = filters(df, start_date_filter, end_date_filter, countries_filter, states_filter)
#filter_confirmed = get_cases_count(filter_df, ['country', 'state', 'lat', 'lon'], ["confirmed"])
#filter_recovered = get_cases_count(filter_df, ['country', 'state', 'lat', 'lon'], ["recovered"])
#filter_death = get_cases_count(filter_df, ['country', 'state', 'lat', 'lon'], ["deaths"])

# Metric Summary when applying all other variables
num_confirmed = filter_df.loc[(df['status'] == 'confirmed'), 'cases'].sum()
#num_confirmed = get_cases_count(filter_df, ['country', 'state', 'lat', 'lon'], ["confirmed"])
num_deaths = filter_df.loc[(df['status'] == 'deaths'), 'cases'].sum()
num_recover = filter_df.loc[(df['status'] == 'recovered'), 'cases'].sum()

# Metrics Summary
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.metric(label="Confirmed", value=num_confirmed)

with col2:
    st.metric(label="Decesased", value=num_deaths)
with col3:
    st.metric(label="Recovered", value=num_recover)



map_df = pd.DataFrame(filter_df.dropna(subset=['lat','lon']))

fig = px.scatter_mapbox(map_df, lat="lat", lon="lon", hover_name="country", hover_data=["state", "cases"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
st.plotly_chart(fig)

st.table(filter_df.head(8))





