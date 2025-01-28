from init import Base, engine, SessionLocal
from models import Note
from sqlalchemy.exc import IntegrityError

def init_db():
    """Initializes the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def seed_data():
    """Seeds the database with initial data."""
    db = SessionLocal()
    try:
        # Check if the note already exists
        existing_note = db.query(Note).filter(Note.code == "SAMPLE01").first()
        if existing_note:
            print("Duplicate entry detected. Updating content...")
            existing_note.content = "VGhpcyBpcyBhIHVwZGF0ZWQgbm90ZS4uLg=="  # Updated content
        else:
            # Add the new note if it doesn't exist
            sample_note = Note(code="SAMPLE01", content="VGhpcyBpcyBhIHNhbXBsZSBub3RlLi4u")  # Pre-encrypted content
            db.add(sample_note)
        db.commit()
    except IntegrityError as e:
        print("IntegrityError occurred:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_data()
