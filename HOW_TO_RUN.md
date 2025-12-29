# 🌌 Cosmic AI Chatbot - Setup & Run Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Testing Azure API](#testing-azure-api)
3. [Running the Backend](#running-the-backend)
4. [Running the Frontend](#running-the-frontend)
5. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

### Required Software
- **Python 3.8+** - For backend
- **Node.js 16+** - For frontend
- **npm** or **yarn** - Package manager for frontend

### Azure OpenAI Requirements
- Azure OpenAI API Key
- Azure OpenAI Endpoint URL
- Deployment names for:
  - Chat model (e.g., `gpt-5-chat`)
  - Embedding model (e.g., `text-embedding-ada-002`)

---

## 🧪 Testing Azure API

Before running the application, verify your Azure OpenAI configuration is working correctly.

### Step 1: Navigate to Backend Directory
```bash
cd Backend
```

### Step 2: Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Run the Test Script
```bash
python test_azure_api.py
```

### Expected Output
The test script will verify:
- ✅ Environment variables are loaded correctly
- ✅ Azure OpenAI client initialization
- ✅ Chat completion endpoint
- ✅ Embedding generation endpoint
- ✅ Streaming chat functionality

### Test Results Interpretation

**All Tests Passed (5/5):**
```
SUCCESS! ALL TESTS PASSED! (5/5)
Your Azure OpenAI API is configured correctly and working!
```
✅ You're ready to run the application!

**Some Tests Failed:**
```
WARNING: SOME TESTS FAILED (4/5 passed)
```
⚠️ Common issues:
- **Rate Limit Error**: Wait a few minutes and try again
- **Invalid Deployment Name**: Check your `.env` file
- **Authentication Error**: Verify your API key

---

## 🚀 Running the Backend

### Method 1: Using the Batch Script (Recommended for Windows)

Simply double-click `backend.bat` or run:
```cmd
backend.bat
```

This script will:
1. Check/create Python virtual environment
2. Install/update dependencies
3. Start the FastAPI server

### Method 2: Manual Setup

#### Step 1: Navigate to Backend Directory
```bash
cd Backend
```

#### Step 2: Create Virtual Environment (if not exists)
```bash
python -m venv venv
```

#### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Start the Server
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Backend URLs
Once running, the backend will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### Verify Backend is Running
Open your browser and navigate to:
```
http://localhost:8000/docs
```
You should see the FastAPI interactive documentation.

---

## 🎨 Running the Frontend

### Method 1: Using the Batch Script (Recommended for Windows)

Simply double-click `frontend.bat` or run:
```cmd
frontend.bat
```

This script will:
1. Check/install node_modules
2. Start the development server

### Method 2: Manual Setup

#### Step 1: Navigate to Frontend Directory
```bash
cd Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main
```

#### Step 2: Install Dependencies (first time only)
```bash
npm install
```

or if you prefer yarn:
```bash
yarn install
```

#### Step 3: Start Development Server
```bash
npm run dev
```

or with yarn:
```bash
yarn dev
```

### Frontend URL
Once running, the frontend will be available at:
- **App**: http://localhost:3000

### Verify Frontend is Running
Open your browser and navigate to:
```
http://localhost:3000
```
You should see the Cosmic AI chatbot interface.

---

## 🔧 Configuration

### Backend Configuration (.env)
Located at: `Backend/.env`

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_BASE=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-chat
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_OPENAI_API_VERSION=2024-02-01
```

### Frontend Configuration (.env)
Located at: `Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main/.env`

```env
VITE_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Backend Issues

#### Issue: "Module not found" error
**Solution:**
```bash
cd Backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Issue: "Port 8000 already in use"
**Solution:**
1. Find and kill the process using port 8000:
```powershell
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

2. Or use a different port:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

#### Issue: Azure API authentication error
**Solution:**
1. Verify your `.env` file has correct credentials
2. Check API key is not expired
3. Ensure endpoint URL is correct (should end with `/`)
4. Run the test script: `python test_azure_api.py`

#### Issue: CORS errors
**Solution:**
The backend is configured to allow CORS from `http://localhost:3000`. If you're using a different port, update `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:YOUR_PORT"],
    ...
)
```

### Frontend Issues

#### Issue: "npm: command not found"
**Solution:**
Install Node.js from https://nodejs.org/

#### Issue: "Cannot find module" errors
**Solution:**
```bash
cd Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main
rm -rf node_modules package-lock.json
npm install
```

#### Issue: "Port 3000 already in use"
**Solution:**
1. Kill the process using port 3000
2. Or the dev server will automatically suggest an alternative port

#### Issue: API connection errors
**Solution:**
1. Ensure backend is running on http://localhost:8000
2. Check frontend `.env` file has correct `VITE_API_URL`
3. Check browser console for CORS errors

---

## 📊 Running Both Simultaneously

### Option 1: Two Terminal Windows

**Terminal 1 - Backend:**
```bash
cd Backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main
npm run dev
```

### Option 2: Batch Scripts

**Windows:**
1. Double-click `backend.bat`
2. Double-click `frontend.bat`

---

## 🧪 Testing the Full Stack

1. **Start Backend**: Run `backend.bat` or manual commands
2. **Verify Backend**: Open http://localhost:8000/docs
3. **Start Frontend**: Run `frontend.bat` or manual commands
4. **Verify Frontend**: Open http://localhost:3000
5. **Test Chat**: Send a message in the chat interface
6. **Test File Upload**: Upload a PDF or DOCX file
7. **Test RAG**: Ask questions about the uploaded document

---

## 📝 Quick Start Commands

### Complete Setup (First Time)

```bash
# Backend Setup
cd Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Test Azure API
python test_azure_api.py

# Start Backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# In a new terminal - Frontend Setup
cd Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main
npm install
npm run dev
```

### Daily Usage (After Setup)

**Using Batch Scripts:**
```bash
# Just double-click both:
backend.bat
frontend.bat
```

**Or manually:**
```bash
# Terminal 1
cd Backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2
cd Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main
npm run dev
```

---

## 🎯 Summary

| Component | Command | URL |
|-----------|---------|-----|
| **Backend** | `backend.bat` or manual uvicorn | http://localhost:8000 |
| **Backend API Docs** | - | http://localhost:8000/docs |
| **Frontend** | `frontend.bat` or `npm run dev` | http://localhost:3000 |
| **Test Azure API** | `python test_azure_api.py` | - |

---

## 🆘 Need Help?

1. **Check Logs**: Both backend and frontend show detailed logs in the terminal
2. **Test Azure API**: Run `python test_azure_api.py` to verify configuration
3. **Check Environment Files**: Ensure `.env` files are properly configured
4. **Verify Ports**: Make sure ports 8000 and 3000 are available
5. **Browser Console**: Check for JavaScript errors in browser developer tools

---

## 🎉 Success Indicators

✅ **Backend Running Successfully:**
- Terminal shows: "Uvicorn running on http://0.0.0.0:8000"
- http://localhost:8000/docs loads successfully
- No error messages in terminal

✅ **Frontend Running Successfully:**
- Terminal shows: "Local: http://localhost:3000"
- Browser opens automatically or http://localhost:3000 loads
- Chat interface is visible

✅ **Full Stack Working:**
- Can send messages in chat
- Can upload files
- Can ask questions about uploaded documents
- Responses appear in chat interface

---

**Happy Chatting! 🌌**
