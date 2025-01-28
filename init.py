import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet

# Fetch the database URL from environment variables (defaults to SQLite for local development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notes.db")

# Setup database engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base for models
Base = declarative_base()

# Fetch the encryption key from environment variables
KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())  # Default to a generated key if not set
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
