from fastapi import FastAPI

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="API for the e-commerce customer support chatbot.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the E-Commerce Chatbot API!"}

# We will add the /api/chat endpoint in the next milestone