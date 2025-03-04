from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64

# Generate a strong encryption key from a master password
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 requires a 32-byte key
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt data using AES-256
def encrypt(password: str, plaintext: str) -> str:
    salt = os.urandom(16)  # Generate a new salt
    key = derive_key(password, salt)
    iv = os.urandom(16)  # Generate a new IV (Initialization Vector)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Padding to ensure data is a multiple of block size
    padding_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + (chr(padding_length) * padding_length)

    ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()
    
    # Encode result as base64 (salt + IV + ciphertext)
    return base64.b64encode(salt + iv + ciphertext).decode()

# Decrypt data using AES-256
def decrypt(password: str, encrypted_data: str) -> str:
    data = base64.b64decode(encrypted_data)
    salt, iv, ciphertext = data[:16], data[16:32], data[32:]
    
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    padding_length = ord(plaintext_padded[-1:])
    return plaintext_padded[:-padding_length].decode()
