from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from database import Base, engine

class Client(Base):
     __tablename__ = "clients"
     id = Column(Integer, primary_key=True, index=True)
     name = Column(String, nullable=False)
     company_name = Column(String, nullable=True)
     phone = Column(String, nullable=False)
     email = Column(String, nullable=True)
     notes = Column(Text, nullable=True)
     
     contracts = relationship("Contract", back_populates="client")