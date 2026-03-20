import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from fastapi.responses import FileResponse

# Relative import when running as a module, but running directly might need sys.path hack
# We'll just assume running from `indecimal` root: `python -m backend.main`
from backend.rag_pipeline import rag_ask

app = FastAPI(title="Mini RAG Chatbot API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(BASE_DIR, "frontend")

# Mount frontend
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    context: list

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not rag_ask:
        return ChatResponse(
            answer="Error: RAG pipeline not initialized. Did you run `python backend/document_processor.py` first to build the vector index?",
            context=[]
        )
    
    try:
        result = rag_ask(request.query)
        return ChatResponse(
            answer=result["answer"],
            context=result["context"]
        )
    except Exception as e:
        return ChatResponse(
            answer=f"Error generating answer: {str(e)}",
            context=[]
        )

# Simple endpoint to serve the frontend index.html on root
@app.get("/")
async def get_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
