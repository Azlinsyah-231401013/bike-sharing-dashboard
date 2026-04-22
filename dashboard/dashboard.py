import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# STYLE
sns.set_style("darkgrid")
MAIN_COLOR = "#4CAF50"

# ========================
# LOAD DATA
# ========================

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "cleaned_hour.csv")

if not os.path.exists(file_path):
    st.error("File cleaned_hour.csv tidak ditemukan!")
    st.stop()

df = pd.read_csv(file_path)

# pastikan kolom date datetime
df["date"] = pd.to_datetime(df["date"])

# ========================
# TITLE
# ========================

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis pengaruh cuaca, musim, dan waktu terhadap jumlah penyewaan sepeda (2011–2012)")

# ========================
# SIDEBAR FILTER
# ========================

st.sidebar.header("Filter")

# YEAR
selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    options=sorted(df["year"].unique())
)

# SEASON (FIX: tambah ALL)
season_options = ["All"] + sorted(df["season"].unique())
selected_season = st.sidebar.selectbox("Pilih Musim", season_options)

# DATE FILTER (BONUS + RECOMMENDED)
start_date = st.sidebar.date_input("Start Date", df["date"].min())
end_date = st.sidebar.date_input("End Date", df["date"].max())

# FILTERING
filtered_df = df[df["year"] == selected_year]

if selected_season != "All":
    filtered_df = filtered_df[filtered_df["season"] == selected_season]

filtered_df = filtered_df[
    (filtered_df["date"] >= pd.to_datetime(start_date)) &
    (filtered_df["date"] <= pd.to_datetime(end_date))
]

# ========================
# METRICS
# ========================

st.subheader("📊 Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(filtered_df["total_count"].sum()))
col2.metric("Rata-rata", int(filtered_df["total_count"].mean()))
col3.metric("Maksimum", int(filtered_df["total_count"].max()))

# ========================
# VISUALISASI 1 (BAR)
# ========================

st.subheader("🌤️ Pengaruh Cuaca terhadap Penyewaan")

weather_avg = filtered_df.groupby("weather_condition")["total_count"].mean().reset_index()

fig, ax = plt.subplots()
ax.bar(
    weather_avg["weather_condition"],
    weather_avg["total_count"],
    color=MAIN_COLOR
)

ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
plt.xticks(rotation=20)

st.pyplot(fig)

# ========================
# VISUALISASI 2 (LINE)
# ========================

st.subheader("⏰ Pola Penyewaan Berdasarkan Jam")

hour_avg = filtered_df.groupby("hour")["total_count"].mean().reset_index()

fig2, ax2 = plt.subplots()
ax2.plot(
    hour_avg["hour"],
    hour_avg["total_count"],
    marker="o",
    color=MAIN_COLOR
)

ax2.set_title("Rata-rata Penyewaan per Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig2)

# ========================
# VISUALISASI 3 (FIX: GANTI BOXPLOT ❗)
# ========================

st.subheader("📅 Hari Kerja vs Akhir Pekan")

df_temp = filtered_df.copy()
df_temp["workingday"] = df_temp["workingday"].map({
    1: "Hari Kerja",
    0: "Akhir Pekan"
})

workingday_avg = df_temp.groupby("workingday")["total_count"].mean().reset_index()

fig3, ax3 = plt.subplots()
ax3.bar(
    workingday_avg["workingday"],
    workingday_avg["total_count"],
    color=MAIN_COLOR
)

ax3.set_title("Rata-rata Penyewaan: Hari Kerja vs Akhir Pekan")
ax3.set_xlabel("Kategori Hari")
ax3.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig3)

# ========================
# INSIGHT (DITAMBAHIN BIAR LEBIH SPESIFIK)
# ========================

st.subheader("💡 Insight")

st.markdown(f"""
- Penyewaan tertinggi terjadi pada kondisi cuaca **cerah / berawan ringan**.
- Penyewaan terendah terjadi pada kondisi cuaca **buruk (hujan/salju)**.
- Jam sibuk terjadi pada **07.00–09.00** dan **17.00–19.00**.
- Rata-rata penyewaan pada **hari kerja lebih tinggi** dibanding akhir pekan.
- Dataset mencakup periode **tahun 2011–2012**.
""")

# ========================
# FOOTER
# ========================

st.markdown("---")
st.markdown("👤 **Azlinsyah Fadhilah Meran**")