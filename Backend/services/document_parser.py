"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Document Parser
═══════════════════════════════════════════════════════════════
"""

import os
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger()


class DocumentParser:
    """
    ┌─────────────────────────────────────────────┐
    │  📄 Parse various document formats          │
    │  Supports: PDF, DOCX, TXT, MD               │
    └─────────────────────────────────────────────┘
    """
    
    @staticmethod
    def parse(file_path: str) -> str:
        """
        Parse document and extract text
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        logger.info(f"📄 Parsing document: {os.path.basename(file_path)}")
        logger.info(f"   └─ Format: {ext}")
        
        if ext in ['.txt', '.md']:
            return DocumentParser._parse_text(file_path)
        elif ext == '.pdf':
            return DocumentParser._parse_pdf(file_path)
        elif ext == '.docx':
            return DocumentParser._parse_docx(file_path)
        else:
            raise ValueError(f"❌ Unsupported file format: {ext}")
    
    @staticmethod
    def _parse_text(file_path: str) -> str:
        """Parse plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        logger.info(f"   └─ Extracted: {len(content)} characters")
        return content
    
    @staticmethod
    def _parse_pdf(file_path: str) -> str:
        """Parse PDF file"""
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(file_path)
            text_parts = []
            
            logger.info(f"   └─ Pages found: {len(reader.pages)}")
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    text_parts.append(text)
                    logger.info(f"      └─ Page {page_num + 1}: {len(text)} chars")
            
            full_text = "\n\n".join(text_parts)
            logger.info(f"   └─ Total extracted: {len(full_text)} characters")
            
            return full_text
            
        except Exception as e:
            logger.error(f"❌ PDF parsing error: {e}")
            raise
    
    @staticmethod
    def _parse_docx(file_path: str) -> str:
        """Parse DOCX file"""
        try:
            from docx import Document as DocxDocument
            
            doc = DocxDocument(file_path)
            paragraphs = []
            
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    paragraphs.append(text)
            
            full_text = "\n\n".join(paragraphs)
            
            logger.info(f"   └─ Paragraphs: {len(paragraphs)}")
            logger.info(f"   └─ Total extracted: {len(full_text)} characters")
            
            return full_text
            
        except Exception as e:
            logger.error(f"❌ DOCX parsing error: {e}")
            raise
