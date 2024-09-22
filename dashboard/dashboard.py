import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


st.title('Dashboard Penyewaan Sepeda')

min_date = pd.to_datetime('2011-01-01')  # Tanggal minimal
max_date = pd.to_datetime('2012-12-31')  # Tanggal maksimal

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
with st.sidebar:
    st.subheader('Pilih Rentang Data')

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.header('Data Penjualan')
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

col1, col2 = st.columns([1, 1])

with col1:
    st.write("Jumlah Penjualan")
    st.write(filtered_hour_df['cnt'].sum())

with col2:
    st.header("Kolom 2")

# plot_df = filtered_hour_df.groupby('dteday')['cnt'].sum().reset_index()
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

# Mengelompokkan data ke dalam rentang 10 hari
filtered_hour_df['date_range'] = pd.cut(filtered_hour_df['dteday'], 
                                          bins=pd.date_range(start=start_date, end=end_date, freq='10D'),
                                          right=False)

# Menghitung total penjualan untuk setiap rentang
plot_df = filtered_hour_df.groupby('date_range')['cnt'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='dteday', y='cnt', data=filtered_hour_df, errorbar=None, hue='dteday', palette='viridis', legend=False)
sns.despine()
plt.title('Distribution of Bike Rentals by Weather Conditions')
plt.xlabel('Weather Conditions', fontsize=20)
plt.ylabel('Number of Bike Rentals')
plt.grid(False)
st.pyplot(plt)
