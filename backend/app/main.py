from fastapi import FastAPI
# Add these imports to main.py
from fastapi import Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine) # Ensure tables are created

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# The main chat endpoint
@app.post("/api/chat", response_model=schemas.ChatResponse, tags=["Chat"])
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    # 1. Get or create the conversation
    conversation = crud.get_or_create_conversation(db, user_id=request.user_id, conversation_id=request.conversation_id)
    
    # 2. Save the user's message
    crud.save_message(db, conversation_id=conversation.id, role="user", content=request.user_message)
    
    # 3. (TEMP) Generate a dummy AI response. We'll replace this in Milestone 5.
    ai_dummy_response = f"I received your message: '{request.user_message}'. I am still learning!"
    
    # 4. Save the AI's response
    crud.save_message(db, conversation_id=conversation.id, role="ai", content=ai_dummy_response)
    
    # 5. Prepare and return the response
    history = db.query(models.Message).filter(models.Message.conversation_id == conversation.id).all()
    
    return schemas.ChatResponse(
        ai_response=ai_dummy_response,
        conversation_id=conversation.id,
        history=history
    )

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="API for the e-commerce customer support chatbot.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the E-Commerce Chatbot API!"}

# We will add the /api/chat endpoint in the next milestone