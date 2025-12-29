# Backend Architecture Plan - FastAPI Setup

## 📋 Overview

This plan details the FastAPI backend architecture for the RAG chatbot system, running on **port 8000** with CORS configured for the frontend at **port 3000**.

---

### 🛠️ Environment Setup
It is **required** to use a Python virtual environment to manage dependencies and avoid system-level conflicts.

1. **Create Virtual Environment**:
   ```powershell
   python -m venv venv
   ```

2. **Activate Environment**:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

### 🚀 Bootstrapping with `backend.bat`
For quick startup, a `backend.bat` file should be located at the project root (`c:\Users\aryan\OneDrive\Desktop\Simple_ChatBot\backend.bat`).

**Content of `backend.bat`**:
```batch
@echo off
echo [COSMIC BACKEND] Starting initialization...

cd Backend

if not exist venv (
    echo [COSMIC BACKEND] Creating virtual environment...
    python -m venv venv
)

echo [COSMIC BACKEND] Activating virtual environment...
call venv\\Scripts\\activate

echo [COSMIC BACKEND] Checking dependencies...
pip install -r requirements.txt

echo [COSMIC BACKEND] Launching FastAPI server...
uvicorn main:app --reload --port 8000
```

---

## 🗂️ Directory Structure

```
Backend/
├── .env                          # Environment variables (already exists)
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
├── main.py                       # FastAPI app entry point
├── config/
│   └── settings.py              # Pydantic settings from environment
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py            # Document upload endpoints
│   │   ├── chat.py              # Chat/query endpoints
│   │   └── health.py            # Health check endpoint
│   └── dependencies.py          # Shared dependencies
├── services/
│   ├── __init__.py
│   ├── chunking.py              # Recursive text chunking logic
│   ├── embeddings.py            # Azure OpenAI embedding service
│   ├── vector_store.py          # FAISS vector database wrapper
│   ├── document_processor.py   # Document parsing (PDF, DOCX, TXT)
│   └── chat_service.py          # RAG query orchestration
├── models/
│   ├── __init__.py
│   ├── schemas.py               # Pydantic request/response models
│   └── document.py              # Document data models
├── utils/
│   ├── __init__.py
│   ├── file_handler.py          # File upload/validation utilities
│   └── logger.py                # Logging configuration
├── uploads/                      # Uploaded documents storage
└── vector_store/                 # FAISS index persistence
    ├── index.faiss
    ├── metadata.json
    └── chunks.json
```

---

## 🔧 Configuration Management

### `config/settings.py`

```python
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_BASE: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-5-chat"
    AZURE_OPENAI_API_VERSION: str = "2024-02-01"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-ada-002"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Storage Configuration
    UPLOAD_DIR: str = "./uploads"
    VECTOR_DB_PATH: str = "./vector_store"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Chunking Configuration
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    
    # HNSW Configuration
    HNSW_M: int = 16
    HNSW_EF_CONSTRUCTION: int = 200
    HNSW_EF_SEARCH: int = 50
    
    # RAG Configuration
    TOP_K_CHUNKS: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
```

---

## 🚀 FastAPI Application Setup

### `main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from config.settings import settings
from api.routes import upload, chat, health
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger()

