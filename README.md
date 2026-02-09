---
title: Flower Classification Cnn App
emoji: 🌸
colorFrom: pink
colorTo: red
sdk: docker
pinned: false
---

# 🌸 Flower Classification System CNN

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Qruby626/flower-classification)

Sistem Klasifikasi Jenis Bunga Berbasis Citra Digital Menggunakan CNN dengan Transfer Learning (MobileNetV2).

## 📋 Deskripsi Proyek

Aplikasi ini adalah sistem berbasis web yang dibangun menggunakan Flask untuk mengklasifikasikan jenis bunga berdasarkan gambar yang diunggah pengguna. Model AI dilatih menggunakan arsitektur MobileNetV2 dengan metode Transfer Learning.

### Fitur Utama

- **Klasifikasi Citra**: Mengidentifikasi jenis bunga dari gambar yang diunggah.
- **Confidence Score**: Menampilkan tingkat keyakinan model terhadap prediksi.
- **Visualisasi Heatmap (Grad-CAM)**: Menunjukkan area fokus model pada gambar.
- **Riwayat Prediksi**: Menyimpan riwayat prediksi selama sesi aktif.
- **Evaluasi Model**: Menampilkan metrik performa model (Akurasi, Presisi, Recall, F1-Score).

## 🚀 Cara Menjalankan Aplikasi

### Prasyarat

- Python 3.8 - 3.10
- Git

### Instalasi

1.  **Clone Repository**

    ```bash
    git clone https://github.com/Qruby626/flower-classification-cnn-app.git
    cd flower-cnn-app
    ```

2.  **Buat Virtual Environment (Opsional tapi Direkomendasikan)**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi**

    ```bash
    python app.py
    ```

5.  **Buka di Browser**

    Akses aplikasi di `http://127.0.0.1:5000`

## 📂 Struktur Folder

```
flower-cnn-app/
├── app.py              # File utama aplikasi Flask
├── model_utils.py      # Utilitas untuk memuat dan menggunakan model
├── visualization.py    # Utilitas untuk Grad-CAM
├── history_utils.py    # Manajemen riwayat prediksi
├── verify_history.py   # Script verifikasi history (dev)
├── requirements.txt    # Daftar library yang dibutuhkan
├── model/              # Folder penyimpanan model (.keras)
├── static/             # File statis (CSS, JS, gambar upload)
├── templates/          # Template HTML (Jinja2)
└── data/               # Folder data (jika ada)
```

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python, Flask
- **AI/ML**: TensorFlow, Keras, MobileNetV2
- **Frontend**: HTML, CSS (Vanilla), JavaScript
- **Pengolahan Citra**: OpenCV, Pillow, NumPy

## 📝 Aturan Sistem

- **Format Gambar**: .jpg, .jpeg, .png
- **Ukuran Maksimal**: 5 MB
- **Dimensi Input Model**: 224x224 piksel
- **Privasi**: Gambar pengguna tidak disimpan permanen.

## 👥 Kontributor

- [Qruby626](https://github.com/Qruby626)

---
*Dikembangkan untuk Tugas Akhir Semester Mata Kuliah Neuro Computing.*
