# Testing & Verification Plan

## 📋 Overview

This plan provides comprehensive testing procedures for the RAG chatbot system, from individual components to end-to-end user flows.

---

## 🎯 Testing Goals

1. Verify Azure OpenAI credentials are working
2. Test document processing pipeline
3. Verify HNSW vector search accuracy
4. Test RAG retrieval quality
5. Validate end-to-end user flows
6. Ensure CORS configuration works
7. Test error handling

---

## 🔐 Phase 1: Azure OpenAI Credential Validation

### Test 1: API Connection Test

**Objective**: Verify Azure OpenAI credentials in `.env` are valid

**Location**: Backend root

**Steps**:
1. Start backend server:
   ```bash
   cd Backend
   uvicorn main:app --reload
   ```

2. Test health endpoint with Azure check:
   ```bash
   curl http://localhost:8000/api/health/azure
   ```

**Expected Output**:
```json
{
  "azure_openai": "connected",
  "status": "healthy"
}
```

**Pass Criteria**: Status is "healthy" and azure_openai is "connected"

---

### Test 2: Embedding Generation Test

**Objective**: Verify embeddings API works

**Create**: `Backend/test_embeddings.py`

```python
import os
from dotenv import load_dotenv
load_dotenv()

from services.embeddings import get_embedding_service

def test_embedding_generation():
    """Test Azure OpenAI embedding generation"""
    
    print("Testing Azure OpenAI Embeddings...")
    
    try:
        service = get_embedding_service()
        
        # Test single embedding
        test_text = "This is a test document about artificial intelligence."
        embedding = service.embed_query(test_text)
        
        print(f"✅ Embedding generated successfully")
        print(f"   Dimension: {len(embedding)}")
        print(f"   Expected: 1536")
        print(f"   Match: {'✅ Yes' if len(embedding) == 1536 else '❌ No'}")
        
        # Test batch embeddings
        test_texts = [
            "First test chunk",
            "Second test chunk",
            "Third test chunk"
        ]
        embeddings = service.embed_texts(test_texts)
        
        print(f"\n✅ Batch embeddings generated")
        print(f"   Shape: {embeddings.shape}")
        print(f"   Expected: (3, 1536)")
        print(f"   Match: {'✅ Yes' if embeddings.shape == (3, 1536) else '❌ No'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_embedding_generation()
    exit(0 if success else 1)
```

**Run**:
```bash
cd Backend
python test_embeddings.py
```

**Pass Criteria**: Both single and batch embeddings return correct dimensions (1536)

---

## 📄 Phase 2: Document Processing Tests

### Test 3: Text Chunking Test

**Objective**: Verify recursive text chunking works correctly

**Create**: `Backend/test_chunking.py`

```python
from services.chunking import get_text_chunker

def test_chunking():
    """Test recursive text chunking"""
    
    print("Testing Recursive Text Chunking...")
    
    # Test document with paragraphs
    test_text = """
    This is the first paragraph of the test document.
    It contains multiple sentences to test chunking.
    The chunker should handle this intelligently.
    
    This is the second paragraph.
    It provides additional context for testing.
    Recursive chunking should split at paragraph boundaries first.
    
    This is the third paragraph with more detailed information.
    The goal is to ensure semantic coherence is maintained.
    Each chunk should be meaningful on its own.
    """ * 20  # Repeat to make it larger
    
    chunker = get_text_chunker()
    chunks = chunker.chunk_text(test_text)
    
    print(f"✅ Text chunked successfully")
    print(f"   Original length: {len(test_text)} chars")
    print(f"   Number of chunks: {len(chunks)}")
    print(f"   Average chunk size: {sum(len(c) for c in chunks) // len(chunks)} chars")
    
    # Verify chunks are not empty
    assert all(len(c) > 0 for c in chunks), "❌ Empty chunks found"
    print("✅ No empty chunks")
    
    # Verify chunks are within reasonable size
    assert all(len(c) < 5000 for c in chunks), "❌ Chunks too large"
    print("✅ All chunks within size limit")
    
    # Print first chunk as sample
    print(f"\nSample chunk:")
    print(f"   {chunks[0][:200]}...")
    
    return True

if __name__ == "__main__":
    success = test_chunking()
    exit(0 if success else 1)
```

