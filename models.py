# generate database table
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    #  table name 
    __tablename__ = "product"

    id = Column(Integer, primary_key=True , index=True)
    name = Column(String(100))
    price = Column(Float)