# decoder.py
import jpegio as jio

def bits_to_str(bits):
    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b+8]
        if len(byte) < 8:
            break
        char = chr(int("".join(map(str, byte)), 2))
        if char == '\x00':
            break
        chars.append(char)
    return ''.join(chars)

def extract_bits_from_image(img_path):
    jpg = jio.read(img_path)
    coeffs = jpg.coef_arrays[0]
    bits = []

    h, w = coeffs.shape
    for y in range(h):
        for x in range(w):
            coef = coeffs[y, x]
            if coef == 0 or abs(coef) == 1:
                continue
            bits.append(coef & 1)
    return bits

def extract_jsteg(img_path):
    bits = extract_bits_from_image(img_path)
    return bits_to_str(bits)