**Run**:
```bash
cd Backend
python test_chunking.py
```

**Pass Criteria**: 
- Chunks are created
- No empty chunks
- All chunks within size limit

---

### Test 4: Document Parsing Test

**Objective**: Test PDF, DOCX, TXT parsing

**Create test files**:

`Backend/test_files/test.txt`:
```
This is a test text file.
It has multiple lines.
The parser should read all content.
```

`Backend/test_files/test.pdf`: (Create a simple PDF with text)

**Create**: `Backend/test_parsing.py`

```python
from services.document_processor import DocumentParser
import os

def test_parsing():
    """Test document parsing for different formats"""
    
    print("Testing Document Parsing...")
    
    parser = DocumentParser()
    test_dir = "test_files"
    
    # Test TXT
    txt_path = os.path.join(test_dir, "test.txt")
    if os.path.exists(txt_path):
        text = parser.parse(txt_path)
        print(f"✅ TXT parsed: {len(text)} chars")
    else:
        print(f"⚠️  No test.txt file found")
    
    # Add more format tests as needed
    
    return True

if __name__ == "__main__":
    success = test_parsing()
    exit(0 if success else 1)
```

**Pass Criteria**: All formats parse without errors

---

## 🔍 Phase 3: Vector Database Tests

###Test 5: FAISS Index Creation Test

**Objective**: Verify FAISS index can be created and persisted

**Create**: `Backend/test_vector_store.py`

```python
import numpy as np
from services.vector_store import get_vector_store

def test_vector_store():
    """Test FAISS vector store operations"""
    
    print("Testing FAISS Vector Store...")
    
    vs = get_vector_store()
    
    # Test 1: Add vectors
    print("\n1. Testing add_chunks...")
    test_embeddings = np.random.randn(5, 1536).astype('float32')
    test_chunks = [
        "Artificial intelligence is transforming technology.",
        "Machine learning enables computers to learn from data.",
        "Neural networks are inspired by biological brains.",
        "Deep learning uses multiple layers of processing.",
        "Natural language processing helps computers understand text."
    ]
    
    vs.add_chunks(
        file_id="test-doc-1",
        filename="test.txt",
        chunks=test_chunks,
        embeddings=test_embeddings
    )
    
    print(f"✅ Added {len(test_chunks)} chunks")
    print(f"   Total vectors in index: {vs.index.ntotal}")
    
    # Test 2: Search
    print("\n2. Testing search...")
    query_embedding = np.random.randn(1536).astype('float32')
    results = vs.search(query_embedding, top_k=3)
    
    print(f"✅ Search completed")
    print(f"   Results found: {len(results)}")
    
    for i, result in enumerate(results):
        print(f"   {i+1}. Score: {result['score']:.3f}")
        print(f"      Content: {result['content'][:60]}...")
    
    # Test 3: Document status
    print("\n3. Testing document status...")
    status = vs.get_document_status("test-doc-1")
    print(f"✅ Status retrieved")
    print(f"   Status: {status['status']}")
    print(f"   Chunks: {status['chunks_count']}")
    
    # Test 4: Persistence
    print("\n4. Testing persistence...")
    import os
    index_path = os.path.join("vector_store", "index.faiss")
    exists = os.path.exists(index_path)
    print(f"{'✅' if exists else '❌'} Index persisted to disk: {exists}")
    
    return True

if __name__ == "__main__":
    success = test_vector_store()
    exit(0 if success else 1)
```

**Run**:
```bash
cd Backend
python test_vector_store.py
```

**Pass Criteria**:
- Vectors added successfully
- Search returns results
- Index persisted to disk

