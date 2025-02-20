import streamlit as st
import pandas as pd
import numpy as np

from pages.demographic_data import demographic_df

#demographic_df = pd.read_csv(r'C:\Users\JessicaMahendran\OneDrive - lumilinks.com\Desktop\streamlit_in_snowflake\demographic_df.csv')

cluster_df = demographic_df.drop(columns=['Zip']).groupby('Cluster').mean().reset_index()

# select box for the user to select cluster 
select_cluster = st.selectbox('Select Cluster', cluster_df['Cluster'].unique())

# define column groups
age_columns = ['Children (0-15)', 'Youth (15-24)', 'Adult (25-60)', 'Senior (over 60)']
edu_columns = ['Less than high school', 'High school graduate', 'College/Associates degree', 'Bachelors or higher']
income_columns = ['<25k', '25k-50k', '50k-100k', 'over 100k']

# select box for the user to select feature
select_feature = st.multiselect('Select Feature', ['AGE', 'EDUCATION', 'INCOME'])

# plot
def create_bar_chart(data, selected_columns, title):
    st.subheader(title)
    st.bar_chart(data[selected_columns].T)
    
# filter df for selected cluster
filtered_df = cluster_df[cluster_df['Cluster'] == select_cluster]

# Generate charts based on selected features
if 'AGE' in select_feature:
    create_bar_chart(filtered_df, age_columns, 'Age Distribution')

if 'EDUCATION' in select_feature:
    create_bar_chart(filtered_df, edu_columns, 'Education Level Distribution')

if 'INCOME' in select_feature:
    create_bar_chart(filtered_df, income_columns, 'Income Distribution')
    
