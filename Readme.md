# Bike Sharing Data Analysis Dashboard 🚲✨

## Deskripsi Proyek
Proyek ini merupakan submission akhir untuk kelas **Belajar Analisis Data dengan Python** dari Dicoding (Coding Camp powered by DBS 2026). Proyek ini berfokus pada analisis dataset *Bike Sharing* untuk menggali *insight* bisnis yang berharga, meliputi proses *Data Wrangling*, *Exploratory Data Analysis* (EDA), *Advanced Analysis* (Clustering/Binning), dan pembuatan *dashboard* interaktif menggunakan Streamlit.

## Pertanyaan Bisnis
1. Bagaimana tren total peminjaman sepeda berdasarkan musim sepanjang tahun 2011 hingga 2012?
2. Bagaimana perbandingan perilaku peminjaman antara pengguna kasual dan pengguna terdaftar pada hari kerja dibandingkan hari libur/akhir pekan?

## Struktur Direktori
- `/data`: Direktori ini berisi dataset mentah (`day.csv`) yang digunakan dalam proyek.
- `/dashboard`: Direktori ini berisi file `dashboard.py` yang digunakan untuk membuat dashboard interaktif menggunakan Streamlit.
- `notebook.ipynb`: File ini berisi proses analisis data secara lengkap menggunakan Jupyter Notebook / Google Colab.
- `requirements.txt`: File ini berisi daftar *library* yang dibutuhkan untuk menjalankan proyek ini.
- `README.md`: File informasi mengenai proyek ini.

## Setup Environment - Anaconda
Jika Anda menggunakan distribusi Anaconda, jalankan perintah berikut pada Anaconda Prompt:

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