---

### Test 6: HNSW Search Accuracy Test

**Objective**: Verify HNSW returns semantically similar results

```python
def test_hnsw_accuracy():
    """Test HNSW search returns semantically similar results"""
    
    from services.vector_store import get_vector_store
    from services.embeddings import get_embedding_service
    
    print("Testing HNSW Search Accuracy...")
    
    vs = get_vector_store()
    emb_service = get_embedding_service()
    
    # Add chunks about AI
    ai_chunks = [
        "Machine learning is a subset of artificial intelligence.",
        "Python is a popular programming language.",
        "Neural networks process information like human brains.",
        "Databases store and organize data efficiently.",
        "Deep learning requires large amounts of training data."
    ]
    
    embeddings = emb_service.embed_texts(ai_chunks)
    vs.add_chunks("test-ai", "ai.txt", ai_chunks, embeddings)
    
    # Query about AI
    query = "What is machine learning?"
    query_emb = emb_service.embed_query(query)
    results = vs.search(query_emb, top_k=2)
    
    print(f"\nQuery: '{query}'")
    print(f"Top results:")
    for i, r in enumerate(results):
        print(f"  {i+1}. (Score: {r['score']:.3f}) {r['content']}")
    
    # Check if most relevant chunk is retrieved
    top_content = results[0]['content']
    assert "machine learning" in top_content.lower(), "❌ Most relevant chunk not retrieved"
    print("\n✅ HNSW correctly retrieved relevant content")
    
    return True

if __name__ == "__main__":
    success = test_hnsw_accuracy()
    exit(0 if success else 1)
```

**Pass Criteria**: Most relevant chunk is in top results

---

## 🔗 Phase 4: API Endpoint Tests

### Test 7: Upload Endpoint Test

**Objective**: Test document upload API

```bash
# Create test file
echo "This is a test document for upload testing." > test_upload.txt

# Upload file
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test_upload.txt" \
  -v
```

**Expected Output**:
```json
{
  "filename": "test_upload.txt",
  "file_id": "uuid-here",
  "size": 46,
  "status": "uploaded"
}
```

**Pass Criteria**: 
- HTTP 200 response
- file_id returned
- status is "uploaded"

---

### Test 8: Analyze Endpoint Test

**Objective**: Test document analysis API

```bash
# Use file_id from previous test
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_id":"<file_id_here>"}' \
  -v

# Check status
curl http://localhost:8000/api/analyze/status/<file_id_here>
```

**Expected Output**:
```json
{
  "file_id": "uuid-here",
  "status": "completed",
  "chunks_count": 1
}
```

**Pass Criteria**: Status becomes "completed" after processing

---

### Test 9: Chat Endpoint Test

**Objective**: Test RAG chat endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is in the uploaded document?",
    "use_rag": true,
    "file_ids": ["<file_id_here>"]
  }' \
  -v
```

**Expected Output**:
```json
{
  "response": "Based on the uploaded document...",
  "retrieved_chunks": [...]
}
```

**Pass Criteria**: 
- Response references document content
- retrieved_chunks contains relevant snippets

---

## 🌐 Phase 5: CORS & Integration Tests

### Test 10: CORS Configuration Test

**Objective**: Verify frontend can make requests

```bash
# Test OPTIONS preflight
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS http://localhost:8000/api/upload \
     -v
```

**Expected Headers**:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: POST, GET, OPTIONS
```

**Pass Criteria**: CORS headers present

---

## 🎭 Phase 6: End-to-End User Flow Tests

### Test 11: Complete RAG Flow (Manual)

**Objective**: Test complete user journey

**Steps**:

1. **Start Backend**:
   ```bash
   cd Backend
   uvicorn main:app --reload
   ```

2. **Start Frontend**:
   ```bash
   cd Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main
   npm run dev
   ```

