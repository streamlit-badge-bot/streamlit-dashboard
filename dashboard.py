import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import xlrd

# Set title
st.title ('PhDs awarded in the US visualization')

# simple description
st.write('In this dashboard we will analyze the PhDs awarded in the US data from the National Center for Science and Engineering Statistics (NCSES) within the National Science Foundation (NSF). These charts are interactive.')

# Chart I: Number of PhD recipients by field of study
# load data
@st.cache
def load_field_data():
    data = pd.read_excel('./data_tables/new-sed17-sr-tab017.xlsx')
    return data
field = load_field_data()

# set widgets
st.sidebar.title('Chart I')
study_field = st.sidebar.selectbox('Select broad field of study', ['All fields', 'Life sciences', 'Physical sciences and earth sciences', 'Mathematics and computer sciences', 'Psychology and social sciences','Engineering', 'Education', 'Humanities and arts', 'Other'])
st.subheader(f'Chart I: Number of doctorate recipients  for {study_field} (1987-2017)')

# Checkbox to show raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(field)

# Partition data of a selected field by status 

mapping = {'All fields': ['U.S. citizen or permanent resident',
       'Temporary visa holder', 'Unknown'], 
           'Life sciences': ['U.S. citizen or permanent resident.1', 'Temporary visa holder.1', 'Unknown.1'],
          'Physical sciences and earth sciences':['U.S. citizen or permanent resident.2', 'Temporary visa holder.2', 'Unknown.2'],
           'Mathematics and computer sciences':['U.S. citizen or permanent resident.3', 'Temporary visa holder.3', 'Unknown.3'],
           'Psychology and social sciences': ['U.S. citizen or permanent resident.4', 
                                             'Temporary visa holder.4', 'Unknown.4'],
           'Engineering': ['U.S. citizen or permanent resident.5', 'Temporary visa holder.5', 'Unknown.5'],
           'Education':['U.S. citizen or permanent resident.6', 'Temporary visa holder.6', 'Unknown.6'],
           'Humanities and arts':['U.S. citizen or permanent resident.7', 'Temporary visa holder.7', 'Unknown.7'],
           'Other': ['U.S. citizen or permanent resident.8', 'Temporary visa holder.8', 'Unknown.8']
          }
mapping[study_field].insert(0, study_field)
selected_field_with_status = field[mapping[study_field]]

# If checkbox is checked, chart with citizenship status will be displayed.
show_status = st.sidebar.checkbox('Show Citizenship Status')
show_status_grouped = st.sidebar.checkbox('Show Grouped Citizenship Status')

if show_status:
    fig = go.Figure(data=[
        go.Bar(name='U.S. citizen or permanent resident', 
               x=selected_field_with_status.index,
               y=selected_field_with_status.iloc[:, 1]),
        go.Bar(name='Temporary visa holder',
               x=selected_field_with_status.index, 
               y=selected_field_with_status.iloc[:, 2]),
        go.Bar(name='Unknow',
               x=selected_field_with_status.index, 
               y=selected_field_with_status.iloc[:, 3])
               ])
    if show_status_grouped:
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)
    else:
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)
else:
    fig = px.bar(field, 
             x='Year',
             y=study_field
    )
    st.plotly_chart(fig)


# Chart II: Age Distribution of Doctorate Recipients
# load data
@st.cache
def load_age_data():
    data = pd.read_excel('./data_tables/sed17-sr-tab027.xlsx', skiprows=3)
    data.drop(['Median age at doctorate (years)a', 'All ages'], axis='columns', inplace=True) 
    data.set_index('Broad field of study and demographic characteristic', inplace=True)
    data = data.rename(index={'Life sciencesb': 'Life sciences',
                  'Otherc': 'Other'})
    return data
age = load_age_data()

# set widgets
st.sidebar.title('Chart II')
age_selection = st.sidebar.selectbox('Select broad field of study or sex or citizenship status', ['All fields', 'Life sciences', 'Physical sciences and earth sciences', 'Mathematics and computer sciences', 'Psychology and social sciences','Engineering', 'Education', 'Humanities and arts', 'Other', 'Male', 'Female', 'U.S. citizen or permanent resident', 'Temporary visa holder'])
st.subheader(f'Chart II: Age distribution of doctorate recipients for {age_selection} (1987-2017)')

fig = px.pie(age, values=age.loc[age_selection, :], 
                         names=age.columns,
                        title=age_selection)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)

st.markdown("""
Life Sciences includes agricultural sciences and natural resources; biological and biomedical sciences; and health sciences. 

Other includes other non-science and engineering fields not shown separately.
""")


