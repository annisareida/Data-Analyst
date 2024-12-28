# -*- coding: utf-8 -*-
"""streamlit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VhhQV9s8yvIodjOmccApMkXO8kWwcgCP
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk membersihkan dan memproses data
def preprocess_data(df):
    df['kmDriven'] = df['kmDriven'].replace({' km': '', ',': ''}, regex=True).astype(float)
    df['AskPrice'] = df['AskPrice'].replace({'₹': '', ',': ''}, regex=True).astype(float)
    df['PostedDate'] = pd.to_datetime(df['PostedDate'], errors='coerce')
    df['Transmission'] = df['Transmission'].astype('category')
    df['Owner'] = df['Owner'].astype('category')
    df['FuelType'] = df['FuelType'].astype('category')
    return df

# Load dataset
st.title("Car Sales Analysis Dashboard")
st.write("Dataset sudah dimuat langsung dari file lokal.")
dataset_path = './used_car_dataset.csv'
df = pd.read_csv(dataset_path)

# Preprocessing data
df = preprocess_data(df)

# Sidebar untuk filter
st.sidebar.header("Filter Options")
selected_transmission = st.sidebar.selectbox("Select Transmission Type", options=df['Transmission'].cat.categories)
selected_owner = st.sidebar.selectbox("Select Ownership", options=df['Owner'].cat.categories)
selected_fuel = st.sidebar.selectbox("Select Fuel Type", options=df['FuelType'].cat.categories)

# Apply filters
filtered_data = df[
    (df['Transmission'] == selected_transmission) &
    (df['Owner'] == selected_owner) &
    (df['FuelType'] == selected_fuel)
]

# Display filtered data
st.subheader("Filtered Dataset")
st.write(filtered_data)

# Visualizations
st.subheader("Visualizations")

# Distribution of AskPrice
st.write("### Distribution of Car Prices")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['AskPrice'], kde=True, color='skyblue', ax=ax)
ax.set_title("Distribution of Car Prices")
ax.set_xlabel("Price (₹)")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Relationship between Age and AskPrice
st.write("### Relationship between Car Age and Price")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='Age', y='AskPrice', data=filtered_data, ax=ax)
ax.set_title("Car Age vs. Price")
ax.set_xlabel("Car Age (Years)")
ax.set_ylabel("Price (₹)")
st.pyplot(fig)

# Scatterplot of kmDriven and AskPrice
st.write("### Relationship between Distance Driven and Price")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='kmDriven', y='AskPrice', data=filtered_data, ax=ax)
ax.set_title("Distance Driven vs. Price")
ax.set_xlabel("Distance Driven (km)")
ax.set_ylabel("Price (₹)")
st.pyplot(fig)

# Correlation Heatmap
st.write("### Correlation Heatmap")
corr = filtered_data[['Age', 'kmDriven', 'AskPrice']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
ax.set_title("Correlation between Features")
st.pyplot(fig)
