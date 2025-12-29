"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Chat Service with RAG
═══════════════════════════════════════════════════════════════
"""

import json
import time
from typing import List, Dict, Optional, AsyncGenerator
from openai import AzureOpenAI, APIError, APIConnectionError
from config.settings import settings
from services.vector_store import get_vector_store
from services.embeddings import get_embedding_service
from services.toon_formatter import ToonFormatter
from services.response_formatter import ResponseFormatter
from utils.logger import setup_logger

logger = setup_logger()


# ─────────────────────────────────────────────────────────────
#  🛡️ System Prompt - Knowledge-Bound Guardrail
# ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are Cosmic AI, an intelligent and professional assistant.

**Your Knowledge Boundary:**
- You EXCLUSIVELY answer based on the provided CONTEXT from uploaded documents
- If information is not in the context, politely state: "I couldn't find that information in your documents."

**Response Guidelines:**
1. **Be Clear & Structured**: Use headings, lists, and proper formatting
2. **Provide Evidence**: Quote relevant parts from the context when helpful
3. **Be Comprehensive**: Cover all aspects of the question that are in the context
4. **Use Markdown**: Format your responses with proper markdown for readability
   - Use **bold** for emphasis
   - Use bullet points for lists
   - Use code blocks for technical content
   - Use > for important quotes
5. **Be Professional**: Maintain a helpful, knowledgeable tone
6. **Be Concise**: Provide thorough answers without unnecessary verbosity

**Important:** Never use your general training knowledge to answer document-specific questions. Only use the provided CONTEXT.
"""


class ChatService:
    """
    ┌─────────────────────────────────────────────┐
    │  💬 Chat Service with RAG Integration       │
    │  Streaming responses with context           │
    └─────────────────────────────────────────────┘
    """
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_API_BASE
        )
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT_NAME
        
        logger.info(f"💬 ChatService initialized")
        logger.info(f"   └─ Deployment: {self.deployment}")
    
    async def stream_chat_response(
        self,
        query: str,
        history: List[Dict] = None,
        current_summary: str = "",
        use_rag: bool = True,
        file_ids: List[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        ┌─────────────────────────────────────────────┐
        │  🌊 Stream chat response with RAG           │
        └─────────────────────────────────────────────┘
        """
        
        history = history or []
        context_chunks = []
        
        logger.info("─" * 60)
        logger.info(f"💬 Processing query: {query[:50]}...")
        
        # ─────────────────────────────────────
        # Step 1: RAG Retrieval (if enabled)
        # ─────────────────────────────────────
        if use_rag:
            logger.info("🔍 Retrieving relevant context...")
            
            try:
                embedding_service = get_embedding_service()
                vector_store = get_vector_store()
                
                # Generate query embedding
                query_embedding = embedding_service.embed_query(query)
                
                # Search for similar chunks
                context_chunks = vector_store.search(
                    query_embedding,
                    top_k=settings.TOP_K_RESULTS,
                    file_ids=file_ids
                )
                
                if context_chunks:
                    logger.info(f"   └─ Found: {len(context_chunks)} relevant chunks")
                    for i, chunk in enumerate(context_chunks):
                        logger.info(f"      └─ Chunk {i+1}: Score {chunk['score']:.3f}")
                else:
                    logger.info("   └─ No relevant chunks found")
                    
            except Exception as e:
                logger.error(f"❌ RAG retrieval error: {e}")
        
        # ─────────────────────────────────────
        # Step 2: Prepare Messages
        # ─────────────────────────────────────
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add Long-Term Memory (Recap) if available
        if current_summary:
            messages.append({
                "role": "system",
                "content": f"PREVIOUS_RECAP: {current_summary}"
            })
        
        # Build input payload (Combined for token efficiency)
        input_parts = []
        
        # Add recent history (last 10 messages)
        if history:
            recent_history = history[-10:]
            history_text = ToonFormatter.format_history(recent_history)
            if history_text:
                input_parts.append(f"HISTORY:\n{history_text}")
        
        # Add RAG context
        if context_chunks:
            context_text = ToonFormatter.format_full_context(context_chunks)
            input_parts.append(f"CONTEXT:\n{context_text}")
        
        # Add the query
        input_parts.append(f"QUERY: {query}")
        
        # Combine into single user message
        user_content = "\n\n".join(input_parts)
        messages.append({"role": "user", "content": user_content})
        
        logger.info(f"📤 Sending to Azure OpenAI...")
        logger.info(f"   └─ Messages: {len(messages)}")
        
        # ─────────────────────────────────────
        # Step 3: Stream Response
        # ─────────────────────────────────────
        try:
            stream = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                stream=True,
                temperature=settings.GPT_TEMPERATURE,
                max_tokens=settings.GPT_MAX_COMPLETION_TOKENS,
                top_p=settings.GPT_TOP_P,
                frequency_penalty=settings.GPT_FREQUENCY_PENALTY,
                presence_penalty=settings.GPT_PRESENCE_PENALTY
            )

            
            full_response = ""
            
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        content = delta.content
                        full_response += content
                        
                        # Yield SSE formatted data
                        yield f"data: {json.dumps({'content': content})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"
            
            logger.info(f"✅ Response completed: {len(full_response)} chars")
            
        except Exception as e:
            logger.error(f"❌ Streaming error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    async def get_chat_response(
        self,
        query: str,
        history: List[Dict] = None,
        use_rag: bool = True,
        file_ids: List[str] = None
    ) -> Dict:
        """
        Get non-streaming chat response
        """
        
        history = history or []
        context_chunks = []
        
        # RAG Retrieval
        if use_rag:
            try:
                embedding_service = get_embedding_service()
                vector_store = get_vector_store()
                
                query_embedding = embedding_service.embed_query(query)
                context_chunks = vector_store.search(
                    query_embedding,
                    top_k=settings.TOP_K_RESULTS,
                    file_ids=file_ids
                )
            except Exception as e:
                logger.error(f"❌ RAG retrieval error: {e}")
        
        # Prepare messages
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add context
        input_parts = []
        
        if history:
            recent_history = history[-10:]
            history_text = ToonFormatter.format_history(recent_history)
            if history_text:
                input_parts.append(f"HISTORY:\n{history_text}")
        
        if context_chunks:
            context_text = ToonFormatter.format_full_context(context_chunks)
            input_parts.append(f"CONTEXT:\n{context_text}")
        
        input_parts.append(f"QUERY: {query}")
        
        user_content = "\n\n".join(input_parts)
        messages.append({"role": "user", "content": user_content})
        
        # Get response
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=settings.GPT_TEMPERATURE,
                max_tokens=settings.GPT_MAX_COMPLETION_TOKENS,
                top_p=settings.GPT_TOP_P,
                frequency_penalty=settings.GPT_FREQUENCY_PENALTY,
                presence_penalty=settings.GPT_PRESENCE_PENALTY
            )

            
            return {
                "response": response.choices[0].message.content,
                "retrieved_chunks": context_chunks,
                "model": self.deployment
            }
            
        except Exception as e:
            logger.error(f"❌ Chat error: {e}")
            raise


# Global chat service instance
_chat_service = None


def get_chat_service() -> ChatService:
    """Get or create chat service singleton"""
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service
