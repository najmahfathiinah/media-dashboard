# 🥤 GenZ Drink Media Intelligence Dashboard

Selamat datang di repositori Proyek Media Intelligence Dashboard. Ini adalah aplikasi web interaktif yang dirancang untuk para profesional media, dibangun untuk mengubah data mentah dari kampanye media sosial menjadi _insight_ strategis yang dapat ditindaklanjuti.

Aplikasi ini dikembangkan sebagai solusi untuk studi kasus analisis produk minuman yang menargetkan audiens Gen Z, menggantikan analisis manual yang lambat dengan _dashboard_ dinamis yang ditenagai oleh AI.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://1najmahfathiinahr2306164746.streamlit.app/)

### **[➡️ Kunjungi Live Demo Aplikasi di Sini](https://1najmahfathiinahr2306164746.streamlit.app/)**

## Tampilan Dashboard
*(Disarankan untuk menambahkan screenshot dari dashboard Anda yang sudah jadi di sini)*

![Screenshot Dashboard](URL_SCREENSHOT_ANDA)

## ✨ Fitur Utama
- **Upload Data Dinamis:** Memungkinkan pengguna mengunggah dataset CSV mereka sendiri untuk dianalisis secara _real-time_.
- **Preprocessing Otomatis:** Sistem secara cerdas membersihkan data, menstandarisasi nama kolom, dan menangani nilai yang hilang untuk memastikan kualitas data.
- **Filter Komprehensif:** Data dapat difilter secara interaktif berdasarkan rentang tanggal, platform, dan tipe media.
- **KPI Dashboard:** Menampilkan metrik performa utama seperti Total Postingan, Total Engagement, Rata-rata Engagement, dan persentase Sentimen Positif.
- **5 Visualisasi Interaktif:** Disajikan dalam format tab yang rapi, berisi 5 grafik Plotly untuk analisis mendalam:
  1.  **Distribusi Sentimen:** Memahami persepsi publik (Positif, Netral, Negatif).
  2.  **Tren Engagement:** Melacak fluktuasi engagement dari waktu ke waktu.
  3.  **Performa Platform:** Membandingkan platform mana yang paling efektif.
  4.  **Proporsi Tipe Media:** Menganalisis format konten yang paling dominan.
  5.  **Top 5 Lokasi:** Mengidentifikasi area geografis dengan engagement tertinggi.
- **Integrasi Multi-Model AI:** Pengguna dapat memilih antara model **Google Gemini** atau **GPT-3.5 (via OpenRouter)** untuk mendapatkan _insight_ naratif otomatis pada setiap grafik.
- **Rekomendasi Strategis:** Fitur untuk menghasilkan rekomendasi kampanye yang dapat ditindaklanjuti berdasarkan keseluruhan data yang ditampilkan.

## 🛠️ Teknologi & Tools yang Digunakan
- **Bahasa**: Python
- **Framework Aplikasi**: Streamlit
- **Analisis Data**: Pandas, NumPy
- **Visualisasi Data**: Plotly
- **Integrasi AI**: Google Gemini API, OpenRouter AI
- **Deployment**: Streamlit Community Cloud & GitHub

## 🚀 Cara Menjalankan Secara Lokal

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/najmahfathiinah/media-dashboard.git](https://github.com/najmahfathiinah/media-dashboard.git)
    cd media-dashboard
    ```
2.  **Install Dependencies:**
    Pastikan Anda memiliki file `requirements.txt` di dalam folder Anda.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Siapkan API Keys:**
    Aplikasi ini memerlukan API Key untuk fitur AI. Masukkan kunci Anda di sidebar saat aplikasi berjalan.
    - [Dapatkan Google API Key](https://aistudio.google.com/app/apikey)
    - [Dapatkan OpenRouter API Key](https://openrouter.ai/keys)
4.  **Jalankan Aplikasi:**
    ```bash
    streamlit run media_ai_dashboard.py
    ```

## 📂 Struktur File Proyek
```
.
├── .streamlit/
│   └── config.toml      # File konfigurasi untuk tema terang/gelap
├── media_ai_dashboard.py # Skrip utama aplikasi Streamlit
├── Spirifi.csv          # Dataset default
├── requirements.txt     # Daftar library Python yang dibutuhkan
└── README.md            # File dokumentasi ini
```
---
*Proyek ini merupakan implementasi dari studi kasus untuk membangun
