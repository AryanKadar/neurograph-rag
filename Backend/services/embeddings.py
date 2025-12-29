"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Embedding Service (Local Model)
═══════════════════════════════════════════════════════════════
Uses sentence-transformers for local embedding generation.
Falls back to this since Azure OpenAI embedding deployment is not available.
"""

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger()


class EmbeddingService:
    """
    ┌─────────────────────────────────────────────┐
    │  🧠 Local Embedding Generation              │
    │  Model: all-mpnet-base-v2 (768 dimensions)  │
    └─────────────────────────────────────────────┘
    """
    
    # Model produces 768-dimensional embeddings (better quality than 384)
    MODEL_NAME = "all-mpnet-base-v2"
    EMBEDDING_DIMENSION = 768
    
    def __init__(self):
        logger.info(f"🧠 Loading local embedding model: {self.MODEL_NAME}...")
        self.model = SentenceTransformer(self.MODEL_NAME)
        self.dimension = self.EMBEDDING_DIMENSION
        
        logger.info(f"🧠 EmbeddingService initialized (LOCAL)")
        logger.info(f"   └─ Model: {self.MODEL_NAME}")
        logger.info(f"   └─ Dimension: {self.dimension}")

    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            NumPy array of shape (len(texts), 768)
        """
        if not texts:
            return np.array([])
        
        logger.info(f"🧠 Generating embeddings for {len(texts)} texts...")
        
        try:
            # Generate embeddings using sentence-transformers
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            embeddings_array = embeddings.astype(np.float32)
            
            logger.info(f"   └─ Generated: {len(embeddings)} embeddings")
            logger.info(f"   └─ Shape: {embeddings_array.shape}")
            
            return embeddings_array
            
        except Exception as e:
            logger.error(f"❌ Error generating embeddings: {e}")
            raise
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query
        
        Args:
            query: Query text
            
        Returns:
            NumPy array of shape (768,)
        """
        embeddings = self.embed_texts([query])
        return embeddings[0] if len(embeddings) > 0 else np.array([])


# Global embedding service instance
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service singleton"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


async def test_azure_connection() -> bool:
    """Test embedding service connection"""
    try:
        service = get_embedding_service()
        test_embedding = service.embed_query("test")
        return len(test_embedding) == EmbeddingService.EMBEDDING_DIMENSION
    except Exception as e:
        logger.error(f"❌ Embedding service test failed: {e}")
        return False
