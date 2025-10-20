import os
import uuid
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

from werkzeug.utils import secure_filename, send_file

from encryptor import encrypt_text, decrypt_text, decrypt_file, load_key

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads/"
app.config['ENCRYPTED_FOLDER'] = "uploads/encrypted/"
app.config['DECRYPTED_FOLDER'] = "uploads/decrypted/"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCRYPTED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECRYPTED_FOLDER'], exist_ok=True)


app.secret_key = "geheim"

load_key()

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "POST":
        text = request.form['text']
        print("tekst te encrypten:", text)
        encypted_text = encrypt_text(text)
        print("Encrypted text:", encypted_text)
        return render_template('encrypt.html', encrypted_text=encypted_text)
    return render_template('encrypt.html')

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        text = request.form['text']
        print("tekst te decrypten:", text)
        decrypted_text = decrypt_text(text)
        print("Decrypted text:", decrypted_text)
        return render_template('decrypt.html', decrypted_text=decrypted_text)
    return render_template('decrypt.html')

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if not file:
            return "Geen bestand geupload", 400

    #slaat het bestand tijdelijk op
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(temp_path)
    return "Bestand succesvol geupload", 200

    #versleutelen van het bestand
    encrypted_path = encrypt_file(temp_path)
    file_id = str(uuid.uuid4())
    new_name = os.path.join(app.config['ENCRYPTED_FOLDER'], file_id + ".enc")
    os.rename(encrypted_path, new_name)

    os.remove(temp_path)

    link= url_for('download', file_id=file_id, _external=True)
    return f"Bestand succesvol geupload. Download link: {link}", 200

@app.route("/download/<file_id>")
def download(file_id):
    encrypted_path = os.path.join(app.config['ENCRYPTED_FOLDER'], file_id + ".enc")
    if not os.path.exists(encrypted_path):
        return "Bestand niet gevonden", 404

    decrypted_path = decrypt_file(encrypted_path)
    return send_file(decrypted_path, as_attachment=True)











# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         ##user = get_username(username)
#
#         if user:
#             print("Wachtwoord in database ", user.password)
#             print("Wachtwoord ingevoerd", password)
#             #print("Hash matching", check_password_hash(user.password, password))
#
#         if user and check_password_hash(user.password, password):
#             #login_user(user)
#             flash("Ingelogd als " + user.username)
#             print("Ingelogd als " + user.username)
#
#             return redirect(url_for('get_students'))
#
#         else:
#             flash("Fout gebruikersnaam of wachtwoord")
#             print("Ingevulde gebruikersnaam:", username)
#             print("Opgehaalde gebruiker:", user)
#
#             return redirect(url_for('login'))
#
#     return render_template('login.html')






if __name__ == '__main__':
    app.run(debug=True)