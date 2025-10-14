from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

from encryptor import encrypt_text, decrypt_text

app = Flask(__name__)

app.secret_key = "geheim"

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method() == "POST":
        text = request.form['text']
        print("tekst te encrypten:", text)
        encypted_text = encrypt_text(text)
        print("Encrypted text:", encypted_text)
        return render_template('encrypt.html', encrypted_text=encypted_text)
    return render_template('encrypt.html')

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method() == "POST":
        text = request.form['text']
        print("tekst te decrypten:", text)
        decrypted_text = decrypt_text(text)
        print("Decrypted text:", decrypted_text)
        return render_template('decrypt.html', decrypted_text=decrypted_text)
    return render_template('decrypt.html')










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