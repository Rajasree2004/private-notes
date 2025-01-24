# init.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize the database URL (SQLite in-memory database for simplicity)
DATABASE_URL = "sqlite:///./notes.db"

# Setup database engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base for models
Base = declarative_base()

# Encryption setup (this should be securely stored in production)
from cryptography.fernet import Fernet
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Utility functions
def generate_code(length=8):
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def encrypt_content(content):
    return cipher.encrypt(content.encode()).decode()

def decrypt_content(encrypted_content):
    from cryptography.fernet import InvalidToken
    try:
        return cipher.decrypt(encrypted_content.encode()).decode()
    except InvalidToken:
        return None
