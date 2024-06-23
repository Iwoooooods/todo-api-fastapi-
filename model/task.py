from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=True)
    updated_at = Column(DateTime, default=None, onupdate=func.current_timestamp(), nullable=True)
    title = Column(String(255), nullable=False)
    brief = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=True)
    deadline = Column(DateTime, nullable=True)
    user_id = Column(BigInteger, nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, user_id={self.user_id})>"
