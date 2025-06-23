import streamlit as st
from steg.encoder import embed_jsteg, str_to_bits
from steg.decoder import extract_bits_from_image, bits_to_str
import os

# Konfigurasi awal
st.set_page_config(page_title="J-STEG Steganografi", page_icon="🖼️")
st.title("🖼️ J-STEG Steganografi")

# Gunakan folder output terpisah
OUTPUT_DIR = "stego_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== Sidebar =====
with st.sidebar:
    st.markdown("## Apa itu J-STEG❓❓")
    st.markdown(
        """
        **J-STEG** (JPEG Steganography) adalah teknik penyisipan pesan rahasia ke dalam gambar **JPEG** dengan cara memodifikasi **bit LSB** dari koefisien DCT yang tidak nol dan bukan ±1.

        Bit pesan disisipkan secara tersembunyi tanpa mengubah tampilan gambar.

        ---
        """
    )
    menu = st.radio("📂 Pilih Mode", ["🔐 Encode", "🔎 Decode"])

# =======================================
#                ENCODE
# =======================================
if menu == "🔐 Encode":
    st.header("🔐 Encode - Sisipkan Pesan ke Gambar JPEG")

    uploaded = st.file_uploader("Unggah Gambar JPEG", type=["jpg", "jpeg"])
    message_to_embed = st.text_area(
        "Masukkan Pesan Rahasia (maks 500 karakter)",
        max_chars=500,
        help="Ketik pesan yang ingin Anda sembunyikan. Maksimum 500 karakter.",
        placeholder="Contoh: Ini adalah pesan rahasia saya!"
    )
    encode_btn = st.button("🔧 Encode Gambar")

    if uploaded and message and encode_btn:
        if len(message) > 500:
            st.error("⚠️ Pesan terlalu panjang. Maksimum 500 karakter.")
        else:
            original_path = os.path.join(OUTPUT_DIR, "original.jpg")
            with open(original_path, "wb") as f:
                f.write(uploaded.read())

            try:
                bits = str_to_bits(message) + [0]*8
                bit_str = ''.join(map(str, bits))
                stego_path = os.path.join(OUTPUT_DIR, "encoded.jpg")
                embed_jsteg(original_path, message, out_path=stego_path)

                st.success("✅ Proses encode berhasil!")
                st.markdown("### 🔢 Bit yang Disisipkan:")
                st.caption(f"Total: {len(bits)} bit")
                st.code(bit_str, language="text")

                with open(stego_path, "rb") as f:
                    st.download_button("⬇️ Unduh Gambar Stego", f, file_name="stego.jpg", mime="image/jpeg")

            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat encode: {e}")

    elif encode_btn:
        st.warning("⚠️ Mohon unggah gambar dan isi pesan terlebih dahulu.")

# =======================================
#                DECODE
# =======================================
elif menu == "🔎 Decode":
    st.header("🔎 Decode - Ekstrak Pesan dari Gambar Stego")

    uploaded = st.file_uploader("Unggah Gambar JPEG Hasil Stego", type=["jpg", "jpeg"])
    decode_btn = st.button("🔍 Decode Pesan")

    if uploaded and decode_btn:
        try:
            stego_input = os.path.join(OUTPUT_DIR, "uploaded_stego.jpg")
            with open(stego_input, "wb") as f:
                f.write(uploaded.read())

            bits = extract_bits_from_image(stego_input)

            # Fungsi deteksi null terminator
            def find_null_terminator_index(bits):
                for i in range(0, len(bits), 8):
                    byte = bits[i:i+8]
                    if len(byte) < 8:
                        break
                    if all(b == 0 for b in byte):
                        return i + 8
                return len(bits)

            end_idx = find_null_terminator_index(bits)
            pesan_bits = bits[:end_idx]
            tambahan_bits = bits[end_idx:]

            pesan_bit_str = ''.join(map(str, pesan_bits))
            tambahan_bit_str = ''.join(map(str, tambahan_bits))

            # Tampilkan bit dengan highlight warna
            def chunk_string(s, chunk_size=1000):
                return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]

            # Potong bit menjadi potongan kecil
            highlighted_html = ""
            for chunk in chunk_string(pesan_bit_str):
                highlighted_html += f"<span style='color:limegreen;font-weight:bold'>{chunk}</span>"

            for chunk in chunk_string(tambahan_bit_str):
                highlighted_html += f"<span style='color:gray'>{chunk}</span>"

            message = bits_to_str(bits)

            st.success("✅ Pesan berhasil diekstrak dari gambar!")

            st.markdown("### 📩 Pesan Tersembunyi:")
            st.code(message, language="text")

            st.markdown("### 🔢 Bit yang Ditemukan:")
            st.caption(f"Bit pesan: {len(pesan_bits)} | Total bit dibaca: {len(bits)}")
            st.markdown(highlighted_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat decode: {e}")

    elif decode_btn:
        st.warning("⚠️ Mohon unggah gambar hasil stego terlebih dahulu.")
