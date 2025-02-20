import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def generate_fixed_random_proportions(rows, columns, seed=42):
    np.random.seed(seed)
    data = np.random.dirichlet(np.ones(columns), size=rows) * 100
    data = np.round(data, 1)
    return data

def create_dataframe(zip_codes, columns, column_names):
    data = generate_fixed_random_proportions(zip_codes, columns)
    df = pd.DataFrame(data, columns=column_names)
    df.insert(0, "Zip", range(1, zip_codes + 1))
    return df

zip_codes = 100

# Income Table
income_columns = ["<25k", "25k-50k", "50k-100k", "over 100k"]
income_df = create_dataframe(zip_codes, len(income_columns), income_columns)

# Age Table
age_columns = ["Children (0-15)", "Youth (15-24)", "Adult (25-60)", "Senior (over 60)"]
age_df = create_dataframe(zip_codes, len(age_columns), age_columns)

# Education Table
education_columns = ["Less than high school", "High school graduate", "College/Associates degree", "Bachelors or higher"]
education_df = create_dataframe(zip_codes, len(education_columns), education_columns)

# Display the tables
st.write("Income Table")
st.write(income_df.head())
st.write("\nAge Table")
st.write(age_df.head())
st.write("\nEducation Table")
st.write(education_df.head())

# merge the three tables
demographic_df = pd.merge(age_df, education_df, on='Zip', how='inner')
demographic_df = pd.merge(demographic_df, income_df, on='Zip', how='inner')


# cluster using KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
demographic_df['Cluster'] = kmeans.fit_predict(demographic_df.drop(columns=['Zip']))

st.write("\nFinal Table")
st.write(demographic_df.head())

# save demographic df to use in the next page
demographic_df.to_csv('demographic_df.csv', index=False)