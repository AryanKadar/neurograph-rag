"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Professional Response Formatter
═══════════════════════════════════════════════════════════════
"""

from typing import List, Dict, Optional
from datetime import datetime
import re


class ResponseFormatter:
    """
    ┌─────────────────────────────────────────────┐
    │  ✨ Professional Response Formatter          │
    │  Creates beautiful, structured responses    │
    └─────────────────────────────────────────────┘
    """
    
    # Icons and symbols for professional formatting
    ICONS = {
        "answer": "💡",
        "source": "📚",
        "info": "ℹ️",
        "warning": "⚠️",
        "success": "✅",
        "error": "❌",
        "search": "🔍",
        "document": "📄",
        "context": "🎯",
        "summary": "📝",
        "code": "```",
        "quote": "💬",
        "bullet": "•",
        "arrow": "→",
        "check": "✓",
        "star": "⭐"
    }
    
    @staticmethod
    def format_professional_response(
        answer: str,
        context_chunks: Optional[List[Dict]] = None,
        query: str = ""
    ) -> str:
        """
        Format a professional response with sections, icons, and structure.
        
        Example Output:
        ┌─────────────────────────────────────────┐
        │  💡 Answer                               │
        └─────────────────────────────────────────┘
        
        Your answer here with proper formatting...
        
        ┌─────────────────────────────────────────┐
        │  📚 Sources (3 documents)                │
        └─────────────────────────────────────────┘
        
        • Document 1: filename.pdf (Relevance: 95%)
        • Document 2: another.pdf (Relevance: 87%)
        """
        
        sections = []
        
        # Main Answer Section
        sections.append(ResponseFormatter._create_section_header("Answer", "💡"))
        sections.append(ResponseFormatter._format_answer_text(answer))
        sections.append("")  # Blank line for spacing
        
        # Sources Section (if available)
        if context_chunks and len(context_chunks) > 0:
            sources_header = ResponseFormatter._create_section_header(
                f"Sources ({len(context_chunks)} references)", 
                "📚"
            )
            sections.append(sources_header)
            sections.append(ResponseFormatter._format_sources(context_chunks))
            sections.append("")
        
        return "\n".join(sections)
    
    @staticmethod
    def _create_section_header(title: str, icon: str = "") -> str:
        """Create a beautiful section header with borders"""
        header_text = f"{icon} {title}" if icon else title
        border_length = len(header_text) + 4
        
        header = f"""
