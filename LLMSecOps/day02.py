# Importing Necessary Libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

# Defining Data Models
class ChatRequest(BaseModel):
    question: str
    context: str

class ChatResponse(BaseModel):
    answer: str

# Creating the FastAPI Application
app = FastAPI(title="Question Answering API", description="A simple QA API using transformers")

# Initialize the pipeline once at startup
qa_pipeline = None

@app.on_event("startup")
async def startup_event():
    global qa_pipeline
    # Initializing the Question-Answering Pipeline
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Creating the /chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if qa_pipeline is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        result = qa_pipeline(question=request.question, context=request.context)
        return ChatResponse(answer=result['answer'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": qa_pipeline is not None}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Question Answering API", "docs": "/docs"}

# running the app server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)