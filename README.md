# GenZ Drink Media Intelligence Dashboard

Selamat datang di repositori proyek Media Intelligence Dashboard. Aplikasi ini adalah sebuah *tool* interaktif yang dibangun menggunakan Streamlit dan Python untuk menganalisis, memvisualisasikan, dan mendapatkan wawasan dari data performa kampanye media sosial.

**[➡️ Klik di sini untuk mencoba Live Demo](URL_STREAMLIT_APP_ANDA)**

## Tampilan Dashboard
*(Disarankan untuk menambahkan screenshot dari dashboard Anda yang sudah jadi di sini)*

![Screenshot Dashboard](URL_SCREENSHOT_ANDA)

## ✨ Fitur Utama
- **Upload Data Dinamis:** Pengguna dapat mengunggah dataset CSV mereka sendiri untuk dianalisis secara langsung.
- **Preprocessing Otomatis:** Sistem secara cerdas membersihkan data, menstandarisasi nama kolom, dan menangani nilai yang hilang.
- **Filter Komprehensif:** Data dapat difilter secara interaktif berdasarkan rentang tanggal, platform, dan tipe media.
- **KPI Dashboard:** Menampilkan metrik performa utama seperti Total Postingan, Total Engagement, Rata-rata Engagement, dan persentase Sentimen Positif.
- **5 Visualisasi Interaktif:** Dashboard disajikan dalam format tab yang rapi, berisi 5 grafik Plotly untuk analisis mendalam:
  1.  **Distribusi Sentimen:** Memahami persepsi publik (Positif, Netral, Negatif).
  2.  **Tren Engagement:** Melacak fluktuasi engagement dari waktu ke waktu.
  3.  **Performa Platform:** Membandingkan platform mana yang paling efektif.
  4.  **Proporsi Tipe Media:** Menganalisis format konten yang paling dominan.
  5.  **Top 5 Lokasi:** Mengidentifikasi area geografis dengan engagement tertinggi.
- **Download Data:** Fitur untuk mengunduh data yang sudah difilter, laporan ringkasan, dan analisis platform dalam format CSV.

## 🛠️ Teknologi yang Digunakan
- **Python**
- **Streamlit** (Framework Aplikasi Web)
- **Pandas** & **NumPy** (Manipulasi Data)
- **Plotly** (Visualisasi Data Interaktif)
- **GitHub** (Version Control)
- **Streamlit Community Cloud** (Deployment)

## 🚀 Cara Menjalankan Secara Lokal

1.  **Clone Repository:**
    ```bash
    git clone [URL_GITHUB_REPO_ANDA]
    cd [nama-repository]
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Jalankan Aplikasi:**
    ```bash
    streamlit run media_intelligence_dashboard.py
    ```

---
*Proyek ini merupakan implementasi dari studi kasus untuk membangun tool Media Intelligence yang modern dan berbasis data.*
