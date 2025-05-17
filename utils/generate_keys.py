import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_keys():
    # Create keys directory if it doesn't exist
    keys_dir = "keys"
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir)

    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Save private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(os.path.join(keys_dir, "private_key.pem"), "wb") as f:
        f.write(private_pem)

    # Save public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(os.path.join(keys_dir, "public_key.pem"), "wb") as f:
        f.write(public_pem)

    print("RSA keys generated successfully in the 'keys' directory!")

if __name__ == "__main__":
    generate_rsa_keys() 