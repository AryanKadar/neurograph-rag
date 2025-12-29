"""Simple Azure OpenAI API Test"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

print("\n" + "="*70)
print("AZURE OPENAI GPT-5-CHAT TEST")
print("="*70 + "\n")

# Get config from .env
api_key = os.getenv('AZURE_OPENAI_API_KEY')
api_base = os.getenv('AZURE_OPENAI_API_BASE')
deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')

print(f"Deployment Name: {deployment}")
print(f"API Base: {api_base}")
print(f"API Version: {api_version}")
print(f"API Key: {api_key[:10]}...{api_key[-10:]}\n")

try:
    # Initialize client
    print("Initializing Azure OpenAI client...")
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=api_base
    )
    print("✓ Client initialized successfully!\n")
    
    # Test chat completion
    print("Testing chat completion with GPT-5-chat...")
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello! Azure GPT-5-chat is working perfectly!' if you can read this."}
        ],
        max_tokens=100,
        temperature=0.7
    )
    
    message = response.choices[0].message.content
    print("✓ Chat completion successful!\n")
    print(f"Response: {message}\n")
    print(f"Tokens used - Prompt: {response.usage.prompt_tokens}, Completion: {response.usage.completion_tokens}, Total: {response.usage.total_tokens}")
    
    print("\n" + "="*70)
    print("SUCCESS! GPT-5-CHAT IS WORKING!")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}\n")
    print(f"Error type: {type(e).__name__}\n")
    print("="*70)
    print("TEST FAILED")
    print("="*70 + "\n")
