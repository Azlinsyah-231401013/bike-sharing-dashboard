import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    daily_rent_df.rename(columns={"cnt": "total_count"}, inplace=True)
    return daily_rent_df

def create_seasonal_rent_df(df):
    seasonal_df = df.groupby("season").cnt.mean().reset_index()
    seasonal_df.rename(columns={"cnt": "avg_count"}, inplace=True)
    return seasonal_df

def create_workingday_user_df(df):
    workingday_df = df.groupby("workingday").agg({
        "casual": "mean",
        "registered": "mean"
    }).reset_index()
    workingday_df['workingday'] = workingday_df['workingday'].map({
        0: 'Weekend/Holiday',
        1: 'Working Day'
    })
    return workingday_df

def create_temp_cluster_df(df):
    def categorize_temp(temp):
        if temp < 0.3: return 'Dingin (Cold)'
        elif 0.3 <= temp < 0.6: return 'Sejuk (Mild)'
        else: return 'Panas (Hot)'
    
    df['temp_cluster'] = df['temp'].apply(categorize_temp)
    cluster_df = df.groupby("temp_cluster").cnt.mean().reset_index()
    cluster_df.rename(columns={"cnt": "avg_count"}, inplace=True)
    return cluster_df

current_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(current_dir, "day.csv")

day_df = pd.read_csv(file_path)

day_df["dteday"] = pd.to_datetime(day_df["dteday"])

day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

with st.sidebar:
    st.title("Bike Sharing Dashboard 🚲")

    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu Analisis',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

daily_rent_df = create_daily_rent_df(main_df)
seasonal_rent_df = create_seasonal_rent_df(main_df)
workingday_user_df = create_workingday_user_df(main_df)
temp_cluster_df = create_temp_cluster_df(main_df)

st.header('Bike Sharing Analysis Dashboard ✨')

col1, col2, col3 = st.columns(3)

with col1:
    total_rent = main_df.cnt.sum()
    st.metric("Total Peminjaman", value=f"{total_rent:,}")

with col2:
    avg_casual = int(main_df.casual.mean())
    st.metric("Rata-rata Kasual", value=avg_casual)

with col3:
    avg_registered = int(main_df.registered.mean())
    st.metric("Rata-rata Terdaftar", value=avg_registered)

st.subheader('Daily Rental Trend')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dteday"],
    daily_rent_df["total_count"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Tren Peminjaman Sepeda Harian", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader("Analisis Musim dan Perilaku Pengguna")

col_a, col_b = st.columns(2)

with col_a:
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        x="season", 
        y="avg_count",
        data=seasonal_rent_df.sort_values(by="avg_count", ascending=False),
        palette="viridis",
        ax=ax
    )
    ax.set_title("Rata-rata Peminjaman per Musim", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

with col_b:
    melted_user_df = pd.melt(
        workingday_user_df, 
        id_vars=['workingday'], 
        value_vars=['casual', 'registered'],
        var_name='user_type', 
        value_name='avg_count'
    )
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        x="workingday", 
        y="avg_count", 
        hue="user_type", 
        data=melted_user_df,
        palette=["#FF9999", "#99FF99"],
        ax=ax
    )
    ax.set_title("User Behavior: Working Day vs Weekend", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

st.subheader("Advanced Analysis: Temperature Clustering")
st.write("Melihat pengaruh suhu terhadap rata-rata peminjaman sepeda.")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="temp_cluster", 
    y="avg_count",
    data=temp_cluster_df,
    palette="YlOrRd",
    ax=ax
)
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_xlabel("Klaster Suhu")
st.pyplot(fig)

st.caption('Copyright (c) Priadi Cuanda 2026 - DBS Coding Camp')
