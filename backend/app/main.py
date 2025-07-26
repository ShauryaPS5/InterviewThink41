# backend/app/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

# Import all the components we've built
from . import crud, models, schemas, llm_integration
from .database import SessionLocal, engine

# This line tells SQLAlchemy to create all the tables defined in models.py
# It will check if the tables exist before creating them, so it's safe to run every time.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="This API powers a customer support chatbot for an e-commerce platform.",
    version="1.0.0"
)

# --- Dependency ---
# This function creates a new database session for each request and closes it when it's done.
# This is a standard pattern in FastAPI to ensure database connections are handled correctly.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API Endpoints ---

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the E-Commerce Chatbot API!"}


@app.post("/api/chat", response_model=schemas.ChatResponse, tags=["Chat"])
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    """
    The main endpoint for handling chat interactions.

    - Accepts a user's message, user ID, and an optional conversation ID.
    - Persists the user's message and the AI's response to the database.
    - Integrates with an LLM to generate context-aware and data-driven responses.
    - Returns the AI's response, the current conversation ID, and the full chat history.
    """
    
    # 1. Get the existing conversation or create a new one.
    conversation = crud.get_or_create_conversation(
        db, 
        user_id=request.user_id, 
        conversation_id=request.conversation_id
    )
    
    # 2. Save the user's incoming message to the database.
    crud.save_message(
        db, 
        conversation_id=conversation.id, 
        role="user", 
        content=request.user_message
    )
    
    # 3. Get an intelligent response from the LLM, which may query the database.
    ai_response_content = llm_integration.get_llm_response(
        db, 
        user_message=request.user_message
    )
    
    # 4. Save the AI's response to the database.
    crud.save_message(
        db, 
        conversation_id=conversation.id, 
        role="ai", 
        content=ai_response_content
    )
    
    # 5. Retrieve the full, updated conversation history.
    history = db.query(models.Message)\
                .filter(models.Message.conversation_id == conversation.id)\
                .order_by(models.Message.timestamp)\
                .all()
    
    # 6. Return the final response object.
    return schemas.ChatResponse(
        ai_response=ai_response_content,
        conversation_id=conversation.id,
        history=history
    )