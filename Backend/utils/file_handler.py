"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - File Upload Handler
═══════════════════════════════════════════════════════════════
"""

import os
import uuid
import glob
from fastapi import UploadFile, HTTPException
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger()

ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.md'}


def validate_file(file: UploadFile):
    """
    ┌─────────────────────────────────────────────┐
    │  📋 Validate uploaded file                  │
    └─────────────────────────────────────────────┘
    """
    
    # Check file extension
    _, ext = os.path.splitext(file.filename or "")
    if ext.lower() not in ALLOWED_EXTENSIONS:
        logger.warning(f"Rejected file type: {ext}")
        raise HTTPException(
            status_code=400,
            detail=f"❌ File type {ext} not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    logger.info(f"✅ File validation passed: {file.filename}")


async def save_upload_file(file: UploadFile) -> tuple[str, str]:
    """
    ┌─────────────────────────────────────────────┐
    │  💾 Save uploaded file to disk              │
    │  Clears old files to keep only latest      │
    └─────────────────────────────────────────────┘
    
    Returns:
        tuple of (file_path, file_id)
    """
    
    # Clear existing files in upload dir to keep only the latest one
    logger.info("🧹 Cleaning up old uploaded files...")
    for old_file in glob.glob(os.path.join(settings.UPLOAD_DIR, "*")):
        try:
            os.remove(old_file)
            logger.info(f"   └─ Removed: {os.path.basename(old_file)}")
        except Exception as e:
            logger.error(f"   └─ Failed to delete {old_file}: {e}")
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    _, ext = os.path.splitext(file.filename or "")
    filename = f"{file_id}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    # Save file
    logger.info(f"💾 Saving new file: {filename}")
    with open(file_path, "wb") as buffer:
        content = await file.read()
        
        # Check file size
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"❌ File too large. Max size: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        buffer.write(content)
    
    logger.info(f"✅ File saved successfully: {file_path}")
    
    return file_path, file_id