# Create FastAPI app
app = FastAPI(
    title="Cosmic AI RAG Backend",
    description="RAG-powered chatbot with HNSW vector search",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(upload.router, prefix="/api", tags=["Documents"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Cosmic AI RAG Backend...")
    # Test Azure OpenAI connection
    from services.embeddings import test_azure_connection
    if await test_azure_connection():
        logger.info("✅ Azure OpenAI connection successful")
    else:
        logger.error("❌ Azure OpenAI connection failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
```

---

## 🛣️ API Endpoints

### 1. Health Check (`api/routes/health.py`)

```python
from fastapi import APIRouter
from services.embeddings import test_azure_connection

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Cosmic AI RAG Backend",
        "version": "1.0.0"
    }

@router.get("/health/azure")
async def azure_health_check():
    """Test Azure OpenAI connection"""
    is_connected = await test_azure_connection()
    return {
        "azure_openai": "connected" if is_connected else "disconnected",
        "status": "healthy" if is_connected else "degraded"
    }
```

### 2. Document Upload (`api/routes/upload.py`)

```python
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
import shutil
import os

from config.settings import settings
from models.schemas import UploadResponse, AnalyzeRequest, AnalyzeResponse
from services.document_processor import process_document
from utils.file_handler import validate_file, save_upload_file

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for processing"""
    
    # Validate file
    validate_file(file)
    
    # Save file
    file_path = await save_upload_file(file)
    
    return UploadResponse(
        filename=file.filename,
        file_id=os.path.basename(file_path),
        size=os.path.getsize(file_path),
        status="uploaded"
    )

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(
    request: AnalyzeRequest,
    background_tasks: BackgroundTasks
):
    """Process document: chunk, embed, and store in vector DB"""
    
    file_path = os.path.join(settings.UPLOAD_DIR, request.file_id)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Process in background (for large files)
    background_tasks.add_task(process_document, file_path, request.file_id)
    
    return AnalyzeResponse(
        file_id=request.file_id,
        status="processing",
        message="Document analysis started"
    )

@router.get("/analyze/status/{file_id}")
async def get_analysis_status(file_id: str):
    \"\"\"Get document processing status\"\"\"
    # This will check if chunks exist in vector store
    from services.vector_store import get_document_status
    
    status = get_document_status(file_id)
    return {
        "file_id": file_id,
        "status": status["status"],
        "chunks_count": status.get("chunks_count", 0)
    }

@router.get("/documents/{file_id}/view")
async def view_document(file_id: str):
    \"\"\"
    Serve the original document for high-fidelity preview (PDF/Text).
    Stored only for the last uploaded document.
    \"\"\"
    from fastapi.responses import FileResponse
    file_path = os.path.join(settings.UPLOAD_DIR, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(file_path)

@router.get("/documents/{file_id}/text-preview")
async def get_document_text(file_id: str):
    \"\"\"Return extracted text from vector store\"\"\"
    vector_store = get_vector_store()
    chunks = [c["content"] for c in vector_store.chunks if c["file_id"] == file_id]
    return {"content": "\\n\\n".join(chunks)}
```

### 3. Chat Endpoint (`api/routes/chat.py`)

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional

from models.schemas import ChatRequest, ChatResponse
from services.chat_service import process_query, stream_chat_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint"""
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    response = await process_query(
        query=request.query,
        use_rag=request.use_rag,
        file_ids=request.file_ids
    )
    
    return response

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint"""
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    return StreamingResponse(
        stream_chat_response(
            query=request.query,
            history=request.history,  # Added history support
            use_rag=request.use_rag,
            file_ids=request.file_ids
        ),
        media_type="text/event-stream"
    )
```

---

## 📝 Pydantic Models

### `models/schemas.py`

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Upload Models
class UploadResponse(BaseModel):
    filename: str
    file_id: str
    size: int
    status: str

class AnalyzeRequest(BaseModel):
    file_id: str

class AnalyzeResponse(BaseModel):
    file_id: str
    status: str
    message: str

# Chat Models
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list) # [{role: "user", content: "..."}]
    use_rag: bool = True
    file_ids: Optional[List[str]] = None

class RetrievedChunk(BaseModel):
    content: str
    score: float
    file_id: str
    chunk_index: int

class ChatResponse(BaseModel):
    response: str
    retrieved_chunks: Optional[List[RetrievedChunk]] = None
    model: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## 🔒 Security & Validation

### File Upload Validation (`utils/file_handler.py`)

```python
from fastapi import UploadFile, HTTPException
from config.settings import settings
import os
import uuid

ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.md'}

def validate_file(file: UploadFile):
    """Validate uploaded file"""
    
    # Check file extension
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {ext} not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    # Check file size (read content length header)
    if hasattr(file, 'size') and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        )

async def save_upload_file(file: UploadFile) -> str:
    """Save uploaded file, clearing old uploads first to save space"""
    import glob
    
    # Optional: Clear existing files in upload dir to keep only the latest one
    # as per user preference for "single active preview"
    for old_file in glob.glob(os.path.join(settings.UPLOAD_DIR, "*")):
        try:
            os.remove(old_file)
            logger.info(f"🧹 Cleaned up old file: {old_file}")
        except Exception as e:
            logger.error(f"Failed to delete {old_file}: {e}")

    file_id = str(uuid.uuid4())
    _, ext = os.path.splitext(file.filename)
    filename = f"{file_id}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return file_path
```

## 🧠 Chat Service & Guardrails (`services/chat_service.py`)

### 🛡️ Knowledge-Bound Guardrail
The system uses a strict **System Prompt** to ensure it only answers from the provided context.

**System Prompt Implementation:**
```python
SYSTEM_PROMPT = """
You are Cosmic AI, a helpful, advanced assistant.
Your knowledge is EXCLUSIVELY limited to the provided document context.

RULES:
1. ONLY use context to answer. If missing, say: "I'm sorry, my cosmic sensors can't find that in your documents."
2. Never use internal training data for document-specific questions.
3. Be professional and maintain the cosmic persona.
"""
```

### 📄 TOON Formatting Service (`services/toon.py`)
This service converts structured data (RAG context, history) into Token-Oriented Object Notation.

```python
class ToonFormatter:
    @staticmethod
    def format_context(chunks: List[Dict]) -> str:
        \"\"\"Converts a list of chunks into TOON format\"\"\"
        # Header for field names
        toon = "{file_id, chunk_index, content}\\n"
        toon += f"[{len(chunks)}]\\n" # Array length
        for c in chunks:
            # Tabular, no redundant quotes or keys
            toon += f"{c['file_id']}\\t{c['chunk_index']}\\t{c['content']}\\n"
        return toon

    @staticmethod
    def format_history(history: List[Dict]) -> str:
        \"\"\"Converts chat history into TOON format\"\"\"
        toon = "{role, content}\\n"
        toon += f"[{len(history)}]\\n"
        for m in history:
            toon += f"{m['role']}\\t{m['content']}\\n"
        return toon
```

### 🕰️ Hybrid History & Summarization
The system preserves near context exactly and summarizes older history.

- **Near Context**: Last **5 turns** (10 messages) kept as-is.
- **Far Context**: All messages before the last 10 are compressed into a single "Memory Summary."
- **Summarization Trigger**: When conversation exceeds 12 messages, old ones are summarized.

**Summarization Service (`services/summarization.py`):**
```python
async def summarize_history(history: List[Dict], current_summary: str = "") -> str:
    \"\"\"Compresses history into a concise TOON-like recap.\"\"\"
    prompt = f\"\"\"
    Update this recap with the NEW TURNS. Keep it concise, preserving key entities.
    
    OLD RECAP: {current_summary}
    NEW TURNS: {history}
    \"\"\"
    # Call Azure OpenAI GPT-5
    # Return updated recap string
```

**Updated Chat Service Logic:**
```python
async def stream_chat_response(query: str, history: List[Dict], current_summary: str, use_rag: bool, file_ids: List[str]):
    # 1. RAG Retrieval (Top 3 chunks)
    # ...
    
    # 2. Prepare Messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # 3. Add Long-Term Memory (Recap)
    if current_summary:
        messages.append({
            "role": "system", 
            "content": f"PREVIOUS_RECAP: {current_summary}"
        })
    
    # 4. Near Context & RAG Context (Combined for Token Efficiency)
    input_payload = []
    if history:
        input_payload.append(f"HISTORY:\\n{ToonFormatter.format_history(history[-10:])}")
    
    if context_chunks:
        input_payload.append(f"CONTENT:\\n{ToonFormatter.format_context(context_chunks)}")
    
    input_payload.append(f"QUERY: {query}")
    
    messages.append({
        "role": "user", 
        "content": "\\n\\n".join(input_payload)
    })
```

---

## 📊 Logging Configuration

### `utils/logger.py`

```python
import logging
import sys

def setup_logger():
    """Configure application logger"""
    
    logger = logging.getLogger("cosmic_ai")
    logger.setLevel(logging.INFO)
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger
```

---

## ✅ Verification Steps

1. **Test CORS Configuration**
   ```bash
   # Frontend should be able to make requests
   curl -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: POST" \
        -X OPTIONS http://localhost:8000/api/health
   ```

2. **Test Health Endpoint**
   ```bash
   curl http://localhost:8000/api/health
   ```

3. **Test Azure OpenAI Connection**
   ```bash
   curl http://localhost:8000/api/health/azure
   ```

4. **Test File Upload**
   ```bash
   curl -X POST http://localhost:8000/api/upload \
        -F "file=@test.txt"
   ```

---

## 🚨 Error Handling

All endpoints include:
- Input validation with Pydantic
- File size limits
- File type restrictions
- Azure OpenAI error handling
- Detailed error messages
- 500-level errors logged

---

## 📌 Next Steps

After backend foundation is complete:
1. Implement document processing service → `03_Document_Processing.md`
2. Set up vector database → `02_Vector_Database_Setup.md`
3. Implement chat service → See chat endpoint details in main plan
