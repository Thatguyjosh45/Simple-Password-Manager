from argon2 import PasswordHasher
import os

HASH_FILE = "data/master_hash.txt"
ph = PasswordHasher()

# Set or verify the master password
def set_master_password(password: str):
    hashed_password = ph.hash(password)
    with open(HASH_FILE, "w") as f:
        f.write(hashed_password)
    print("✅ Master password set successfully!")

def verify_master_password(password: str):
    if not os.path.exists(HASH_FILE):
        print("❌ No master password found. Set it using: python src/main.py set-master --master NEWPASSWORD")
        return False
    
    with open(HASH_FILE, "r") as f:
        stored_hash = f.read().strip()
    
    try:
        ph.verify(stored_hash, password)
        return True
    except:
        print("❌ Incorrect master password!")
        return False
