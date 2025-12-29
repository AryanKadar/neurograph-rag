"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Text Chunker (Recursive Splitting)
═══════════════════════════════════════════════════════════════
"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger()


class TextChunker:
    """
    ┌─────────────────────────────────────────────┐
    │  ✂️ Recursive text chunking                 │
    │  Preserves semantic boundaries              │
    └─────────────────────────────────────────────┘
    """
    
    def __init__(self):
        # Approximate tokens per character (rough estimate)
        # OpenAI uses ~4 chars per token on average
        chunk_size_chars = settings.CHUNK_SIZE * 4
        chunk_overlap_chars = settings.CHUNK_OVERLAP * 4
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size_chars,
            chunk_overlap=chunk_overlap_chars,
            length_function=len,
            separators=[
                "\n\n",  # Paragraph
                "\n",    # Line
                ". ",    # Sentence
                ", ",    # Phrase
                " ",     # Word
                ""       # Character (last resort)
            ],
            keep_separator=True
        )
        
        logger.info(f"✂️ TextChunker initialized")
        logger.info(f"   └─ Chunk size: {chunk_size_chars} chars (~{settings.CHUNK_SIZE} tokens)")
        logger.info(f"   └─ Overlap: {chunk_overlap_chars} chars")
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into semantic chunks
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        if not text or not text.strip():
            logger.warning("⚠️ Empty text provided for chunking")
            return []
        
        logger.info(f"✂️ Chunking text: {len(text)} characters")
        
        chunks = self.splitter.split_text(text)
        
        # Post-process chunks
        min_chunk_chars = settings.MIN_CHUNK_SIZE * 4  # Convert tokens to chars
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            # Remove excessive whitespace
            chunk = " ".join(chunk.split())
            
            # Skip very small chunks (use MIN_CHUNK_SIZE from settings)
            if len(chunk) < min_chunk_chars:
                logger.info(f"   └─ Skipping small chunk {i}: {len(chunk)} chars")
                continue
            
            processed_chunks.append(chunk)

        
        logger.info(f"   └─ Generated: {len(processed_chunks)} chunks")
        
        return processed_chunks


# Global chunker instance
_text_chunker = None


def get_text_chunker() -> TextChunker:
    """Get or create text chunker singleton"""
    global _text_chunker
    if _text_chunker is None:
        _text_chunker = TextChunker()
    return _text_chunker
