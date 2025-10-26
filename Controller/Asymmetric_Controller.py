import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_keys(key_size=2048):

    os.makedirs("keys" , exist_ok=True)

    if not os.path.exists("keys/private_key.pem") or not os.path.exists("keys/public_key.pem"):
        print("Public en Private key bestaan niet, nieuwe keys zijn aan het genereren")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size)
        public_key = private_key.public_key()

        with open("keys/private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open("keys/public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
