# Frontend Integration Plan - React + Cosmic UI

## 📋 Overview

This plan details the frontend modifications to integrate the RAG chatbot backend with the existing Cosmic AI interface running on **port 3000**.

---

## 🎯 Goals

1. Add document upload functionality to the chat interface
2. Add "Analyze" button to trigger document processing
3. Integrate backend API calls with React Query
4. Handle streaming chat responses from FastAPI
5. Display processing status and feedback
6. Maintain the beautiful cosmic theme and animations

---

## 📁 Current Frontend State

### Location
`c:\Users\aryan\OneDrive\Desktop\Simple_ChatBot\Frontend\cosmic-chat-ai-main\cosmic-chat-ai-main\src`

### Tech Stack
- **Framework**: Vite + React 18 + TypeScript
- **Styling**: TailwindCSS + shadcn/ui components
- **Animations**: Framer Motion
- **API**: React Query (@tanstack/react-query)
- **Routing**: React Router DOM
- **Theme**: Next Themes (dark mode support)

### Key Components
- `ChatContainer.tsx` - Main chat interface
- `ChatInput.tsx` - Message input
- `ChatMessage.tsx` - Message display
- `CosmicBackground.tsx` - Animated background

---

## 🔧 Required Changes

### 1. Environment Configuration

Create `.env` file in frontend root:

