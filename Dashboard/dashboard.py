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

try:
    day_df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"File day.csv tidak ditemukan di {file_path}. Pastikan file diletakkan di direktori yang sama dengan dashboard.py")
    st.stop()

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
    st.metric("Rata-rata Kasual", value=f"{avg_casual:,}")
with col3:
    avg_registered = int(main_df.registered.mean())
    st.metric("Rata-rata Terdaftar", value=f"{avg_registered:,}")

st.markdown("---")

st.subheader("1. Tren Rata-rata Peminjaman Berdasarkan Musim")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="season", 
    y="avg_count",
    data=seasonal_rent_df.sort_values(by="avg_count", ascending=False),
    palette="viridis",
    ax=ax1
)
ax1.set_title("Rata-rata Peminjaman per Musim (2011-2012)", fontsize=15)
ax1.set_ylabel("Rata-rata Peminjaman Harian")
ax1.set_xlabel("Musim")

for p in ax1.patches:
    ax1.annotate(format(p.get_height(), '.0f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', xytext = (0, 8), textcoords = 'offset points', weight='bold')

st.pyplot(fig1)

with st.expander("Lihat Penjelasan (Insight)"):
    st.write(
        """
        Berdasarkan grafik di atas, **Musim Gugur (Fall)** adalah musim puncak penyewaan dengan rata-rata tertinggi, 
        disusul oleh Musim Panas (Summer). Sebaliknya, **Musim Semi (Spring)** memiliki tingkat rata-rata peminjaman paling rendah.
        """
    )

st.markdown("---")

st.subheader("2. Perbandingan Perilaku Pengguna (Hari Kerja vs Akhir Pekan)")
melted_user_df = pd.melt(
    workingday_user_df, 
    id_vars=['workingday'], 
    value_vars=['casual', 'registered'],
    var_name='user_type', 
    value_name='avg_count'
)

melted_user_df['user_type'] = melted_user_df['user_type'].map({
    'casual': 'Kasual',
    'registered': 'Terdaftar'
})

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="workingday", 
    y="avg_count", 
    hue="user_type", 
    data=melted_user_df,
    palette=["#FF9999", "#99FF99"],
    ax=ax2
)
ax2.set_title("Rata-rata Pengguna Kasual vs Terdaftar (2011-2012)", fontsize=15)
ax2.set_ylabel("Rata-rata Peminjaman Harian")
ax2.set_xlabel("Tipe Hari")

for p in ax2.patches:
    ax2.annotate(format(p.get_height(), '.0f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', xytext = (0, 8), textcoords = 'offset points', weight='bold')

st.pyplot(fig2)

with st.expander("Lihat Penjelasan (Insight)"):
    st.write(
        """
        Terlihat pola kontras: Pengguna **Terdaftar (Registered)** mendominasi pada **Hari Kerja**, menandakan sepeda digunakan untuk 
        mobilitas harian komuter. Namun, pada **Akhir Pekan (Weekend/Holiday)**, jumlah penyewaan oleh pengguna terdaftar menurun, 
        sementara pengguna **Kasual** melonjak tajam lebih dari dua kali lipat untuk kebutuhan rekreasi.
        """
    )

st.markdown("---")

st.subheader("3. Advanced Analysis: Temperature Clustering")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="temp_cluster", 
    y="avg_count",
    data=temp_cluster_df.sort_values(by="avg_count", ascending=False),
    palette="YlOrRd",
    ax=ax3
)
ax3.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Klaster Suhu", fontsize=15)
ax3.set_ylabel("Rata-rata Peminjaman Harian")
ax3.set_xlabel("Klaster Suhu")

for p in ax3.patches:
    ax3.annotate(format(p.get_height(), '.0f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', xytext = (0, 8), textcoords = 'offset points', weight='bold')

st.pyplot(fig3)

st.caption('Copyright (c) Azlinsyah 2026 - DBS Coding Camp')
