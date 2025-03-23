# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv('https://raw.githubusercontent.com/Jessica1711/Bike-Sharing-Dataset/refs/heads/main/data/day.csv')
hour_df = pd.read_csv('/content/drive/MyDrive/Proyek Analisis Data/hour.csv')

# Streamlit app
st.title("Analisis Data dengan Python 'Bike Sharing Data Dataset' :sparkle: ")
st.write("Selamat Datang di Analisis Data dengan Python untuk Data Bike Sharing. Terdapat 3 pertanyaan yang akan saya analisis, diantaranya :")
st.text("1. Bagaimana perbandingan tren jumlah pengguna sepeda di tahun 2011 dan 2012?")
st.text("2. Bagaimana pola perbandingan penyewaan sepeda harian?")
st.text("3. Bagaimana pengaruh musim terhadap jumlah penyewaan sepeda?")

# Mengubah tipe data menjadi tipe data datetime
try:
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
except ValueError:
    st.error("Gagal mengkonversi kolom 'dteday' ke tipe datetime. Pastikan format tanggal sudah benar.")
# Mengubah angka menjadi keterangan
day_df['mnth'] = day_df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'})
day_df['yr'] = day_df['yr'].map({
    0: '2011', 1: '2012'})
day_df['workingday'] = day_df['workingday'].map({
    0: 'Holiday', 1: 'Workingday'})

# Display data
st.header("Data")
st.text("Berikut adalah data yang saya gunakan untuk proses analisis data dengan python")
## Fungsi untuk menampilkan Data 1
def Day_Data():
  st.subheader("Day Data", divider="blue")
  st.dataframe(day_df.head())
## Fungsi untuk menampilkan Data 2
def Hour_Data():
  st.subheader("Hour Data", divider="blue")
  st.dataframe(hour_df.head())
## Inisialisasi session_state untuk menyimpan status tombol
if "active_data" not in st.session_state:
  st.session_state["active_data"] = None
## Sidebar untuk tombol pemilihan Data yang akan ditampilkan
st.write("### Pilih Data yang akan ditampilkan")
if st.button("Day_Data"):
  st.session_state["active_data"] = "Day_Data" if st.session_state["active_data"] != "Day_Data" else None
if st.button("Hour_Data"):
  st.session_state["active_data"] = "Hour_Data" if st.session_state["active_data"] != "Hour_Data" else None
## Menampilkan data berdasarkan tombol yang dipilih
if st.session_state["active_data"] == "Day_Data":
  st.write("Berikut adalah data pertama yang digunakan dalam proses analisis data")
  Day_Data()
elif st.session_state["active_data"] == "Hour_Data":
  st.write("Berikut adalah data kedua yang digunakan dalam proses analisis data")
  Hour_Data()

# Fitur Interaktif
## Sidebar untuk Filter Tanggal
st.sidebar.header("Filter Tanggal")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
tanggal_mulai = st.sidebar.date_input("Tanggal Mulai", min_date)
tanggal_akhir = st.sidebar.date_input("Tanggal Akhir", max_date)
## Menerapkan Filter
df_filtered = day_df[(day_df["dteday"] >= pd.to_datetime(tanggal_mulai))& (day_df["dteday"] <= pd.to_datetime(tanggal_akhir))]
## Menampilkan Data yang Difilter
st.header("Data Sepeda yang Difilter")
st.write(df_filtered)

#Visualisasi Data
st.header("Visualisasi Data")
##Pertanyaan 1
st.subheader("Perbandingan tren jumlah pengguna sepeda di tahun 2011 dan 2012")
if df_filtered is not None and not df_filtered.empty:
    ### Konversi bulan ke kategori
    df_filtered['mnth'] = pd.Categorical(df_filtered['mnth'], categories=
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
    ordered=True)
    monthly_counts = df_filtered.groupby(by=["mnth", "yr"]).agg({"cnt": "sum"}).reset_index()
    st.write("Data yang dikelompokkan:")
    st.write(monthly_counts) #menampilkan dataframe yang dikelompokkan
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_counts, x="mnth", y="cnt", hue="yr", palette="rocket", marker="o", ax=ax)
    ax.set_title("Tren Sewa Sepeda")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.legend(title="Tahun", loc="upper right")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.write("Tidak ada data yang ditemukan untuk rentang tanggal yang dipilih.")
## Pertanyaan 2
st.subheader("Perbandingan penyewaan sepeda harian dengan pola mingguan")
if df_filtered is not None and not df_filtered.empty:
    # Konversi bulan ke kategori
    df_filtered['weekday'] = pd.Categorical(df_filtered['weekday'], categories=
    ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    ordered=True)
    daily_counts = df_filtered.groupby(by='weekday').agg({'cnt': 'sum'}).reset_index()
    st.write("Data yang dikelompokkan:")
    st.write(daily_counts) #menampilkan dataframe yang dikelompokkan
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=daily_counts, x='weekday', y='cnt', palette='magma', ax=ax)
    ax.set_title('Perbandingan Penyewa Sepeda Setiap Hari')
    ax.set_xlabel(None)
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.write("Tidak ada data yang ditemukan untuk rentang tanggal yang dipilih.")

## Pertanyaan 3
st.subheader("Pengaruh musim terhadap jumlah penyewaan sepeda")
if df_filtered is not None and not df_filtered.empty:
  season_pattern = df_filtered.groupby('season')[['registered', 'casual']].sum().reset_index()
  st.write("Data yang dikelompokkan:")
  st.write(season_pattern) #menampilkan dataframe yang dikelompokkan
  fig, ax = plt.subplots(figsize=(10, 6))
  plt.bar(season_pattern['season'], season_pattern['registered'], label='Registered', color='tab:blue')
  plt.bar(season_pattern['season'], season_pattern['casual'], label='Casual', color='tab:purple')
  plt.xlabel(None)
  plt.ylabel(None)
  plt.title('Jumlah Penyewa Sepeda Berdasarkan Musim')
  plt.legend()
  st.pyplot(fig)
else:
  st.write("Tidak ada data yang ditemukan untuk rentang tanggal yang dipilih.")

#Conclusion
st.header("Conclusion")

##Pertanyaan 1
st.subheader("Pertanyaan 1: Bagaimana perbandingan tren jumlah pengguna sepeda di tahun 2011 dan 2012?")
st.text("Tren penyewaan sepeda pengalami peningkatan dari tahun 2011 ke tahun 2012. Peningkatan tersebut dimulai pada bulan Mei hingga September dan terjadi penurunan pada akhir dan awal tahun.")

##Pertanyaan 2
st.subheader("Bagaimana pola perbandingan penyewaan sepeda harian?")
st.text("Jumlah penyewaan sepeda cenderung meningkat secara bertahap sepanjang hari kerja (dari hari Senin hingga Jumat) dengan puncaknya pada hari Jumat. Kemudian, jumlah penyewaan sepeda mengalami penurun pada akhir pekan (hari Minggu). Hal ini mengindikasikan bahwa sepeda lebih sering digunakan untuk kegiatan rutin sehari-hari seperti pergi bekerja atau sekolah, dibandingkan untuk rekreasi pada hari libur.")

##Pertanyaan 3
st.subheader("Pertanyaan 3: Bagaimana pengaruh musim terhadap jumlah penyewaan sepeda?")
st.text("Jumlah penyewaan sepeda mengalami kenaikan secara bertahap seiring pergantian musim. Pada musim semi tercatat angka penyewaan terendah, sementara musim panas dan gugur menjadi puncak popularitas bersepeda. Setelah itu, terjadi sedikit penurunan jumlah penyewaan di musim dingin.")