┌{'─' * border_length}┐
│  {header_text}  │
└{'─' * border_length}┘
""".strip()
        
        return header
    
    @staticmethod
    def _format_answer_text(text: str) -> str:
        """
        Format the answer text with proper styling.
        - Detect lists and add bullet points
        - Detect code blocks and format them
        - Add proper spacing
        """
        
        # Clean up the text
        text = text.strip()
        
        # Enhance markdown formatting
        lines = text.split('\n')
        formatted_lines = []
        
        in_code_block = False
        for line in lines:
            # Detect code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                formatted_lines.append(line)
                continue
            
            if in_code_block:
                formatted_lines.append(line)
                continue
            
            # Enhance list items
            if line.strip().startswith(('- ', '* ', '• ')):
                # Replace with professional bullet
                cleaned_line = re.sub(r'^[\s]*[-*•][\s]*', '', line)
                formatted_lines.append(f"  • {cleaned_line}")
            elif line.strip().startswith(tuple(f"{i}." for i in range(1, 10))):
                # Numbered lists
                formatted_lines.append(f"  {line.strip()}")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def _format_sources(chunks: List[Dict]) -> str:
        """
        Format source references professionally.
        Shows: document name, relevance score, and snippet preview
        """
        
        sources_text = []
        
        for i, chunk in enumerate(chunks, 1):
            file_id = chunk.get('file_id', 'unknown')
            score = chunk.get('score', 0.0)
            content_preview = chunk.get('content', '')[:80]
            
            # Calculate relevance percentage
            relevance = int(score * 100) if score <= 1 else score
            
            # Create source entry
            source_entry = f"  {ResponseFormatter.ICONS['bullet']} **Source #{i}**"
            source_entry += f" (Relevance: {relevance}%)\n"
            source_entry += f"    {ResponseFormatter.ICONS['document']} Document ID: `{file_id[:12]}...`\n"
            
            if content_preview:
                source_entry += f"    {ResponseFormatter.ICONS['quote']} _\"{content_preview}...\"_\n"
            
            sources_text.append(source_entry)
        
        return '\n'.join(sources_text)
    
    @staticmethod
    def format_error_response(error_message: str, query: str = "") -> str:
        """Format error messages professionally"""
        
        sections = []
        
        # Error Header
        sections.append(ResponseFormatter._create_section_header("System Message", "⚠️"))
        sections.append("")
        
        # Friendly error message
        sections.append(f"{ResponseFormatter.ICONS['error']} I encountered an issue while processing your request.")
        sections.append("")
        sections.append("**What happened:**")
        sections.append(f"  {ResponseFormatter.ICONS['info']} {error_message}")
        sections.append("")
        sections.append("**What you can try:**")
        sections.append(f"  {ResponseFormatter.ICONS['bullet']} Rephrase your question")
        sections.append(f"  {ResponseFormatter.ICONS['bullet']} Upload relevant documents first")
        sections.append(f"  {ResponseFormatter.ICONS['bullet']} Check your internet connection")
        sections.append("")
        
        return '\n'.join(sections)
    
    @staticmethod
    def format_no_context_response(query: str) -> str:
        """Format response when no context is found"""
        
        sections = []
        
        sections.append(ResponseFormatter._create_section_header("No Documents Found", "🔍"))
        sections.append("")
        sections.append(f"{ResponseFormatter.ICONS['info']} I couldn't find relevant information in your uploaded documents.")
        sections.append("")
        sections.append("**Suggestions:**")
        sections.append(f"  {ResponseFormatter.ICONS['bullet']} Upload documents related to: _{query}_")
        sections.append(f"  {ResponseFormatter.ICONS['bullet']} Try a different search term")
        sections.append(f"  {ResponseFormatter.ICONS['bullet']} Check if your documents contain the information you're looking for")
        sections.append("")
        
        return '\n'.join(sections)
    
    @staticmethod
    def add_thinking_process(response: str, steps: List[str]) -> str:
        """
        Add a 'thinking process' section to show the AI's reasoning.
        Great for transparency and trust.
        """
        
        if not steps:
            return response
        
        thinking_section = []
        thinking_section.append("")
        thinking_section.append(ResponseFormatter._create_section_header("How I Found This", "🧠"))
        thinking_section.append("")
        
        for i, step in enumerate(steps, 1):
            thinking_section.append(f"  {i}. {step}")
        
        thinking_section.append("")
        
        return response + '\n'.join(thinking_section)
    
    @staticmethod
    def create_metadata_footer(
        model: str, 
        chunks_searched: int = 0,
        response_time_ms: Optional[int] = None
    ) -> str:
        """Create a professional metadata footer"""
        
        footer = []
        footer.append("")
        footer.append("─" * 50)
        footer.append("")
        
        metadata = []
        metadata.append(f"{ResponseFormatter.ICONS['star']} **Model:** {model}")
        
        if chunks_searched > 0:
            metadata.append(f"{ResponseFormatter.ICONS['search']} **Documents Searched:** {chunks_searched}")
        
        if response_time_ms:
            metadata.append(f"⏱️ **Response Time:** {response_time_ms}ms")
        
        metadata.append(f"🕐 **Generated:** {datetime.now().strftime('%H:%M:%S')}")
        
        footer.append(" | ".join(metadata))
        footer.append("")
        
        return '\n'.join(footer)
