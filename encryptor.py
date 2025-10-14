from cryptography.fernet import Fernet


def key_generator():

    # Genereerd een symetrische sleutel (AES-256)
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Sleutel gegenereerd en opgeslagen")
    return key


def load_key():
    # Laad de symetrische sleutel uit het bestand
    return open("secret.key", "rb").read()

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