import os

from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename


def key_generator():

    # Genereerd een symetrische sleutel (AES-256)
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Sleutel gegenereerd en opgeslagen")
    return key


def load_key():
    if not os.path.exists("secret.key"):
        print("Sleutel niet gevonden, nieuwe sleutel is aan het genereren...")
        return key_generator()

    with open("secret.key", "rb") as key_file:
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


def encrypt_file(file_path):
    key = load_key()
    f =Fernet(key)

    with open(file_path, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    filename = secure_filename(os.path.basename(file_path))
    encrypted_file_path = os.path.join("uploads/encrypted/", filename + ".enc")
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    print("Bestand versleuteld en opgeslagen als:", encrypted_file_path)
    return encrypted_file_path


def decrypt_file(encrypted_file_path):
    key = load_key()
    f = Fernet(key)

    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = f.decrypt(encrypted_data)
    filename = os.path.basename(encrypted_file_path).replace(".enc", "")
    decrypted_file_path = os.path.join("uploads/decrypted/", filename)

    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    print("bestand ontsleuteld en opgeslagen als:", decrypted_file_path)
    return decrypted_file_path


