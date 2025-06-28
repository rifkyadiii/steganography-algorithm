import jpegio as jio
import numpy as np
import random

def message_to_binary(message):
    """Mengubah pesan string menjadi string biner."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary_string):
    """Mengubah string biner kembali menjadi pesan string."""
    # Pastikan panjang biner kelipatan 8
    if len(binary_string) % 8 != 0:
        padding = 8 - (len(binary_string) % 8)
        binary_string = "0" * padding + binary_string
        
    byte_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    message = ""
    for byte in byte_list:
        try:
            # Coba konversi, jika ada karakter non-printable, abaikan
            char = chr(int(byte, 2))
            if char.isprintable() or char in ['\n', '\r', '\t']:
                 message += char
        except ValueError:
            # Jika ada byte yang tidak valid (misal, dari sisa data gambar)
            pass
    return message

def get_embeddable_coeffs(dct_coeffs):
    """Mendapatkan daftar koefisien yang bisa disisipi data (bukan 0 atau 1)."""
    embeddable_coeffs = []
    # Iterasi melalui semua komponen warna (Y, Cb, Cr)
    for i in range(len(dct_coeffs)):
        # Iterasi melalui setiap blok 8x8
        for j in range(dct_coeffs[i].shape[0]):
            for k in range(dct_coeffs[i].shape[1]):
                if dct_coeffs[i][j, k] not in [0, 1]:
                    embeddable_coeffs.append((i, j, k))
    return embeddable_coeffs

def encode(image_path, message, password=None):
    """Menyisipkan pesan ke dalam gambar JPEG menggunakan J-Steg."""
    jpeg = jio.read(image_path)
    dct_coeffs = jpeg.coef_arrays

    # Kapasitas maksimum dalam bit
    available_coeffs = get_embeddable_coeffs(dct_coeffs)
    capacity = len(available_coeffs)

    # Tambahkan delimiter unik untuk menandai akhir pesan
    message += "<-END->"
    binary_message = message_to_binary(message)
    
    if len(binary_message) > capacity:
        raise ValueError(f"Pesan terlalu panjang. Kapasitas: {capacity} bit, Pesan: {len(binary_message)} bit.")

    # Gunakan password untuk mengacak urutan koefisien
    if password:
        random.seed(password)
        random.shuffle(available_coeffs)

    # Sisipkan bit pesan ke LSB koefisien
    for i, bit in enumerate(binary_message):
        idx = available_coeffs[i] # Dapatkan index koefisien (i, j, k)
        coeff_val = dct_coeffs[idx[0]][idx[1], idx[2]]
        
        # Ubah LSB
        if int(bit) == 1:
            dct_coeffs[idx[0]][idx[1], idx[2]] = coeff_val | 1
        else:
            dct_coeffs[idx[0]][idx[1], idx[2]] = coeff_val & ~1

    return jpeg, binary_message

def decode(image_path, password=None):
    """Mengekstrak pesan dari gambar JPEG."""
    jpeg = jio.read(image_path)
    dct_coeffs = jpeg.coef_arrays
    
    available_coeffs = get_embeddable_coeffs(dct_coeffs)

    if password:
        random.seed(password)
        random.shuffle(available_coeffs)

    binary_extracted_full = ""
    delimiter = message_to_binary("<-END->")
    
    for idx in available_coeffs:
        coeff_val = dct_coeffs[idx[0]][idx[1], idx[2]]
        lsb = coeff_val & 1
        binary_extracted_full += str(lsb)
        
        if binary_extracted_full.endswith(delimiter):
            break
    
    # Pisahkan biner pesan dari biner keseluruhan (termasuk delimiter)
    binary_message_part = binary_extracted_full[:-len(delimiter)]
    
    message = binary_to_message(binary_message_part)

    # Kembalikan 3 nilai untuk ditampilkan di UI
    return message, binary_message_part, binary_extracted_full