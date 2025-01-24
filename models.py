from sqlalchemy import Column, String
from init import Base

# Database Model for Notes
class Note(Base):
    __tablename__ = 'notes'
    code = Column(String, primary_key=True, index=True)
    content = Column(String)
