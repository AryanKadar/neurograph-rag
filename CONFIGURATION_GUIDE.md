# 🌌 Cosmic AI - Configuration Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Azure OpenAI Configuration](#azure-openai-configuration)
3. [GPT-5 Model Settings](#gpt-5-model-settings)
4. [RAG Configuration](#rag-configuration)
5. [Vector Database Settings](#vector-database-settings)
6. [File Upload Settings](#file-upload-settings)
7. [Server Configuration](#server-configuration)
8. [Logging & Monitoring](#logging--monitoring)
9. [Optimization Tips](#optimization-tips)

---

## 🎯 Overview

This guide explains all configuration parameters in the `Backend/.env` file and how they affect the Cosmic AI chatbot's performance.

**Location:** `Backend/.env`

All settings are automatically loaded into the application through `config/settings.py`.

---

## 🔐 Azure OpenAI Configuration

### Core Settings

```env
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_BASE=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-chat
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_OPENAI_API_VERSION=2024-02-01
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | Required |
| `AZURE_OPENAI_API_BASE` | Azure endpoint URL | Required |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Chat model deployment name | `gpt-5-chat` |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | Embedding model deployment | `text-embedding-ada-002` |
| `AZURE_OPENAI_API_VERSION` | API version to use | `2024-02-01` |

---

## 🤖 GPT-5 Model Settings

### Token Limits

```env
GPT_MAX_COMPLETION_TOKENS=4000
GPT_MAX_CONTEXT_TOKENS=120000
GPT_RESERVED_TOKENS=2000
```

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `GPT_MAX_COMPLETION_TOKENS` | Maximum tokens in response | `4000` | 100-8000 |
| `GPT_MAX_CONTEXT_TOKENS` | Maximum total context window | `120000` | Up to 128K |
| `GPT_RESERVED_TOKENS` | Tokens reserved for system prompts | `2000` | 500-5000 |

**💡 Tips:**
- **Higher completion tokens** = Longer, more detailed responses
- **Lower completion tokens** = Faster responses, lower costs
- GPT-5 supports up to **128K context window** (120K used by default for safety)

### Temperature & Creativity

```env
GPT_TEMPERATURE=0.7
GPT_TOP_P=0.95
GPT_FREQUENCY_PENALTY=0.0
GPT_PRESENCE_PENALTY=0.0
```

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `GPT_TEMPERATURE` | Response randomness/creativity | `0.7` | 0.0-2.0 |
| `GPT_TOP_P` | Nucleus sampling threshold | `0.95` | 0.0-1.0 |
| `GPT_FREQUENCY_PENALTY` | Reduce repetition of tokens | `0.0` | -2.0-2.0 |
| `GPT_PRESENCE_PENALTY` | Encourage new topics | `0.0` | -2.0-2.0 |

**💡 Temperature Guide:**
- **0.0-0.3**: Focused, deterministic, factual
- **0.4-0.7**: Balanced (recommended for RAG)
- **0.8-1.0**: Creative, varied responses
- **1.1-2.0**: Very creative, unpredictable

**💡 Top-P Guide:**
- **0.9-0.95**: Recommended (balanced diversity)
- **0.95-1.0**: More diverse responses
- **0.5-0.9**: More focused responses

### Response Settings

```env
GPT_STREAM_ENABLED=true
GPT_STREAMING_CHUNK_SIZE=5
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `GPT_STREAM_ENABLED` | Enable streaming responses | `true` |
| `GPT_STREAMING_CHUNK_SIZE` | Characters per stream chunk | `5` |

---

## 🧠 RAG Configuration

### Chunking Settings

```env
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MIN_CHUNK_SIZE=100
```

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `CHUNK_SIZE` | Target chunk size in tokens | `1000` | 500-2000 |
| `CHUNK_OVERLAP` | Overlap between chunks | `200` | 50-500 |
| `MIN_CHUNK_SIZE` | Minimum chunk size to keep | `100` | 50-300 |

**💡 Chunking Guide:**
- **Larger chunks** (1500-2000): Better for long-form content, technical docs
- **Medium chunks** (800-1200): Balanced (recommended)
- **Smaller chunks** (500-800): Better for Q&A, precise retrieval

**Overlap Guide:**
- Set overlap to **15-25% of chunk size**
- Higher overlap = Better context preservation
- Lower overlap = More unique chunks, faster processing

### Retrieval Settings

```env
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7
MAX_CONTEXT_CHUNKS=8
```

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `TOP_K_RESULTS` | Number of chunks to retrieve | `5` | 3-10 |
| `SIMILARITY_THRESHOLD` | Minimum similarity score | `0.7` | 0.5-0.9 |
| `MAX_CONTEXT_CHUNKS` | Max chunks sent to GPT | `8` | 3-15 |

**💡 Retrieval Guide:**
- **TOP_K_RESULTS**: More results = Better coverage, but more tokens used
- **SIMILARITY_THRESHOLD**: 
  - 0.8-0.9: Very strict (only highly relevant)
  - 0.7-0.8: Balanced (recommended)
  - 0.5-0.7: Lenient (more context, some noise)

---

## 🔍 Vector Database Settings

### FAISS HNSW Configuration

```env
HNSW_M=32
HNSW_EF_CONSTRUCTION=200
HNSW_EF_SEARCH=100
EMBEDDING_DIMENSION=1536
```

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `HNSW_M` | Connections per layer | `32` | 16-64 |
| `HNSW_EF_CONSTRUCTION` | Construction accuracy | `200` | 100-500 |
| `HNSW_EF_SEARCH` | Search accuracy | `100` | 50-200 |
| `EMBEDDING_DIMENSION` | Embedding vector size | `1536` | Fixed |

**💡 HNSW Performance Guide:**

**HNSW_M** (Connections per layer):
- **16**: Faster, less accurate
- **32**: Balanced (recommended)
- **48-64**: Slower, more accurate

**HNSW_EF_CONSTRUCTION** (Build-time accuracy):
- Higher = Better index quality, slower indexing
- **100-200**: Good for most cases
- **200-500**: High-quality index for large datasets

**HNSW_EF_SEARCH** (Search-time accuracy):
- Higher = More accurate search, slower
- **50-100**: Fast searches, good accuracy
- **100-200**: Very accurate, slower

---

## 📁 File Upload Settings

```env
MAX_FILE_SIZE_MB=25
ALLOWED_FILE_TYPES=pdf,docx,txt,md
MAX_FILES_PER_UPLOAD=5
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `MAX_FILE_SIZE_MB` | Max file size in MB | `25` |
| `ALLOWED_FILE_TYPES` | Comma-separated file extensions | `pdf,docx,txt,md` |
| `MAX_FILES_PER_UPLOAD` | Max concurrent file uploads | `5` |

---

## 🌐 Server Configuration

```env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:3000` |
| `SERVER_HOST` | Server bind address | `0.0.0.0` |
| `SERVER_PORT` | Server port | `8000` |

---

## 📊 Logging & Monitoring

```env
LOG_LEVEL=INFO
ENABLE_DEBUG_LOGGING=false
LOG_API_CALLS=true
```

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `LOG_LEVEL` | Logging verbosity | `INFO` | DEBUG, INFO, WARNING, ERROR |
| `ENABLE_DEBUG_LOGGING` | Extra debug output | `false` | true, false |
| `LOG_API_CALLS` | Log API requests | `true` | true, false |

---

## 🎯 Optimization Tips

### For Best Performance

```env
# Balanced performance and quality
GPT_MAX_COMPLETION_TOKENS=3000
GPT_TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
HNSW_M=32
HNSW_EF_SEARCH=100
```

### For Maximum Quality

```env
# Prioritize accuracy over speed
GPT_MAX_COMPLETION_TOKENS=4000
GPT_TEMPERATURE=0.5
CHUNK_SIZE=800
CHUNK_OVERLAP=250
TOP_K_RESULTS=7
SIMILARITY_THRESHOLD=0.75
HNSW_M=48
HNSW_EF_SEARCH=150
```

### For Speed & Cost Optimization

```env
# Faster responses, lower costs
GPT_MAX_COMPLETION_TOKENS=2000
GPT_TEMPERATURE=0.7
CHUNK_SIZE=1200
CHUNK_OVERLAP=150
TOP_K_RESULTS=3
HNSW_M=24
HNSW_EF_SEARCH=75
```

### For Large Documents

```env
# Better for processing big files
CHUNK_SIZE=1500
CHUNK_OVERLAP=300
MAX_FILE_SIZE_MB=50
TOP_K_RESULTS=8
MAX_CONTEXT_CHUNKS=10
```

---

## 📈 Performance Impact Summary

| Setting | Higher Value Impact | Lower Value Impact |
|---------|-------------------|-------------------|
| **GPT_MAX_COMPLETION_TOKENS** | Longer responses, higher cost | Shorter responses, faster |
| **GPT_TEMPERATURE** | More creative, varied | More focused, deterministic |
| **CHUNK_SIZE** | Better context, fewer chunks | More granular, more chunks |
| **TOP_K_RESULTS** | More context, higher cost | Faster, less context |
| **HNSW_M** | Better accuracy, slower | Faster, less accurate |
| **HNSW_EF_SEARCH** | More accurate search | Faster search |

---

## 🔄 Applying Configuration Changes

After modifying `.env`:

1. **Save the file**
2. **Restart the backend**:
   ```bash
   # Stop the backend (Ctrl+C)
   # Then restart
   cd Backend
   .\venv\Scripts\Activate.ps1
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   Or simply run:
   ```bash
   .\backend.bat
   ```

3. **Verify changes** in the logs when the server starts

---

## ✅ Validation

To verify your configuration is working:

```bash
cd Backend
.\venv\Scripts\Activate.ps1
python simple_test.py
```

This will test:
- ✅ Environment variables loaded
- ✅ Azure OpenAI connection
- ✅ GPT-5 chat working
- ✅ All settings applied correctly

---

## 🆘 Troubleshooting

### Configuration Not Loading

1. Check `.env` file location: `Backend/.env`
2. No spaces around `=` in `.env`
3. Boolean values must be lowercase: `true` or `false`
4. Lists use commas without spaces: `pdf,docx,txt`

### Performance Issues

- **Slow responses**: Reduce `TOP_K_RESULTS` and `GPT_MAX_COMPLETION_TOKENS`
- **Poor quality**: Increase `SIMILARITY_THRESHOLD` and `TOP_K_RESULTS`
- **Out of memory**: Reduce `CHUNK_SIZE` and `MAX_FILES_PER_UPLOAD`

---

**Happy configuring! 🌌**
