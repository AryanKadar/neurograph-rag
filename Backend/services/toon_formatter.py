"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - TOON Formatter (Token-Oriented Object Notation)
═══════════════════════════════════════════════════════════════
"""

from typing import List, Dict
from utils.logger import setup_logger

logger = setup_logger()


class ToonFormatter:
    """
    ┌─────────────────────────────────────────────┐
    │  📦 TOON Format Converter                   │
    │  Reduces token usage by 30-60%              │
    └─────────────────────────────────────────────┘
    
    TOON uses a tabular format instead of JSON:
    - Header row defines field names
    - Array length on second line
    - Tab-separated values
    """
    
    @staticmethod
    def format_context(chunks: List[Dict]) -> str:
        """
        Converts a list of RAG chunks into TOON format
        
        Example output:
        {file_id, chunk_index, content}
        [3]
        abc-123  0   This is the first chunk...
        abc-123  1   This is the second chunk...
        """
        if not chunks:
            return ""
        
        # Header for field names
        toon = "{file_id, idx, content}\n"
        toon += f"[{len(chunks)}]\n"
        
        for c in chunks:
            # Truncate content for token efficiency in the formatted output
            content = c.get('content', '')[:500]  # First 500 chars for context preview
            file_id = c.get('file_id', 'unknown')[:8]  # Shortened file ID
            idx = c.get('chunk_index', 0)
            
            toon += f"{file_id}\t{idx}\t{content}\n"
        
        return toon
    
    @staticmethod
    def format_history(history: List[Dict]) -> str:
        """
        Converts chat history into TOON format
        
        Example output:
        {role, content}
        [4]
        user    Hello!
        assistant   Hi there!
        """
        if not history:
            return ""
        
        toon = "{role, content}\n"
        toon += f"[{len(history)}]\n"
        
        for m in history:
            role = m.get('role', 'user')
            content = m.get('content', '')
            # Escape newlines in content
            content = content.replace('\n', ' ').replace('\t', ' ')
            toon += f"{role}\t{content}\n"
        
        return toon
    
    @staticmethod
    def format_full_context(chunks: List[Dict]) -> str:
        """
        Format chunks with full content (not truncated) for RAG
        """
        if not chunks:
            return ""
        
        formatted_chunks = []
        for i, c in enumerate(chunks):
            content = c.get('content', '')
            formatted_chunks.append(f"[Chunk {i+1}]:\n{content}")
        
        return "\n\n".join(formatted_chunks)
