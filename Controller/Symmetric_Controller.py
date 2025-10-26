import os

from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename


def key_generator():

    # Genereerd een symetrische sleutel (AES-256)
    key = Fernet.generate_key()
    with open("../secret.key", "wb") as key_file:
        key_file.write(key)
    print("Sleutel gegenereerd en opgeslagen")
    return key


def load_key():
    if not os.path.exists("../secret.key"):
        print("Sleutel niet gevonden, nieuwe sleutel is aan het genereren...")
        return key_generator()

    with open("../secret.key", "rb") as key_file:
        key = key_file.read()

    if len(key) != 44:
        print("key is sussy, nieuwe sleutel aan het genereren...........")

        return key_generator()
    return key


def encrypt_text(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_text(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message


