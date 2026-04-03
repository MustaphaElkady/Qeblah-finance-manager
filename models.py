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

class Package(Base):
     __tablename__ = "packages"
     id = Column(Integer, primary_key=True, index=True)
     package_name = Column(String, nullable=False)
     package_type = Column(String, nullable=True)
     default_price = Column(Float, nullable=False, default=0)
     description = Column(Text, nullable=True)

     contracts = relationship("Contract", back_populates="package")



class Contract(Base):
     __tablename__ = "contracts"
     id = Column(Integer, primary_key=True, index=True)
     client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
     package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)

     start_date = Column(Date, nullable=False)
     end_date = Column(Date, nullable=False)
     agreed_price = Column(Float, nullable=False)
     status = Column(String, nullable=False, default="Active")
     client = relationship("Client", back_populates="contracts")
     package = relationship("Package", back_populates="contracts")
     payments = relationship("Payment", back_populates="contract")
     expenses = relationship("Expense", back_populates="contract")


class Payment(Base):
     __tablename__ = "payments"    
     id = Column(Integer, primary_key=True, index=True)
     contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
     payment_date = Column(Date, nullable=False)
     amount = Column(Float, nullable=False)
     payment_method = Column(String, nullable=True)
     notes = Column(Text, nullable=True)
     contract = relationship("Contract", back_populates="payments")

class Expense(Base):
     __tablename__ = "expenses"    
     id = Column(Integer, primary_key=True, index=True)
     contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
     expense_date = Column(Date, nullable=False)
     category = Column(String, nullable=False)
     amount = Column(Float, nullable=False)
     notes = Column(Text, nullable=True)
     contract = relationship("Contract", back_populates="expenses")

def create_tables(): # 002_app.py
    Base.metadata.create_all(bind=engine)