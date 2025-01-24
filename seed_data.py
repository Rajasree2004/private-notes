from init import Base, engine, SessionLocal
from model import Note

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    sample_note = Note(code="SAMPLE01", content="VGhpcyBpcyBhIHNhbXBsZSBub3RlLi4u")  # Pre-encrypted content
    db.add(sample_note)
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    seed_data()
