import jpegio as jio
import numpy as np

def str_to_bits(s):
    return [int(b) for c in s for b in f"{ord(c):08b}"]

def embed_jsteg(img_path, message, out_path="stego_output/encoded.jpg"):
    jpg = jio.read(img_path)
    coeffs = jpg.coef_arrays[0]
    bits = str_to_bits(message) + [0] * 8  # null terminator

    h, w = coeffs.shape
    bit_index = 0
    for y in range(h):
        for x in range(w):
            val = coeffs[y, x]
            if val == 0 or abs(val) == 1:
                continue
            if bit_index < len(bits):
                coeffs[y, x] = (val & ~1) | bits[bit_index]
                bit_index += 1
            else:
                break
        if bit_index >= len(bits):
            break

    jpg.coef_arrays[0] = coeffs
    jio.write(jpg, out_path)
    return out_path
