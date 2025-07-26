from sqlalchemy.orm import Session
from . import models, schemas

# Function to get or create a conversation
def get_or_create_conversation(db: Session, user_id: str, conversation_id: int = None):
    if conversation_id:
        conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    else:
        conversation = models.Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    return conversation

# Function to save a message
def save_message(db: Session, conversation_id: int, role: str, content: str):
    message = models.Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# Functions to query product data
def get_product_stock(db: Session, product_name: str):
    product = db.query(models.Product).filter(models.Product.product_name.ilike(f"%{product_name}%")).first()
    return product

def get_order_status(db: Session, order_id: str):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    return order