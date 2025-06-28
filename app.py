# app.py

import os
# --- PERUBAHAN DI SINI ---
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from werkzeug.utils import secure_filename
import jsteg
import jpegio as jio

# Konfigurasi Flask
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'super-secret-key-change-me' 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    results = {
        'active_tab': session.pop('active_tab', 'encode'),
        'success_encode': session.pop('success_encode', False),
        'encoded_image': session.pop('encoded_image', None),
        'binary_before': session.pop('binary_before', None),
        'error_encode': session.pop('error_encode', None),
        'success_decode': session.pop('success_decode', False),
        'decoded_message': session.pop('decoded_message', None),
        'binary_message_part': session.pop('binary_message_part', None),
        'binary_extracted_full': session.pop('binary_extracted_full', None),
        'error_decode': session.pop('error_decode', None)
    }
    return render_template('index.html', **results)

@app.route('/encode', methods=['POST'])
def encode_route():
    session['active_tab'] = 'encode'

    if 'image' not in request.files or 'message' not in request.form:
        session['error_encode'] = "Form tidak lengkap!"
        return redirect(url_for('index'))
    
    file = request.files['image']
    message = request.form['message']
    password = request.form.get('password')

    if file.filename == '':
        session['error_encode'] = "Tidak ada gambar yang dipilih!"
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        try:
            binary_before_message = jsteg.message_to_binary(message)
            stego_jpeg, _ = jsteg.encode(input_path, message, password)
            
            output_filename = 'stego_' + filename
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            jio.write(stego_jpeg, output_path)
            
            session['success_encode'] = True
            session['encoded_image'] = output_filename
            session['binary_before'] = binary_before_message
            return redirect(url_for('index'))

        except Exception as e:
            session['error_encode'] = f"Terjadi kesalahan: {e}"
            return redirect(url_for('index'))
    
    session['error_encode'] = "Format file tidak didukung. Gunakan .jpg atau .jpeg."
    return redirect(url_for('index'))

@app.route('/decode', methods=['POST'])
def decode_route():
    session['active_tab'] = 'decode'

    if 'image' not in request.files:
        session['error_decode'] = "Tidak ada gambar yang dipilih!"
        return redirect(url_for('index'))
    
    file = request.files['image']
    password = request.form.get('password_decode')

    if file.filename == '':
        session['error_decode'] = "Tidak ada gambar yang dipilih!"
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        try:
            decoded_message, binary_message_part, binary_extracted_full = jsteg.decode(input_path, password)
            
            if not decoded_message:
                session['error_decode'] = "Tidak ada pesan tersembunyi yang ditemukan atau password salah."
                return redirect(url_for('index'))

            session['success_decode'] = True
            session['decoded_message'] = decoded_message
            session['binary_message_part'] = binary_message_part
            session['binary_extracted_full'] = binary_extracted_full
            return redirect(url_for('index'))

        except Exception as e:
            session['error_decode'] = f"Gagal mendekode: {e}"
            return redirect(url_for('index'))

    session['error_decode'] = "Format file tidak didukung."
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)