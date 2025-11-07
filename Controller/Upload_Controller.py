import hashlib
import os

from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename

from Controller.Symmetric_Controller import load_key

base_dir = os.path.abspath(os.path.dirname(__file__) + "/..")
upload_dir = os.path.join(base_dir, "uploads")
encrypted_dir = os.path.join(upload_dir, "encrypted")
decrypted_dir = os.path.join(upload_dir, "decrypted")


# het encrypten van de file
def encrypt_file(file_path):
    key = load_key()
    f =Fernet(key)

    with open(file_path, "rb") as file:
        file_data = file.read()

    #checksum implementeren
    checksum = hashlib.sha256(file_data).hexdigest()
    encrypted_data = f.encrypt(file_data)

    filename = secure_filename(os.path.basename(file_path))
    encrypted_file_path = os.path.join(encrypted_dir, filename + ".enc")
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    print("Bestand versleuteld en opgeslagen als:", encrypted_file_path)
    print("Checken en de sum is" , checksum)
    return encrypted_file_path , checksum

    #het decrypten van de file
def decrypt_file(encrypted_file_path):
    key = load_key()
    f = Fernet(key)

    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = f.decrypt(encrypted_data)
    filename = os.path.basename(encrypted_file_path).replace(".enc", "")
    decrypted_file_path = os.path.join(decrypted_dir , filename)

    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    print("bestand ontsleuteld en opgeslagen als:", decrypted_file_path)
    return decrypted_file_path

    
def checksum(file_path):

    hash= hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunks in iter(lambda: f.read(4096), b""):
            hash.update(chunks)
    return hash.hexdigest()



