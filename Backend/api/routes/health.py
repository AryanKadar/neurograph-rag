"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Health Check Routes
═══════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter
from datetime import datetime
from config.settings import settings
from services.embeddings import test_azure_connection
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """
    ┌─────────────────────────────────────────────┐
    │  💚 Basic health check                      │
    └─────────────────────────────────────────────┘
    """
    logger.info("💚 Health check requested")
    
    return {
        "status": "healthy",
        "service": "Cosmic AI Backend",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/health/azure")
async def azure_health_check():
    """
    ┌─────────────────────────────────────────────┐
    │  ☁️ Azure OpenAI connection health          │
    └─────────────────────────────────────────────┘
    """
    logger.info("☁️ Azure OpenAI health check requested")
    
    try:
        is_connected = await test_azure_connection()
        
        if is_connected:
            logger.info("   └─ ✅ Azure OpenAI connection successful")
            return {
                "status": "connected",
                "endpoint": settings.AZURE_OPENAI_API_BASE[:50] + "...",
                "deployment": settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                "embedding_deployment": settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT
            }
        else:
            logger.warning("   └─ ⚠️ Azure OpenAI connection failed")
            return {
                "status": "disconnected",
                "error": "Could not generate test embedding"
            }
            
    except Exception as e:
        logger.error(f"   └─ ❌ Azure OpenAI error: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
