"""
===================================================================
Azure OpenAI API Configuration Test
===================================================================
This script tests the Azure OpenAI API configuration to ensure:
1. Environment variables are loaded correctly
2. API credentials are valid
3. Chat completion endpoint works
4. Embedding endpoint works
5. Connection to Azure is successful
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{text:^70}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}[OK] {text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}[ERROR] {text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}[INFO] {text}{Style.RESET_ALL}")

def test_environment_variables():
    """Test if all required environment variables are set"""
    print_header("Testing Environment Variables")
    
    required_vars = {
        'AZURE_OPENAI_API_KEY': os.getenv('AZURE_OPENAI_API_KEY'),
        'AZURE_OPENAI_API_BASE': os.getenv('AZURE_OPENAI_API_BASE'),
        'AZURE_OPENAI_DEPLOYMENT_NAME': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
        'AZURE_OPENAI_EMBEDDING_DEPLOYMENT': os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT'),
        'AZURE_OPENAI_API_VERSION': os.getenv('AZURE_OPENAI_API_VERSION')
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value:
            # Mask API key for security
            if 'KEY' in var_name:
                masked_value = var_value[:10] + '...' + var_value[-10:] if len(var_value) > 20 else '***'
                print_success(f"{var_name}: {masked_value}")
            else:
                print_success(f"{var_name}: {var_value}")
        else:
            print_error(f"{var_name}: NOT SET")
            all_set = False
    
    return all_set, required_vars

def test_azure_client_initialization(config):
    """Test Azure OpenAI client initialization"""
    print_header("Testing Azure OpenAI Client Initialization")
    
    try:
        client = AzureOpenAI(
            api_key=config['AZURE_OPENAI_API_KEY'],
            api_version=config['AZURE_OPENAI_API_VERSION'],
            azure_endpoint=config['AZURE_OPENAI_API_BASE']
        )
        print_success("Azure OpenAI client initialized successfully")
        return client
    except Exception as e:
        print_error(f"Failed to initialize Azure OpenAI client: {str(e)}")
        return None

def test_chat_completion(client, deployment_name):
    """Test chat completion endpoint"""
    print_header("Testing Chat Completion Endpoint")
    
    try:
        print_info("Sending test message to chat completion endpoint...")
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, Azure API is working!' if you can read this."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        message = response.choices[0].message.content
        print_success("Chat completion successful!")
        print(f"{Fore.CYAN}Response: {Style.RESET_ALL}{message}")
        
        # Print usage statistics
        print(f"\n{Fore.MAGENTA}Usage Statistics:{Style.RESET_ALL}")
        print(f"  Prompt tokens: {response.usage.prompt_tokens}")
        print(f"  Completion tokens: {response.usage.completion_tokens}")
        print(f"  Total tokens: {response.usage.total_tokens}")
        
        return True
    except Exception as e:
        print_error(f"Chat completion failed: {str(e)}")
        print_info(f"Error type: {type(e).__name__}")
        return False

def test_embedding(client, embedding_deployment):
    """Test embedding endpoint"""
    print_header("Testing Embedding Endpoint")
    
    try:
        print_info("Generating test embedding...")
        
        response = client.embeddings.create(
            model=embedding_deployment,
            input="This is a test sentence for embedding generation."
        )
        
        embedding = response.data[0].embedding
        print_success("Embedding generation successful!")
        print(f"{Fore.CYAN}Embedding dimension: {Style.RESET_ALL}{len(embedding)}")
        print(f"{Fore.CYAN}First 5 values: {Style.RESET_ALL}{embedding[:5]}")
        
        # Print usage statistics
        print(f"\n{Fore.MAGENTA}Usage Statistics:{Style.RESET_ALL}")
        print(f"  Prompt tokens: {response.usage.prompt_tokens}")
        print(f"  Total tokens: {response.usage.total_tokens}")
        
        return True
    except Exception as e:
        print_error(f"Embedding generation failed: {str(e)}")
        print_info(f"Error type: {type(e).__name__}")
        return False

def test_streaming_chat(client, deployment_name):
    """Test streaming chat completion"""
    print_header("Testing Streaming Chat Completion")
    
    try:
        print_info("Testing streaming response...")
        
        stream = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": "Count from 1 to 5."}
            ],
            max_tokens=50,
            temperature=0.7,
            stream=True
        )
        
        print(f"{Fore.CYAN}Streaming response: {Style.RESET_ALL}", end="")
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        print()  # New line after streaming
        print_success("Streaming chat completion successful!")
        return True
    except Exception as e:
        print_error(f"Streaming chat failed: {str(e)}")
        print_info(f"Error type: {type(e).__name__}")
        return False

def main():
    """Main test function"""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}")
    print("=" * 70)
    print("     AZURE OPENAI API CONFIGURATION TEST")
    print("=" * 70)
    print(f"{Style.RESET_ALL}")
    
    # Test 1: Environment Variables
    env_vars_ok, config = test_environment_variables()
    if not env_vars_ok:
        print_error("\nEnvironment variables test failed. Please check your .env file.")
        sys.exit(1)
    
    # Test 2: Client Initialization
    client = test_azure_client_initialization(config)
    if not client:
        print_error("\nClient initialization failed. Please check your API credentials.")
        sys.exit(1)
    
    # Test 3: Chat Completion
    chat_ok = test_chat_completion(client, config['AZURE_OPENAI_DEPLOYMENT_NAME'])
    
    # Test 4: Embedding
    embedding_ok = test_embedding(client, config['AZURE_OPENAI_EMBEDDING_DEPLOYMENT'])
    
    # Test 5: Streaming Chat
    streaming_ok = test_streaming_chat(client, config['AZURE_OPENAI_DEPLOYMENT_NAME'])
    
    # Final Summary
    print_header("Test Summary")
    
    tests = [
        ("Environment Variables", env_vars_ok),
        ("Client Initialization", client is not None),
        ("Chat Completion", chat_ok),
        ("Embedding Generation", embedding_ok),
        ("Streaming Chat", streaming_ok)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Fore.CYAN}{'-'*70}{Style.RESET_ALL}")
    
    if passed == total:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}SUCCESS! ALL TESTS PASSED! ({passed}/{total}){Style.RESET_ALL}")
        print(f"{Fore.GREEN}Your Azure OpenAI API is configured correctly and working!{Style.RESET_ALL}\n")
        return 0
    else:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}WARNING: SOME TESTS FAILED ({passed}/{total} passed){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please review the errors above and fix the configuration.{Style.RESET_ALL}\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Test interrupted by user.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