**Location**: `c:\Users\aryan\OneDrive\Desktop\Simple_ChatBot\Frontend\cosmic-chat-ai-main\cosmic-chat-ai-main\.env`

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_MAX_FILE_SIZE=10485760
VITE_ALLOWED_FILE_TYPES=.pdf,.txt,.docx,.md
```

### 2. API Client Setup

Create new file: `src/services/api.ts`

```typescript
// API client configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = {
  baseUrl: API_BASE_URL,
  
  // Upload document
  uploadDocument: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  // Analyze document
  analyzeDocument: async (fileId: string): Promise<AnalyzeResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_id: fileId }),
    });
    
    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  // Check analysis status
  getAnalysisStatus: async (fileId: string): Promise<StatusResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/analyze/status/${fileId}`);
    
    if (!response.ok) {
      throw new Error(`Status check failed: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  // Get document preview info
  getDocumentContent: async (fileId: string): Promise<DocumentContentResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/documents/${fileId}/view`);
    
    if (!response.ok) {
      throw new Error(`Content fetch failed: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  // Send chat message (non-streaming)
  sendMessage: async (query: string, history: any[] = [], useRag: boolean = true, fileIds?: string[]): Promise<ChatResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        query, 
        history, // Send last few messages
        use_rag: useRag, 
        file_ids: fileIds 
      }),
    });
    
    if (!response.ok) {
      throw new Error(`Chat failed: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  // Send chat message (streaming)
  streamMessage: async function* (
    query: string, 
    history: any[] = [], 
    summary: string = "", // Support for hybrid memory
    useRag: boolean = true, 
    fileIds?: string[]
  ): AsyncGenerator<string> {
    const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        query, 
        history, 
        current_summary: summary,
        use_rag: useRag, 
        file_ids: fileIds 
      }),
    });
    
    if (!response.ok) {
      throw new Error(`Chat streaming failed: ${response.statusText}`);
    }
    
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    
    if (!reader) {
      throw new Error('No reader available');
    }
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') continue;
          yield data;
        }
      }
    }
  }
};

// Type definitions
export interface UploadResponse {
  filename: string;
  file_id: string;
  size: number;
  status: string;
}

export interface AnalyzeResponse {
  file_id: string;
  status: string;
  message: string;
}

export interface StatusResponse {
  file_id: string;
  status: string;
  chunks_count: number;
}

export interface ChatResponse {
  response: string;
  retrieved_chunks?: Array<{
    content: string;
    score: number;
    file_id: string;
    chunk_index: number;
  }>;
  model: string;
  timestamp: string;
}

export interface DocumentContentResponse {
  file_id: string;
  filename: string;
  content: string; // Base64 for binary or raw text
  mimetype: string;
}
```

### 3. Document Upload Component

Create new file: `src/components/DocumentUpload.tsx`

```typescript
import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, File, X, CheckCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { apiClient } from '@/services/api';

interface DocumentUploadProps {
  onUploadComplete?: (fileId: string, filename: string) => void;
}

const DocumentUpload = ({ onUploadComplete }: DocumentUploadProps) => {
  const [files, setFiles] = useState<Array<{ id: string; name: string; status: 'uploading' | 'uploaded' | 'analyzing' | 'completed' | 'error' }>>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(event.target.files || []);
    
    for (const file of selectedFiles) {
      // Validate file size
      const maxSize = parseInt(import.meta.env.VITE_MAX_FILE_SIZE || '10485760');
      if (file.size > maxSize) {
        toast({
          title: "File too large",
          description: `${file.name} exceeds 10MB limit`,
          variant: "destructive",
        });
        continue;
      }
      
      // Validate file type
      const ext = `.${file.name.split('.').pop()?.toLowerCase()}`;
      const allowed = (import.meta.env.VITE_ALLOWED_FILE_TYPES || '.pdf,.txt,.docx,.md').split(',');
      if (!allowed.includes(ext)) {
        toast({
          title: "Invalid file type",
          description: `${file.name} is not a supported format`,
          variant: "destructive",
        });
        continue;
      }
      
      // Add to files list
      const tempId = `temp-${Date.now()}-${Math.random()}`;
      setFiles(prev => [...prev, { id: tempId, name: file.name, status: 'uploading' }]);
      
      try {
        // Upload
        const uploadResult = await apiClient.uploadDocument(file);
        
        // Update status to uploaded
        setFiles(prev => prev.map(f => 
          f.id === tempId 
            ? { ...f, id: uploadResult.file_id, status: 'uploaded' as const }
            : f
        ));
        
        toast({
          title: "Upload successful",
          description: `${file.name} uploaded successfully`,
        });
        
      } catch (error) {
        console.error('Upload failed:', error);
        setFiles(prev => prev.map(f => 
          f.id === tempId ? { ...f, status: 'error' as const } : f
        ));
        
        toast({
          title: "Upload failed",
          description: `Failed to upload ${file.name}`,
          variant: "destructive",
        });
      }
    }
    
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleAnalyze = async (fileId: string, filename: string) => {
    setFiles(prev => prev.map(f => 
      f.id === fileId ? { ...f, status: 'analyzing' as const } : f
    ));
    
    try {
      await apiClient.analyzeDocument(fileId);
      
      // Poll for completion
      const pollInterval = setInterval(async () => {
        try {
          const status = await apiClient.getAnalysisStatus(fileId);
          
          if (status.status === 'completed') {
            clearInterval(pollInterval);
            setFiles(prev => prev.map(f => 
              f.id === fileId ? { ...f, status: 'completed' as const } : f
            ));
            
            toast({
              title: "Analysis complete",
              description: `${filename} analyzed: ${status.chunks_count} chunks`,
            });
            
            onUploadComplete?.(fileId, filename);
          }
        } catch (error) {
          clearInterval(pollInterval);
          console.error('Status check failed:', error);
        }
      }, 2000);
      
    } catch (error) {
      console.error('Analysis failed:', error);
      setFiles(prev => prev.map(f => 
        f.id === fileId ? { ...f, status: 'error' as const } : f
      ));
      
      toast({
        title: "Analysis failed",
        description: `Failed to analyze ${filename}`,
        variant: "destructive",
      });
    }
  };

  const handleRemove = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-4"
    >
      <Card className="p-4 bg-card/80 backdrop-blur-xl border-border/50">
        {/* Upload button */}
        <div className="flex items-center gap-3">
          <Button
            onClick={() => fileInputRef.current?.click()}
            variant="outline"
            className="border-cosmic-cyan/30 hover:border-cosmic-cyan"
          >
            <Upload className="w-4 h-4 mr-2" />
            Upload Document
          </Button>
          
          <p className="text-xs text-muted-foreground">
            PDF, TXT, DOCX, MD (max 10MB)
          </p>
        </div>
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.txt,.docx,.md"
          onChange={handleFileSelect}
          className="hidden"
        />
        
        {/* File list */}
        <AnimatePresence>
          {files.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 space-y-2"
            >
              {files.map(file => (
                <motion.div
                  key={file.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="flex items-center justify-between p-3 bg-muted/30 rounded-lg"
                >
                  <div className="flex items-center gap-3 flex-1">
                    <File className="w-4 h-4 text-cosmic-cyan" />
                    <span className="text-sm">{file.name}</span>
                    
                    {file.status === 'uploading' && (
                      <Loader2 className="w-4 h-4 animate-spin text-cosmic-purple" />
                    )}
                    {file.status === 'uploaded' && (
                      <Button
                        size="sm"
                        onClick={() => handleAnalyze(file.id, file.name)}
                        className="bg-gradient-to-r from-cosmic-cyan to-cosmic-purple"
                      >
                        Analyze
                      </Button>
                    )}
                    {file.status === 'analyzing' && (
                      <div className="flex items-center gap-2">
                        <Loader2 className="w-4 h-4 animate-spin text-cosmic-cyan" />
                        <span className="text-xs text-muted-foreground">Analyzing...</span>
                      </div>
                    )}
                    {file.status === 'completed' && (
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span className="text-xs text-green-500">Live & Ready</span>
                      </div>
                    )}
                  </div>
                  
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => handleRemove(file.id)}
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </motion.div>
                
                {/* Automatic Inline Preview renders here immediately when completed */}
                {file.status === 'completed' && (
                  <DocumentInlinePreview filename={file.name} fileId={file.id} />
                )}
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  </motion.div>
);
```

### 4. Inline Document Preview Component

Create new file: `src/components/DocumentInlinePreview.tsx`

```typescript
import { motion } from 'framer-motion';
import { FileText, ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface DocumentInlinePreviewProps {
  filename: string;
  fileId: string;
}

const DocumentInlinePreview = ({ filename, fileId }: DocumentInlinePreviewProps) => {
  const isPdf = filename.toLowerCase().endsWith('.pdf');
  const previewUrl = `http://localhost:8000/api/documents/${fileId}/view`;

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      className="mt-3 overflow-hidden rounded-xl border border-cosmic-cyan/20 bg-black/40 backdrop-blur-md shadow-[0_0_15px_rgba(6,182,212,0.1)]"
    >
      <div className="flex items-center justify-between p-2 px-3 bg-cosmic-cyan/10 border-b border-cosmic-cyan/10 backdrop-blur-xl">
        <div className="flex items-center gap-2">
          <FileText size={14} className="text-cosmic-cyan" />
          <span className="text-[10px] font-bold uppercase tracking-widest text-cosmic-cyan/80">
            Document Content Insight
          </span>
        </div>
        <a href={previewUrl} target="_blank" rel="noreferrer">
          <Button size="icon" variant="ghost" className="h-6 w-6 text-cosmic-cyan/60 hover:text-cosmic-cyan">
            <ExternalLink size={12} />
          </Button>
        </a>
      </div>
      
      <div className="w-full h-48 bg-white/5 backdrop-blur-sm">
        {isPdf ? (
          <iframe 
            src={`${previewUrl}#toolbar=0&navpanes=0`} 
            className="w-full h-full border-none opacity-90"
            title={filename}
          />
        ) : (
          <div className="p-4 h-full overflow-y-auto font-mono text-[11px] leading-relaxed text-cosmic-cyan/70">
            <pre className="whitespace-pre-wrap">
              {/* This will be populated by a separate fetch if needed */}
              Loading content stream...
            </pre>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default DocumentInlinePreview;
```

### 5. History Indicator Component

Create new file: `src/components/HistoryIndicator.tsx`

```typescript
import { motion } from 'framer-motion';
import { History, Zap, BrainCircuit } from 'lucide-react';

interface HistoryIndicatorProps {
  hasSummary: boolean;
  nearContextCount: number;
}

const HistoryIndicator = ({ hasSummary, nearContextCount }: HistoryIndicatorProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex gap-4 p-2 px-4 rounded-full bg-muted/20 border border-border/30 backdrop-blur-sm self-center text-[10px] uppercase tracking-widest font-bold"
    >
      <div className="flex items-center gap-1.5 text-cosmic-purple">
        <BrainCircuit size={12} className={hasSummary ? "animate-pulse" : "opacity-30"} />
        <span>Memory Summary: {hasSummary ? "Active" : "None"}</span>
      </div>
      
      <div className="w-[1px] h-3 bg-border/50 self-center" />
      
      <div className="flex items-center gap-1.5 text-cosmic-cyan">
        <Zap size={12} className="animate-cosmic-pulse" />
        <span>Live Context: {nearContextCount} Messages</span>
      </div>
    </motion.div>
  );
};

export default HistoryIndicator;
```

### 5. Update ChatContainer

Modify `src/components/ChatContainer.tsx`:

**Changes needed:**
1. Import `DocumentUpload` component
2. Add state for uploaded document IDs
3. Replace simulated API calls with real backend streaming
4. Pass document IDs to chat requests

```typescript
// Add imports
import DocumentUpload from './DocumentUpload';
import HistoryIndicator from './HistoryIndicator';
import { apiClient } from '@/services/api';

// Add state
const [uploadedDocs, setUploadedDocs] = useState<Array<{ id: string; name: string }>>([]);
const [historySummary, setHistorySummary] = useState<string>('');

// ...

// Insert HistoryIndicator between Header and Messages
<motion.div 
  className="flex justify-center p-2 border-b border-border/10"
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
>
  <HistoryIndicator 
    hasSummary={!!historySummary} 
    nearContextCount={messages.length > 10 ? 10 : messages.length} 
  />
</motion.div>

<div ref={chatContainerRef} className="flex-1 overflow-y-auto ...">
  {/* messages... */}
</div>

// Add DocumentUpload component in render
// Insert before the messages area
<DocumentUpload 
  onUploadComplete={(fileId, filename) => {
    setUploadedDocs(prev => [...prev, { id: fileId, name: filename }]);
  }} 
/>
```

### 5. Display Uploaded Documents

Add visual indicator showing which documents are loaded:

```typescript
{/* Document indicator */}
{uploadedDocs.length > 0 && (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    className="mb-4 flex items-center gap-2 text-xs text-muted-foreground"
  >
    <Sparkles className="w-4 h-4 text-cosmic-cyan" />
    <span>
      {uploadedDocs.length} document{uploadedDocs.length > 1 ? 's' : ''} loaded
    </span>
  </motion.div>
)}
```

---

## 💎 Premium Aesthetic Guidelines

To ensure the "Cool/Best Chatbot" look, the following styling rules must be followed:

1. **Glassmorphism**: Use `backdrop-blur-xl` and `bg-card/40` extensively for containers to create a "futuristic space-glass" feel.
2. **Glow Effects**: Apply `shadow-[0_0_20px_rgba(6,182,212,0.3)]` (cyan) and `shadow-[0_0_20px_rgba(168,85,247,0.3)]` (purple) to active elements.
3. **Animated Borders**: Use the `animate-cosmic-pulse` or custom keyframes to make borders "breathe" with light.
4. **Vibrant Gradients**: All primary actions must use the `from-cosmic-cyan via-cosmic-purple to-cosmic-pink` linear gradient.

---

## 🧪 Testing Checklist

### Upload Flow
- [ ] Choose file button opens file picker
- [ ] Only allowed file types can be selected
- [ ] Files over 10MB show error
- [ ] Upload shows spinner
- [ ] Upload success shows "Analyze" button
- [ ] Analyze button triggers backend processing
- [ ] Analysis status polls every 2 seconds
- [ ] Completion shows green checkmark

### Chat Flow
- [ ] Chat without documents works (no RAG)
- [ ] Chat with documents uses RAG
- [ ] Streaming response updates incrementally
- [ ] Cosmic loader shows during thinking
- [ ] Error messages display in toast

### Edge Cases
- [ ] Multiple files can be uploaded
- [ ] Files can be removed before analysis
- [ ] Network errors are handled gracefully
- [ ] Backend down shows appropriate error

---

## 🚀 Bootstrapping with `frontend.bat`
For quick startup, a `frontend.bat` file should be located at the project root (`c:\Users\aryan\OneDrive\Desktop\Simple_ChatBot\frontend.bat`).

**Content of `frontend.bat`**:
```batch
@echo off
echo [COSMIC FRONTEND] Starting initialization...

cd Frontend/cosmic-chat-ai-main/cosmic-chat-ai-main

if not exist node_modules (
    echo [COSMIC FRONTEND] Installing dependencies...
    npm install
)

echo [COSMIC FRONTEND] Launching Vite development server...
npm run dev
```

---

## 📦 Dependencies

All required dependencies are already in `package.json`:
- ✅ React Query (@tanstack/react-query)
- ✅ shadcn/ui components
- ✅ Framer Motion
- ✅ Lucide React icons
- ✅ React Hook Form
- ✅ Sonner (toast notifications)

---

## 🚀 Implementation Order

1. Create `.env` file with API base URL
2. Create `src/services/api.ts` with API client
3. Create `src/components/DocumentUpload.tsx`
4. Modify `src/components/ChatContainer.tsx` to use backend
5. Test upload flow
6. Test chat flow with RAG
7. Test error states
8. Polish UI/UX

---

## 📝 Environment Variables

**Frontend `.env`**:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_MAX_FILE_SIZE=10485760
VITE_ALLOWED_FILE_TYPES=.pdf,.txt,.docx,.md
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_BASE_URL;
```

---

## ✅ Acceptance Criteria

1. User can upload PDF/DOCX/TXT/MD files
2. "Analyze" button appears after upload
3. Analysis progress is shown
4. Completed documents show checkmark
5. Chat uses uploaded documents for RAG
6. Streaming responses work smoothly
7. All error states show appropriate feedback
8. Cosmic theme is maintained throughout

---

## 📌 Next Steps

1. Implement backend endpoints → Already planned
2. Test end-to-end flow → `05_Testing_Verification.md`
3. Deploy and monitor → Production deployment plan
