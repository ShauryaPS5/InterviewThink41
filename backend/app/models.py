from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Product(Base):
    __tablename__ = "products"
    product_id = Column(String, primary_key=True, index=True)
    product_name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)

# Define other models for Customer, Order, OrderItem, etc.
# For example, for Orders:
class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    order_date = Column(DateTime)
    status = Column(String)
    # Add relationships
    customer = relationship("Customer", back_populates="orders")

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String, primary_key=True, index=True)
    customer_name = Column(String)
    email = Column(String)
    # Add back-population for the relationship
    orders = relationship("Order", back_populates="customer")



    # Add these classes to backend/app/models.py

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True) # A unique identifier for the user
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String) # "user" or "ai"
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")

# TODO: Define models for OrderItem and Review