3. **User Actions**:
   - Open `http://localhost:3000`
   - Click "Upload Document"
   - Select a PDF/TXT file
   - Wait for upload (spinner appears)
   - Click "Analyze" button
   - Wait for analysis (shows "Analyzing...")
   - See green checkmark when complete
   - Type a question about the document
   - Press Enter
   - Watch streaming response appear

**Pass Criteria**:
- ✅ Upload works without errors
- ✅ Analysis completes successfully
- ✅ Chat response references document content
- ✅ Streaming works smoothly
- ✅ No console errors

---

### Test 12: Error Handling (Manual)

**Test Scenarios**:

1. **File Too Large**:
   - Upload 15MB file
   - Expect: Error toast notification

2. **Invalid File Type**:
   - Upload .exe file
   - Expect: Error toast notification

3. **Backend Down**:
   - Stop backend server
   - Try to upload
   - Expect: Network error message

4. **Invalid API Key**:
   - Temporarily break Azure API key in .env
   - Try analysis
   - Expect: Graceful error message

**Pass Criteria**: All errors handled gracefully with user feedback

---

## 📊 Phase 7: Performance Tests

### Test 13: Large Document Test

**Objective**: Test system with large documents

**Steps**:
1. Create large test document (5000+ words)
2. Upload and analyze
3. Measure processing time

**Success Metrics**:
- Processing completes within 30 seconds
- No memory errors
- All chunks embedded successfully

---

### Test 14: Multiple Document Test

**Objective**: Test with multiple documents

**Steps**:
1. Upload 5 different documents
2. Analyze all
3. Query across all documents

**Success Metrics**:
- All documents process successfully
- Search returns results from multiple docs
- Response time <200ms for search

---

## ✅ Final Verification Checklist

### Backend
- [ ] Azure OpenAI credentials work
- [ ] Embeddings generate correctly (1536 dims)
- [ ] Recursive chunking produces semantic chunks
- [ ] FAISS index created successfully
- [ ] HNSW search returns relevant results
- [ ] All API endpoints respond correctly
- [ ] CORS headers configured properly
- [ ] Error handling works

### Frontend
- [ ] Upload UI appears
- [ ] File validation works
- [ ] Upload progress shows
- [ ] Analyze button triggers processing
- [ ] Analysis status polls correctly
- [ ] Completion shows checkmark
- [ ] Chat integrates with backend
- [ ] Streaming responses work
- [ ] Error states display
- [ ] Cosmic theme maintained

### Integration
- [ ] End-to-end flow works smoothly
- [ ] No CORS errors
- [ ] Streaming is smooth
- [ ] Error handling is graceful
- [ ] Performance is acceptable

---

## 🚨 Known Issues & Limitations

1. **FAISS Deletion**: FAISS doesn't support native deletion; requires index rebuild
2. **Embedding Caching**: No caching currently; may hit rate limits with heavy use
3. **File Size**: 10MB limit may be small for some documents
4. **Concurrent Users**: Single vector store instance; may need locking for production

---

## 📝 Test Reporting

Create test report template:

```markdown
# RAG Chatbot Test Report

Date: YYYY-MM-DD
Tester: [Name]

## Phase 1: Azure OpenAI ✅/❌
- [ ] Connection Test
- [ ] Embedding Generation

## Phase 2: Document Processing ✅/❌
- [ ] Text Chunking
- [ ] Document Parsing

## Phase 3: Vector Database ✅/❌
- [ ] Index Creation
- [ ] HNSW Search

## Phase 4: API Endpoints ✅/❌
- [ ] Upload
- [ ] Analyze
- [ ] Chat

## Phase 5: Integration ✅/❌
- [ ] CORS
- [ ] End-to-End Flow

## Issues Found:
1. [Issue description]
2. [Issue description]

## Overall Status: [Pass/Fail/Partial]
```

---

## 📌 Next Steps After Testing

1. Document any bugs found
2. Fix critical issues
3. Optimize performance bottlenecks
4. Add monitoring and logging
5. Prepare for deployment
