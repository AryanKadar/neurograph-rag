"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Secure & Professional Console Logger
═══════════════════════════════════════════════════════════════
"""

import logging
import sys
import re
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Custom cosmic theme
cosmic_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "cosmic": "bold magenta",
})

console = Console(theme=cosmic_theme)


# ─────────────────────────────────────────────────────────────
#  🔒 Security: Hide Sensitive Data
# ─────────────────────────────────────────────────────────────

def sanitize_message(message: str) -> str:
    """
    Remove or mask sensitive information from log messages.
    - API keys
    - Credentials
    - Tokens
    - Personal information
    """
    
    # Mask API keys (various formats)
    message = re.sub(
        r'(api[_-]?key[_-]?[:=]\s*)["\']?([a-zA-Z0-9]{20,})["\']?',
        r'\1"***REDACTED***"',
        message,
        flags=re.IGNORECASE
    )
    
    # Mask Azure OpenAI keys
    message = re.sub(
        r'(AZURE[_-]?OPENAI[_-]?API[_-]?KEY[_-]?[:=]\s*)["\']?([a-zA-Z0-9]{20,})["\']?',
        r'\1"***REDACTED***"',
        message,
        flags=re.IGNORECASE
    )
    
    # Mask generic secrets/tokens
    message = re.sub(
        r'(secret[_-]?key|token|password|credential)([_-]?[:=]\s*)["\']?([a-zA-Z0-9]{8,})["\']?',
        r'\1\2"***REDACTED***"',
        message,
        flags=re.IGNORECASE
    )
    
    # Mask Bearer tokens
    message = re.sub(
        r'Bearer\s+[a-zA-Z0-9\-._~+/]+=*',
        'Bearer ***REDACTED***',
        message
    )
    
    # Mask connection strings
    message = re.sub(
        r'(mongodb|postgresql|mysql|redis)://[^@]+@',
        r'\1://***REDACTED***@',
        message,
        flags=re.IGNORECASE
    )
    
    return message


class CosmicFormatter(logging.Formatter):
    """Custom formatter with cosmic styling and security"""
    
    SYMBOLS = {
        logging.DEBUG: "🔍",
        logging.INFO: "✨",
        logging.WARNING: "⚠️ ",
        logging.ERROR: "❌",
        logging.CRITICAL: "🚨",
    }
    
    COLORS = {
        logging.DEBUG: "\\033[36m",      # Cyan
        logging.INFO: "\\033[32m",       # Green
        logging.WARNING: "\\033[33m",    # Yellow
        logging.ERROR: "\\033[31m",      # Red
        logging.CRITICAL: "\\033[35m",   # Magenta
    }
    
    RESET = "\\033[0m"
    
    def format(self, record):
        # Sanitize the message to remove sensitive data
        original_msg = record.getMessage()
        sanitized_msg = sanitize_message(original_msg)
        
        symbol = self.SYMBOLS.get(record.levelno, "📌")
        color = self.COLORS.get(record.levelno, "")
        
        # Format timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Create formatted message
        formatted = f"{color}{symbol} [{timestamp}] {sanitized_msg}{self.RESET}"
        
        return formatted


def setup_logger(name: str = "cosmic_ai") -> logging.Logger:
    """
    Configure and return the cosmic logger with security features
    
    ┌─────────────────────────────────────────────┐
    │  🌟 COSMIC AI Logger                        │
    │  Beautiful, readable, SECURE output         │
    └─────────────────────────────────────────────┘
    """
    
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Console handler with custom formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CosmicFormatter())
    
    logger.addHandler(console_handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger


def print_banner():
    """Print the cosmic startup banner"""
    
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ██████╗ ███████╗███╗   ███╗██╗ ██████╗              ║
║  ██╔════╝██╔═══██╗██╔════╝████╗ ████║██║██╔════╝              ║
║  ██║     ██║   ██║███████╗██╔████╔██║██║██║                   ║
║  ██║     ██║   ██║╚════██║██║╚██╔╝██║██║██║                   ║
║  ╚██████╗╚██████╔╝███████║██║ ╚═╝ ██║██║╚██████╗              ║
║   ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝              ║
║                                                               ║
║         🚀 AI BACKEND - Exploring Knowledge Universe          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    
    console.print(banner, style="bold cyan")


def print_section(title: str):
    """Print a section header"""
    console.print(f"\\n{'─' * 60}", style="dim")
    console.print(f"  🌟 {title}", style="bold cyan")
    console.print(f"{'─' * 60}", style="dim")


def print_success(message: str):
    """Print a success message"""
    # Sanitize before printing
    sanitized = sanitize_message(message)
    console.print(f"  ✅ {sanitized}", style="success")


def print_error(message: str):
    """Print an error message"""
    # Sanitize before printing
    sanitized = sanitize_message(message)
    console.print(f"  ❌ {sanitized}", style="error")


def print_info(message: str):
    """Print an info message"""
    # Sanitize before printing
    sanitized = sanitize_message(message)
    console.print(f"  ℹ️  {sanitized}", style="info")


def print_warning(message: str):
    """Print a warning message"""
    # Sanitize before printing
    sanitized = sanitize_message(message)
    console.print(f"  ⚠️  {sanitized}", style="warning")
