import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import math
sns.set(style='dark')


st.title('Dashboard Penyewaan Sepeda')

min_date = pd.to_datetime('2011-01-01')
max_date = pd.to_datetime('2012-12-31') 
selected_season = None
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
col1, col2 = st.columns([1, 1])

st.header('Data Penjualan')
seasons = {
        0: "None",
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
}

with col2:
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )
    except ValueError:
        start_date = min_date
        end_date = max_date
    if not start_date == end_date:
        selected_season = st.selectbox("Pilih musim:", options=list(seasons.keys()), format_func=lambda x: seasons[x])


filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]


with col1:
    st.header('Total Penjualan')
    st.markdown(f"<h1 style='color: green;'>{filtered_hour_df['cnt'].sum()}</h1>", unsafe_allow_html=True)



if selected_season is None:
    selected_season = 0
    print(selected_season)
if selected_season == 0:
    filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]
else:
    filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date)) & (hour_df['season'] == selected_season)]


def format_jam(jam):
    if jam < 10:
        return f"0{jam}:00"
    return f"{jam}:00"

def create_daily_orders_df(df, max=20):
    daily_orders_df = df.groupby('dteday', as_index=False)['cnt'].sum()
    if len(daily_orders_df) == 1:
        daily_orders_df = df.groupby('hr', as_index=False)['cnt'].sum()
        rentang_data = math.ceil(len(daily_orders_df) / max)
        result = []
        for i in range(0, len(daily_orders_df), rentang_data):
            subset = daily_orders_df.iloc[i:i+rentang_data]
            total_cnt = subset['cnt'].sum()
            start_hr = subset['hr'].iloc[0]
            end_hr = subset['hr'].iloc[-1]
            result.append({'start_hr': format_jam(start_hr), 'end_hr': format_jam(end_hr), 'cnt': total_cnt})
        result_df = pd.DataFrame(result)
        return result_df

    rentang_data = math.ceil(len(daily_orders_df) / max)
    result = []
    
    for i in range(0, len(daily_orders_df), rentang_data):
        subset = daily_orders_df.iloc[i:i+rentang_data]
        total_cnt = subset['cnt'].sum()
        start_date = subset['dteday'].iloc[0]
        end_date = subset['dteday'].iloc[-1]
        result.append({'dteday': start_date, 'end_date': end_date, 'cnt': total_cnt})
    result_df = pd.DataFrame(result)
    return result_df

daily_orders_df = create_daily_orders_df(filtered_hour_df, 9)
if not 'start_hr' in daily_orders_df.columns:
    daily_orders_df['date_range'] = '(' + daily_orders_df['dteday'].astype(str) + ')\n(' + daily_orders_df['end_date'].astype(str) + ')'
    plt.figure(figsize=(12, 6))
    sns.barplot(x='date_range', y='cnt', data=daily_orders_df, errorbar=None, palette='viridis')
    sns.despine()
    if not selected_season == 0:
        plt.title(f"Distribution of Bike Rentals by Date Range {seasons[selected_season]}", fontsize=20)
    else:
        plt.title("Distribution of Bike Rentals by Date Range", fontsize=20)
    plt.xlabel('Date Range', fontsize=20)
    plt.ylabel('Number of Bike Rentals', fontsize=16)
    plt.xticks(rotation=25)
    plt.grid(False)
    st.pyplot(plt)
else:
    daily_orders_df['date_range'] = '(' + daily_orders_df['start_hr'].astype(str) + ')\n(' + daily_orders_df['end_hr'].astype(str) + ')'
    plt.figure(figsize=(12, 6))
    sns.barplot(x='date_range', y='cnt', data=daily_orders_df, errorbar=None, palette='viridis')
    sns.despine()
    plt.title('Distribution of Bike Rentals by Time Range')
    plt.xlabel('Time Range', fontsize=16)
    plt.ylabel('Number of Bike Rentals', fontsize=16)
    plt.grid(False)
    st.pyplot(plt)

st.header('Data Musim Penjualan Terbaik')
seasons_df = hour_df.copy()
seasons_df['season'] = seasons_df['season'].map(seasons)
plt.figure(figsize=(12, 6))
sns.barplot(x='cnt', y='season', data=seasons_df, errorbar=None, palette='pastel')
sns.despine()
plt.title('Distribution of Bike Rentals by Seasons', fontsize=22)
plt.xlabel('Many Sales', fontsize=16)
plt.ylabel('', fontsize=16)
plt.grid(False)
st.pyplot(plt)

st.header('Data Evaluasi Penjualan Bulanan')
year = {
    0 : "2011",
    1 : "2012"
}

selected_year = st.selectbox("Pilih Tahun:", options=list(year.keys()), format_func=lambda x: year[x])


# Filter DataFrame berdasarkan pilihan tahun
filtered_df = hour_df[hour_df['yr'] == selected_year]
grouped_by_month = filtered_df.groupby(filtered_df['dteday'].dt.month)['cnt'].sum().reset_index()
grouped_by_month['dteday'] = pd.to_datetime(grouped_by_month['dteday'], format='%m').dt.strftime('%B')

plt.figure(figsize=(12, 6))
sns.barplot(y='cnt', x='dteday', data=grouped_by_month, errorbar=None, palette='Accent')
sns.despine()
plt.title('Distribution of Bike Rentals by Seasons', fontsize=22)
plt.xlabel('Many Sales', fontsize=16)
plt.ylabel('', fontsize=16)
plt.grid(False)
st.pyplot(plt)


st.header('Data Evaluasi Penjualan Pengaruh Cuaca')
weather_labels = {
    1: 'Clear/Few clouds',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Fog'
}
hour_df['weather_impact'] = hour_df['weathersit'].map(weather_labels)
plt.figure(figsize=(10, 6))
sns.barplot(y='weather_impact', x='cnt', data=hour_df, errorbar=None, hue='weather_impact', palette='viridis', legend=False, order=['Clear/Few clouds', 'Mist/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Fog'])
sns.despine()
plt.title('Distribution of Bike Rentals by Weather Conditions')
plt.xlabel('Weather Conditions', fontsize=20)
plt.ylabel('')
plt.grid(False)
st.pyplot(plt)

st.header('Pengguna Registered dan Casual')
plt.figure(figsize=(8, 8))
grouped_df = hour_df.groupby('dteday')[['casual', 'registered']].sum().reset_index()
plt.title('Distribusi Total Pengguna Terdaftar dan Casual')
plt.pie(grouped_df[['casual', 'registered']].sum(), labels=['Casual', 'Registered'], colors=['#ff9999','#66b3ff'])
plt.axis('equal')  
st.pyplot(plt)