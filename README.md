# Aplikasi Steganografi J-Steg berbasis Web

Sebuah aplikasi web sederhana yang dibangun dengan Python dan Flask untuk menyisipkan (encode) dan mengekstrak (decode) pesan rahasia dari gambar JPEG. Aplikasi ini secara spesifik mengimplementasikan algoritma steganografi **J-Steg**, yang bekerja pada domain frekuensi gambar (koefisien DCT).

Aplikasi ini dirancang untuk menjadi ringan dan kompatibel dengan platform hosting modern yang menggunakan *ephemeral filesystem* (penyimpanan non-permanen) dengan memproses semua gambar sepenuhnya di dalam memori.

---

## Tampilan Aplikasi (Screenshot)
Berikut adalah tampilan antarmuka utama aplikasi, yang terbagi menjadi dua tab utama untuk proses encode dan decode.

![image](https://github.com/user-attachments/assets/9a3642c6-f844-4c7b-ae94-1f4d47b571d7)
![image](https://github.com/user-attachments/assets/f734f2f0-4036-4334-a580-55fcff94fe56)
![image](https://github.com/user-attachments/assets/768373c7-beb3-450e-9053-0808e8f98b97)

## Fitur Utama
- **Encode**: Menyisipkan pesan teks ke dalam gambar JPEG.
- **Decode**: Mengekstrak pesan teks dari gambar stego JPEG.
- **Algoritma J-Steg**: Implementasi murni algoritma J-Steg yang memodifikasi LSB dari koefisien DCT, dengan mengabaikan koefisien bernilai 0 dan 1.
- **Proteksi Password**: Pesan dapat dilindungi dengan password opsional untuk lapisan keamanan tambahan (obfuscation).
- **Validasi Password**: Sistem dapat mendeteksi jika password yang dimasukkan salah atau jika password digunakan pada gambar yang tidak terproteksi.
- **Tampilan Biner**: Menampilkan data biner mentah yang diekstrak dari gambar, sangat berguna untuk analisis dan edukasi.
- **Proses In-Memory**: Tidak ada file gambar yang disimpan di server, semuanya diproses di memori. Cocok untuk platform hosting seperti Render, Heroku, dll.
- **Antarmuka Responsif**: Tampilan yang bersih dan mudah digunakan berkat Bootstrap 5.

## Teknologi yang Digunakan
- **Backend**: Python 3
- **Framework**: Flask
- **Manipulasi Gambar & Algoritma**: `jpegio`, `numpy`
- **Server Produksi (Rekomendasi)**: Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

## Konsep Algoritma J-Steg
Berbeda dengan steganografi LSB pada umumnya yang bekerja pada level piksel, J-Steg bekerja setelah gambar melalui proses *Discrete Cosine Transform* (DCT) saat kompresi JPEG.
1.  Gambar dipecah menjadi blok 8x8 piksel dan ditransformasi ke domain frekuensi (koefisien DCT).
2.  Data pesan disisipkan dengan memodifikasi *Least Significant Bit* (LSB) dari koefisien DCT yang sudah terkuantisasi.
3.  Untuk meminimalkan deteksi, J-Steg secara spesifik **tidak akan mengubah** koefisien yang bernilai `0` atau `1`.

## Struktur Proyek
```
/proyek-jsteg
├── app.py              # Logika web aplikasi Flask (routing, request handling)
├── jsteg.py            # Modul inti berisi implementasi algoritma J-Steg
├── requirements.txt    # Daftar dependensi Python
├── tmp_results/        # Folder untuk hasil decode sementara (mencegah cookie besar)
└── templates/
    └── index.html      # File antarmuka web (frontend)
```

## Instalasi & Menjalankan Secara Lokal
Untuk menjalankan aplikasi ini di komputer Anda, ikuti langkah-langkah berikut:

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username/repository-anda.git](https://github.com/username/repository-anda.git)
    cd proyek-jsteg
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    ```bash
    # Membuat venv
    python -m venv venv

    # Mengaktifkan di Windows
    venv\Scripts\activate

    # Mengaktifkan di MacOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependensi**
    Pastikan Anda memiliki `requirements.txt` lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Buat Folder Temporer**
    Aplikasi ini memerlukan folder `tmp_results` untuk berjalan dengan benar.
    ```bash
    mkdir tmp_results
    ```

5.  **Jalankan Aplikasi**
    ```bash
    flask run
    ```

6.  Buka browser dan akses alamat `http://127.0.0.1:5000`.

## Cara Menggunakan
1.  **Sisipkan Pesan (Encode)**
    - Buka tab "Sisipkan Pesan (Encode)".
    - Pilih gambar JPEG yang ingin Anda gunakan.
    - Ketik pesan rahasia Anda di dalam textarea.
    - (Opsional) Masukkan password untuk proteksi.
    - Klik tombol "Sisipkan Pesan". File gambar stego akan otomatis terunduh.

2.  **Ekstrak Pesan (Decode)**
    - Buka tab "Ekstrak Pesan (Decode)".
    - Pilih gambar stego JPEG yang ingin Anda ekstrak pesannya.
    - Jika gambar tersebut diproteksi, masukkan password yang benar.
    - Klik tombol "Ekstrak Pesan".
    - Jika berhasil, pesan yang ditemukan akan ditampilkan beserta data binernya. Jika gagal (misal: password salah), pesan error yang informatif akan muncul.

