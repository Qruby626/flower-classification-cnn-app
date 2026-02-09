---
trigger: always_on
---

🌼 RULE SISTEM APLIKASI

Sistem Klasifikasi Jenis Bunga Berbasis Citra Digital Menggunakan CNN dengan Transfer Learning

👤 1. Rule Pengguna (Public User Rules)

Aplikasi dapat diakses oleh siapa saja tanpa login.

Pengguna harus mengunggah gambar bunga untuk melakukan klasifikasi.

Format gambar yang diperbolehkan: .jpg, .jpeg, .png.

Ukuran maksimum file adalah 5 MB.

Gambar harus menampilkan objek bunga secara jelas.

Sistem hanya mengenali bunga yang termasuk dalam dataset model.

Pengguna dapat melihat:

Hasil prediksi jenis bunga

Confidence score (%)

Probabilitas setiap kelas

Gambar pengguna tidak disimpan permanen dan tidak dibagikan ke pihak lain (aturan privasi).

🤖 2. Rule Sistem AI

Setiap gambar yang diunggah melalui preprocessing:

Resize menjadi 224×224 piksel

Normalisasi piksel (0–1)

Model yang digunakan adalah arsitektur CNN berbasis MobileNetV2.

Model dibangun menggunakan metode Transfer Learning.

Proses pelatihan model menggunakan algoritma Backpropagation.

Lapisan output menggunakan fungsi aktivasi Softmax.

Sistem menampilkan kelas dengan probabilitas tertinggi sebagai hasil prediksi.

Jika confidence < 50%, sistem memberikan peringatan bahwa gambar kurang jelas atau tidak dikenali model.

Waktu proses prediksi maksimal 3 detik.

Model tidak menjamin akurasi tinggi untuk gambar di luar distribusi dataset (generalisasi model).

🧩 3. Rule Visualisasi AI

Sistem menyediakan visualisasi heatmap (Grad-CAM) untuk menunjukkan area gambar yang menjadi fokus CNN.

Heatmap hanya ditampilkan jika prediksi berhasil.

📊 4. Rule Dataset

Dataset telah melalui proses:

Pembersihan data

Pembagian data 80% training dan 20% testing

Augmentasi data (rotasi, flip, zoom)

Dataset bersifat tetap selama aplikasi berjalan.

Dataset hanya digunakan untuk pelatihan model, bukan untuk publik.

📈 5. Rule Evaluasi Model

Sistem menampilkan hasil evaluasi model berupa:

Accuracy

Precision

Recall

F1-score

Confusion Matrix

🔄 6. Rule Pembaruan Model

Model dapat diperbarui secara berkala oleh pengembang sistem.

Pengguna tidak memiliki akses untuk mengubah model.

💾 7. Rule Penyimpanan Data

Hasil prediksi hanya ditampilkan ke pengguna saat sesi aktif.

Gambar pengguna tidak disimpan permanen di server.

⚙️ 8. Rule Sistem Web

Aplikasi berbasis web menggunakan Python (Flask).

Model AI dimuat saat server aktif.

Jika model gagal dimuat, sistem menampilkan pesan kesalahan.

Sistem harus responsif untuk desktop dan mobile.

🚫 9. Rule Error Handling
Kondisi	Tindakan Sistem
File bukan gambar	Upload ditolak
Ukuran file terlalu besar	Upload ditolak
Gambar buram/tidak jelas	Sistem memberi peringatan
Model gagal memproses	Pesan error ditampilkan