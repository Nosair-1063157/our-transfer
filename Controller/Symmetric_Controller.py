import os

from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename


def key_generator():

    # Genereerd met een symetrische sleutel (AES-256)
    key = Fernet.generate_key()
    with open("../secret.key", "wb") as key_file:
        key_file.write(key)
    print("Sleutel gegenereerd en opgeslagen")
    return key

# deze applicatie volgt het Kerckhoff principle,
# de beveiliging is openbaar maar zolang de key geheim is, is het nogsteeds veilig

def load_key():
    if not os.path.exists("../secret.key"):
        #Als de sleutel niet is gevonden wordt er een nieuwe gegenereerd
        print("Sleutel niet gevonden, nieuwe sleutel is aan het genereren...")
        return key_generator()

    with open("../secret.key", "rb") as key_file:
        key = key_file.read()

    #Er is iets mis het de key, bijvoorbeeld een extra character is meegekomen dan komt er een nieuwe key
    if len(key) != 44:
        print("key is sussy, nieuwe sleutel aan het genereren...........")

        return key_generator()
    return key


#encrypten van tekst
def encrypt_text(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

#het uncrypten van tekst
def decrypt_text(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message


