# 🔐 Aplikasi Web Steganografi Gambar dengan Algoritma J-STEG

Aplikasi ini dikembangkan menggunakan **Streamlit** untuk melakukan proses steganografi pada gambar JPEG menggunakan algoritma **J-STEG**, yang menyisipkan pesan rahasia ke dalam **koefisien DCT** gambar. Proyek ini merupakan bagian dari tugas **UAS Sistem Multimedia**.

### 🔧 Fitur

* 🔐 **Encode** pesan rahasia ke dalam gambar JPEG
* 🔎 **Decode** pesan dari gambar hasil stego
* 📊 Visualisasi bit pesan dan bit tambahan JPEG
* 📁 Antarmuka pengguna berbasis web (Streamlit)
* ✅ Penjelasan algoritma J-STEG di sidebar
* 📥 Fitur download gambar hasil encode

---

### 📚 Apa itu J-STEG?

> **J-STEG** adalah algoritma steganografi untuk format JPEG yang bekerja dengan menyisipkan bit pesan ke dalam **bit paling tidak signifikan (LSB)** dari koefisien DCT JPEG, **hanya pada nilai yang ≠ 0 dan ≠ ±1**. Karena hanya mengubah bit LSB, gambar hasil stego tampak **sama seperti aslinya** bagi mata manusia.

---

### 🚀 Cara Menjalankan Aplikasi

#### 💻 Secara Lokal (di Komputer Sendiri)

1. **Clone repository** ini:

   ```bash
   git clone https://github.com/rifkyadiii/Steganography_Algorithm.git
   cd jsteg-streamlit
   ```

2. **Install dependensi** (disarankan menggunakan virtual environment):

   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi Streamlit:**

   ```bash
   streamlit run app.py
   ```

4. Buka browser dan akses:

   ```
   http://localhost:8501
   ```

---

#### 🌐 Jalankan Langsung di Streamlit Cloud (tanpa install)

Jika ingin mencoba aplikasi ini **tanpa menginstal apapun**, bisa jalankan langsung secara online melalui **Streamlit Cloud**:

```
https://steganography-uas-sismul.streamlit.app/
```

---

### 📂 Struktur Folder

```
.
├── app.py                  # Aplikasi utama Streamlit
├── steg/
│   ├── encoder.py          # Fungsi untuk encode J-STEG
│   └── decoder.py          # Fungsi untuk decode J-STEG
├── output/           # Folder hasil output encode/decode
├── requirements.txt        # Daftar dependensi Python
└── README.md               # Dokumentasi ini
```

---

### 🧪 Contoh Penggunaan

#### Mode Encode

1. Unggah gambar JPEG milikmu sendiri.
2. Masukkan pesan rahasia (maks. 500 karakter).
3. Klik `🔧 Encode Gambar`.
4. Unduh hasil stego (`stego.jpg`).

#### Mode Decode

1. Unggah gambar hasil stego (`stego.jpg`).
2. Klik `🔍 Decode Pesan`.
3. Lihat bit hasil ekstraksi dan pesan asli yang tersembunyi.

---

### 🛡️ Catatan Penting

* **Jangan kompres ulang** gambar hasil stego sebelum decode (misal: dibuka dan disimpan ulang dengan editor foto).
* Pesan yang disisipkan akan tetap **berada di bagian awal** dari hasil ekstraksi bit.
* Algoritma ini menyisipkan **null terminator (`00000000`)** sebagai tanda akhir pesan.

---

### 👨‍👩‍👧‍👦 Anggota Kelompok

| Nama   | NIM       |
| ------ | --------- |
| Gevira Zahra Shofa | 1227050050 |
| Moch Rifky Aulia Adikusumah | 1227050072 |
| Muhammad Zidan | 1227050079 |
| Muhammad Ahsani Taqwim | 1227050083 |

---

### 📚 Referensi

* Penjelasan algoritma J-STEG: [ResearchGate](https://www.researchgate.net/publication/327161300)
* Dokumentasi pustaka `jpegio`: [https://github.com/dwgoon/jpegio](https://github.com/dwgoon/jpegio)
* Dokumentasi Streamlit: [https://docs.streamlit.io/](https://docs.streamlit.io/)
