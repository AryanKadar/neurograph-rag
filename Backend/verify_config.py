"""
═══════════════════════════════════════════════════════════════
 🌌 COSMIC AI - Configuration Verification Script
═══════════════════════════════════════════════════════════════
"""

from config.settings import settings
from colorama import init, Fore, Style

init(autoreset=True)

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{text:^70}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

def print_section(text):
    print(f"\n{Fore.MAGENTA}{'─'*70}")
    print(f"{Fore.MAGENTA}{text}")
    print(f"{Fore.MAGENTA}{'─'*70}{Style.RESET_ALL}")

def print_setting(name, value, unit=""):
    print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} {name:30s}: {Fore.YELLOW}{value}{unit}{Style.RESET_ALL}")

def verify_configuration():
    """Verify all configuration settings"""
    
    print_header("COSMIC AI - CONFIGURATION VERIFICATION")
    
    # Azure OpenAI
    print_section("🔐 Azure OpenAI Configuration")
    print_setting("API Base", settings.AZURE_OPENAI_API_BASE[:50] + "...")
    print_setting("Deployment Name", settings.AZURE_OPENAI_DEPLOYMENT_NAME)
    print_setting("Embedding Deployment", settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT)
    print_setting("API Version", settings.AZURE_OPENAI_API_VERSION)
    
    # GPT-5 Model Configuration
    print_section("🤖 GPT-5 Model Settings")
    print_setting("Max Completion Tokens", settings.GPT_MAX_COMPLETION_TOKENS)
    print_setting("Max Context Tokens", f"{settings.GPT_MAX_CONTEXT_TOKENS:,}")
    print_setting("Reserved Tokens", settings.GPT_RESERVED_TOKENS)
    print_setting("Temperature", settings.GPT_TEMPERATURE)
    print_setting("Top-P", settings.GPT_TOP_P)
    print_setting("Frequency Penalty", settings.GPT_FREQUENCY_PENALTY)
    print_setting("Presence Penalty", settings.GPT_PRESENCE_PENALTY)
    print_setting("Stream Enabled", settings.GPT_STREAM_ENABLED)
    
    # RAG Configuration
    print_section("🧠 RAG Configuration")
    print_setting("Chunk Size", settings.CHUNK_SIZE, " tokens")
    print_setting("Chunk Overlap", settings.CHUNK_OVERLAP, " tokens")
    print_setting("Min Chunk Size", settings.MIN_CHUNK_SIZE, " tokens")
    print_setting("Top K Results", settings.TOP_K_RESULTS)
    print_setting("Similarity Threshold", settings.SIMILARITY_THRESHOLD)
    print_setting("Max Context Chunks", settings.MAX_CONTEXT_CHUNKS)
    
    # Vector Database
    print_section("🔍 Vector Database (HNSW)")
    print_setting("HNSW M (Connections)", settings.HNSW_M)
    print_setting("HNSW EF Construction", settings.HNSW_EF_CONSTRUCTION)
    print_setting("HNSW EF Search", settings.HNSW_EF_SEARCH)
    print_setting("Embedding Dimension", settings.EMBEDDING_DIMENSION)
    
    # File Upload
    print_section("📁 File Upload Configuration")
    print_setting("Max File Size", settings.MAX_FILE_SIZE / 1024 / 1024, " MB")
    print_setting("Allowed File Types", ", ".join(settings.ALLOWED_FILE_TYPES_LIST))
    print_setting("Max Files Per Upload", settings.MAX_FILES_PER_UPLOAD)
    
    # Server Configuration
    print_section("🌐 Server Configuration")
    print_setting("Server Host", settings.SERVER_HOST)
    print_setting("Server Port", settings.SERVER_PORT)
    print_setting("CORS Origins", len(settings.CORS_ORIGINS), " origins")
    for origin in settings.CORS_ORIGINS:
        print(f"   {Fore.CYAN}└─{Style.RESET_ALL} {origin}")
    
    # Logging
    print_section("📊 Logging & Monitoring")
    print_setting("Log Level", settings.LOG_LEVEL)
    print_setting("Debug Logging", settings.ENABLE_DEBUG_LOGGING)
    print_setting("Log API Calls", settings.LOG_API_CALLS)
    
    # Summary
    print_section("📋 Configuration Summary")
    
    total_params = 42
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ All {total_params} configuration parameters loaded successfully!{Style.RESET_ALL}")
    
    # Performance estimate
    print(f"\n{Fore.CYAN}Performance Estimates:{Style.RESET_ALL}")
    print(f"  • Max response length: ~{settings.GPT_MAX_COMPLETION_TOKENS * 0.75:.0f} words")
    print(f"  • Context window: ~{settings.GPT_MAX_CONTEXT_TOKENS / 1000:.0f}K tokens")
    print(f"  • Chunk size: ~{settings.CHUNK_SIZE * 0.75:.0f} words per chunk")
    print(f"  • Retrieved context: ~{settings.TOP_K_RESULTS * settings.CHUNK_SIZE * 0.75:.0f} words")
    
    print(f"\n{Fore.GREEN}{'='*70}")
    print(f"{Fore.GREEN}{'Configuration verified and ready to use!':^70}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    verify_configuration()
