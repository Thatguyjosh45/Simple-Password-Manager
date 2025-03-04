import sqlite3
from src.encryption import encrypt, decrypt

DB_FILE = "data/passwords.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Store a new password
def store_password(master_password: str, service: str, username: str, plaintext_password: str):
    encrypted_password = encrypt(master_password, plaintext_password)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",
                   (service, username, encrypted_password))
    conn.commit()
    conn.close()
    print(f"✅ Password saved for {service}")

# Retrieve and decrypt a stored password
def retrieve_password(master_password: str, service: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE service = ?", (service,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        username, encrypted_password = result
        decrypted_password = decrypt(master_password, encrypted_password)
        return f"Service: {service}\nUsername: {username}\nPassword: {decrypted_password}"
    else:
        return "❌ No password found for this service."

# List all stored services
def list_services():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT service FROM passwords")
    services = cursor.fetchall()
    conn.close()
    
    if services:
        return [service[0] for service in services]
    else:
        return []
