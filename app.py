import os
import uuid
from datetime import datetime, timedelta

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Flask, render_template, request, url_for

from flask import send_file
from werkzeug.utils import secure_filename

from Controller.Asymmetric_Controller import generate_rsa_keys
from Controller.Symmetric_Controller import encrypt_text, decrypt_text, load_key
from Controller.Upload_Controller import decrypt_file, encrypt_file

app = Flask(__name__)

temporary_links = {}

app.config['UPLOAD_FOLDER'] = "uploads/"
app.config['ENCRYPTED_FOLDER'] = "uploads/encrypted/"
app.config['DECRYPTED_FOLDER'] = "uploads/decrypted/"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCRYPTED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECRYPTED_FOLDER'], exist_ok=True)


app.secret_key = "geheim"

@app.route("/", methods=["GET", "POST"])
def s_encrypt():
    encrypted_text = None
    if request.method == "POST":
        text = request.form['text']
        print("tekst te encrypten:", text)
        encrypted_text = encrypt_text(text)
        print("Encrypted text:", encrypted_text)
        encrypted_text = encrypted_text.decode()
        return render_template('encrypt.html', encrypted_text=encrypted_text)
    return render_template('encrypt.html')

@app.route("/decrypt", methods=["GET", "POST"])
def s_decrypt():
    if request.method == "POST":
        token = request.form['token'].strip()

        try:
            decrypted_text = decrypt_text(token)
            print("Decrypted text:", decrypted_text)
        except Exception as e:
            print("Decryptiefout:", e)

        return render_template("decrypt.html", decrypted_text=decrypted_text)
    return render_template('decrypt.html')

# @app.route("/a_encrypt", methods=["GET", "POST"])
# def a_encrypt():
#     if request_method == "POST":


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if not file:
            return "Geen bestand geupload", 400

    #slaat het bestand tijdelijk op
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(temp_path)


    #versleutelen van het bestand
        encrypted_path, checksum = encrypt_file(temp_path)
        file_id = str(uuid.uuid4())
        new_name = os.path.join(app.config['ENCRYPTED_FOLDER'], file_id + ".enc")
        os.replace(encrypted_path, new_name)

        temporary_links[file_id] = {
            'path': new_name,
            'expires_at': datetime.now() + timedelta(minutes=60)
        }

        try:
            os.remove(temp_path)
        except FileNotFoundError:
            pass
        link= url_for('download', file_id=file_id, _external=True)
        return render_template('upload.html', download_link=link, checksum=checksum)

    return render_template('upload.html', )

@app.route("/a_encrypt", methods=["GET", "POST"])
def a_encrypt():
    encrypted_text = None
    if request.method == "POST":
        text = request.form['text']
        print("tekst te encrypten:", text)
        generate_rsa_keys()

        with open("keys/public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        encrypted_stuff = public_key.encrypt(
            text.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_text = encrypted_stuff.hex()
        print("Encrypted text:", encrypted_text)
        return render_template('a_encrypt.html', encrypted_text=encrypted_text)
    return render_template('a_encrypt.html')

@app.route("/a_decrypt", methods=["GET", "POST"])
def a_decrypt():
    decrypted_text = None
    if request.method == "POST":
        token = request.form['token'].strip()
        print("te decrypten token:", token)
        generate_rsa_keys()

        with open("keys/private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        try:
            decrypted_stuff = private_key.decrypt(
                bytes.fromhex(token),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_text = decrypted_stuff.decode()
            print("Decrypted text:", decrypted_text)
        except Exception as e:
            print("Decryptiefout:", e)
        return render_template("a_decrypt.html", decrypted_text=decrypted_text)
    return render_template('a_decrypt.html')

@app.route("/download/<file_id>")
def download(file_id):

    file = temporary_links.get(file_id)
    if not file:
        return "Woops ongeldige of verlopen link", 404

    if datetime.now() > file['expires_at']:
        del temporary_links[file_id]
        return "Woops de link is verlopen na een uurtje", 403


    encrypted_path = os.path.join(app.config['ENCRYPTED_FOLDER'], file_id + ".enc")
    if not os.path.exists(encrypted_path):
        return "Bestand niet gevonden", 404

    decrypted_path = decrypt_file(encrypted_path)
    return send_file(decrypted_path, as_attachment=True)



if __name__ == '__main__':
    app.run()
    load_key()
    generate_rsa_keys()