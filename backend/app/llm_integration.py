import os
from groq import Groq
from . import crud
from sqlalchemy.orm import Session

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
LLM_MODEL = "llama3-8b-8192"

# This is the "tool" the LLM can use to query your database.
def get_database_info(db: Session, query: str):
    """
    This function processes a user's natural language query,
    determines what information is needed, and queries the database.
    """
    query_lower = query.lower()

    # Rule-based logic to map intent to a CRUD function
    if "how many" in query_lower and "left" in query_lower:
        # Extract product name (this is a simplification)
        product_name = query_lower.split("how many ")[1].split(" left")[0].strip()
        product = crud.get_product_stock(db, product_name)
        if product:
            return f"There are {product.stock_quantity} units of {product.product_name} left in stock."
        else:
            return f"Sorry, I couldn't find a product named {product_name}."

    elif "status of order" in query_lower:
        order_id = query_lower.split("status of order ")[1].strip().upper()
        order = crud.get_order_status(db, order_id)
        if order:
            return f"The status of order {order.order_id} is: {order.status}."
        else:
            return f"Sorry, I could not find any information for order ID {order_id}."
    
    # Add more rules for other use cases, like top selling products.
    
    else:
        return None # Return None if no specific tool matches

def get_llm_response(db: Session, user_message: str):
    # First, try to use our database tools
    db_info = get_database_info(db, user_message)
    if db_info:
        return db_info

    # If no tool matches, fall back to a general chat with the LLM
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful customer support assistant for an e-commerce store."
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model=LLM_MODEL,
    )
    return chat_completion.choices[0].message.content