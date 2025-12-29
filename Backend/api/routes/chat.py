"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Chat Routes
═══════════════════════════════════════════════════════════════
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from datetime import datetime
from services.chat_service import get_chat_service
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter(prefix="/api", tags=["chat"])


# ─────────────────────────────────────────────────────────────
#  📦 Request/Response Models
# ─────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Chat request model"""
    query: str = Field(..., min_length=1, max_length=2000)
    history: Optional[List[dict]] = Field(default_factory=list)
    current_summary: Optional[str] = ""
    use_rag: bool = True
    file_ids: Optional[List[str]] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    retrieved_chunks: Optional[List[dict]] = None
    model: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ─────────────────────────────────────────────────────────────
#  🚀 Chat Endpoints
# ─────────────────────────────────────────────────────────────

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    ┌─────────────────────────────────────────────┐
    │  🌊 Streaming chat endpoint                 │
    │  Returns Server-Sent Events                 │
    └─────────────────────────────────────────────┘
    """
    
    logger.info("═" * 60)
    logger.info("🌊 STREAMING CHAT REQUEST")
    logger.info("═" * 60)
    logger.info(f"   └─ Query: {request.query[:50]}...")
    logger.info(f"   └─ History: {len(request.history)} messages")
    logger.info(f"   └─ RAG enabled: {request.use_rag}")
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    chat_service = get_chat_service()
    
    return StreamingResponse(
        chat_service.stream_chat_response(
            query=request.query,
            history=request.history,
            current_summary=request.current_summary,
            use_rag=request.use_rag,
            file_ids=request.file_ids
        ),
        media_type="text/event-stream"
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    ┌─────────────────────────────────────────────┐
    │  💬 Non-streaming chat endpoint             │
    │  Returns complete response                  │
    └─────────────────────────────────────────────┘
    """
    
    logger.info("═" * 60)
    logger.info("💬 CHAT REQUEST")
    logger.info("═" * 60)
    logger.info(f"   └─ Query: {request.query[:50]}...")
    logger.info(f"   └─ RAG enabled: {request.use_rag}")
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    chat_service = get_chat_service()
    
    try:
        result = await chat_service.get_chat_response(
            query=request.query,
            history=request.history,
            use_rag=request.use_rag,
            file_ids=request.file_ids
        )
        
        return ChatResponse(
            response=result["response"],
            retrieved_chunks=result.get("retrieved_chunks"),
            model=result["model"],
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
