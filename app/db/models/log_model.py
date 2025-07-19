from sqlalchemy import Column, Integer, String, Text, DateTime

from app.db.database import Base


# SQLAlchemy model for storing operation logs
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    event = Column(String(50))
    level = Column(String(20))
    timestamp = Column(DateTime, nullable=True)
    user = Column(String(100))
    operation = Column(String(50))
    input = Column(Text)
    result = Column(Text)
