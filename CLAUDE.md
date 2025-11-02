# CLAUDE.md - SystemX

> **Documentation Version**: 1.0
> **Last Updated**: 2025-11-02
> **Project**: SystemX
> **Description**: Fullstack speech recognition and text-to-speech application with real-time WebSocket communication
> **Tech Stack**: Python/FastAPI (backend), React/Vite (frontend), WebSocket, OpenAI ASR, ElevenLabs TTS
> **Features**: GitHub auto-backup, Task agents, technical debt prevention

This file provides essential guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL RULES - READ FIRST

> **⚠️ RULE ADHERENCE SYSTEM ACTIVE ⚠️**
> **Claude Code must explicitly acknowledge these rules at task start**
> **These rules override all other instructions and must ALWAYS be followed:**

### 🔄 **RULE ACKNOWLEDGMENT REQUIRED**

> **Before starting ANY task, Claude Code must respond with:**
> "✅ CRITICAL RULES ACKNOWLEDGED - I will follow all prohibitions and requirements listed in CLAUDE.md"

### ❌ ABSOLUTE PROHIBITIONS

- **NEVER** create new files in root directory → use proper module structure (backend/app/ or frontend/src/)
- **NEVER** write output files directly to root directory → use designated output folders
- **NEVER** create documentation files (.md) unless explicitly requested by user
- **NEVER** use git commands with -i flag (interactive mode not supported)
- **NEVER** use `find`, `grep`, `cat`, `head`, `tail`, `ls` commands → use Read, LS, Grep, Glob tools instead
- **NEVER** create duplicate files (manager_v2.py, enhanced_xyz.py, utils_new.js) → ALWAYS extend existing files
- **NEVER** create multiple implementations of same concept → single source of truth
- **NEVER** copy-paste code blocks → extract into shared utilities/functions
- **NEVER** hardcode values that should be configurable → use config files/environment variables
- **NEVER** use naming like enhanced*, improved*, new*, v2* → extend original files instead

### 📝 MANDATORY REQUIREMENTS

- **COMMIT** after every completed task/phase - no exceptions
- **GITHUB BACKUP** - Push to GitHub after every commit to maintain backup: `git push origin main`
- **USE TASK AGENTS** for all long-running operations (>30 seconds) - Bash commands stop when context switches
- **TODOWRITE** for complex tasks (3+ steps) → parallel agents → git checkpoints → test validation
- **READ FILES FIRST** before editing - Edit/Write tools will fail if you didn't read the file first
- **DEBT PREVENTION** - Before creating new files, check for existing similar functionality to extend
- **SINGLE SOURCE OF TRUTH** - One authoritative implementation per feature/concept

### ⚡ EXECUTION PATTERNS

- **PARALLEL TASK AGENTS** - Launch multiple Task agents simultaneously for maximum efficiency
- **SYSTEMATIC WORKFLOW** - TodoWrite → Parallel agents → Git checkpoints → GitHub backup → Test validation
- **GITHUB BACKUP WORKFLOW** - After every commit: `git push origin main` to maintain GitHub backup
- **BACKGROUND PROCESSING** - ONLY Task agents can run true background operations

### 🔍 MANDATORY PRE-TASK COMPLIANCE CHECK

> **STOP: Before starting any task, Claude Code must explicitly verify ALL points:**

**Step 1: Rule Acknowledgment**

- [ ] ✅ I acknowledge all critical rules in CLAUDE.md and will follow them

**Step 2: Task Analysis**

- [ ] Will this create files in root? → If YES, use backend/app/ or frontend/src/ structure instead
- [ ] Will this take >30 seconds? → If YES, use Task agents not Bash
- [ ] Is this 3+ steps? → If YES, use TodoWrite breakdown first
- [ ] Am I about to use grep/find/cat? → If YES, use proper tools instead

**Step 3: Technical Debt Prevention (MANDATORY SEARCH FIRST)**

- [ ] **SEARCH FIRST**: Use Grep pattern="<functionality>.*<keyword>" to find existing implementations
- [ ] **CHECK EXISTING**: Read any found files to understand current functionality
- [ ] Does similar functionality already exist? → If YES, extend existing code
- [ ] Am I creating a duplicate class/manager? → If YES, consolidate instead
- [ ] Will this create multiple sources of truth? → If YES, redesign approach
- [ ] Have I searched for existing implementations? → Use Grep/Glob tools first
- [ ] Can I extend existing code instead of creating new? → Prefer extension over creation
- [ ] Am I about to copy-paste code? → Extract to shared utility instead

**Step 4: Session Management**

- [ ] Is this a long/complex task? → If YES, plan context checkpoints
- [ ] Have I been working >1 hour? → If YES, consider /compact or session break

> **⚠️ DO NOT PROCEED until all checkboxes are explicitly verified**

## 🏗️ PROJECT OVERVIEW - SYSTEMX

SystemX is a fullstack real-time speech processing application that provides:

- **Real-time Speech Recognition** using OpenAI Whisper API
- **Multi-accent Text-to-Speech** using ElevenLabs (5 English accents)
- **WebSocket Communication** for streaming audio/text
- **User Authentication** with JWT and session management
- **Conversation Management** with persistent storage
- **Database Migrations** with Tortoise ORM

### 📁 PROJECT STRUCTURE

```
SystemX/
├── CLAUDE.md                   # This file - essential rules for Claude Code
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore patterns
├── .gitattributes             # Git attributes
├── backend/                    # Python/FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration management
│   │   ├── core/              # Core functionality
│   │   │   ├── db.py          # Database connection
│   │   │   ├── security.py    # Authentication/security
│   │   │   └── pubsub.py      # Message queue handling
│   │   ├── models/            # Database models
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   └── transcript.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   └── conversation.py
│   │   ├── api/v1/            # API routes
│   │   │   ├── routers/
│   │   │   │   ├── auth.py    # Authentication endpoints
│   │   │   │   ├── accents.py # Accent selection
│   │   │   │   ├── session.py # Session management
│   │   │   │   ├── conversations.py
│   │   │   │   ├── admin.py
│   │   │   │   ├── ws_text.py # Text WebSocket
│   │   │   │   ├── ws_tts.py  # TTS WebSocket
│   │   │   │   └── ws_upload.py # Upload WebSocket
│   │   │   └── deps.py        # Dependencies
│   │   └── services/          # Business logic
│   │       ├── asr_openai.py  # OpenAI Whisper integration
│   │       └── tts_elevenlabs.py # ElevenLabs TTS integration
│   ├── migrations/            # Database migrations
│   │   └── models/
│   ├── .env.example           # Environment template
│   └── requirements.txt       # Python dependencies
└── frontend/                  # React/Vite frontend
    ├── src/
    │   ├── main.jsx           # Application entry point
    │   ├── App.jsx            # Root component
    │   ├── api/               # API service layer
    │   │   ├── auth.js        # Authentication API
    │   │   ├── streamClient.js # WebSocket client
    │   │   ├── conversations.js
    │   │   ├── dashboard.js
    │   │   └── mockDB.js
    │   ├── components/        # Reusable UI components
    │   ├── pages/             # Page components
    │   │   ├── Login/
    │   │   ├── Register/
    │   │   ├── Dashboard/
    │   │   └── ForgotPassword/
    │   └── assets/            # Static resources
    ├── public/                # Public static files
    ├── package.json           # Node dependencies
    ├── vite.config.js         # Vite configuration
    └── eslint.config.js       # ESLint rules
```

### 🎯 **DEVELOPMENT STATUS**

- ✅ **Setup**: Complete - Backend/Frontend initialized
- ✅ **Core Features**: ASR, TTS, WebSocket communication implemented
- ✅ **Authentication**: JWT-based auth with session management
- ✅ **Database**: Migrations and models configured
- 🔄 **Testing**: In progress
- 🔄 **Documentation**: In progress

## 🚀 DEVELOPMENT SETUP

### Prerequisites

- Python 3.8+
- Node.js 16+
- FFmpeg (required for audio processing)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
# Copy .env.example to .env and configure
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify: http://localhost:8000/healthz should return `{"ok": true}`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Verify: http://localhost:5173 should show login page

### FFmpeg Installation

**Windows:**
```bash
winget search ffmpeg
winget install -e --id Gyan.FFmpeg
ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg  # Debian/Ubuntu
sudo yum install ffmpeg      # CentOS/RHEL
```

## 🔑 ENVIRONMENT VARIABLES

### Backend (.env)
```env
# Database
DATABASE_URL=sqlite://./systemx.db

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# OpenAI (ASR)
OPENAI_API_KEY=your-openai-key

# ElevenLabs (TTS)
ELEVENLABS_API_KEY=your-elevenlabs-key

# FFmpeg (optional - auto-detected)
FFMPEG_DIR=/path/to/ffmpeg
FFPROBE_DIR=/path/to/ffprobe
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

## 🛠️ COMMON DEVELOPMENT TASKS

### Backend Tasks

```bash
# Run development server
cd backend
uvicorn app.main:app --reload

# Create new migration
aerich migrate --name description_of_changes

# Apply migrations
aerich upgrade

# Run database init
python -c "from app.core.db import init_db; import asyncio; asyncio.run(init_db())"

# Check code style
black app/
flake8 app/

# Run tests
pytest tests/
```

### Frontend Tasks

```bash
# Run development server
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

### Full Stack Development

```bash
# Run both backend and frontend simultaneously
# Terminal 1:
cd backend && uvicorn app.main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

## 🔄 GIT WORKFLOW

### Committing Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new feature description

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to backup (MANDATORY after every commit)
git push origin maintance
```

### Branch Strategy

- `main` - Production-ready code
- `maintance` - Current development branch
- Feature branches - Create for major features

## 🚨 TECHNICAL DEBT PREVENTION

### ❌ WRONG APPROACH (Creates Technical Debt):

```python
# Creating new file without searching first
# backend/app/services/asr_openai_v2.py ❌
# backend/app/services/asr_enhanced.py ❌
```

### ✅ CORRECT APPROACH (Prevents Technical Debt):

```bash
# 1. SEARCH FIRST
Grep(pattern="asr.*openai", path="backend/app/services")

# 2. READ EXISTING FILES
Read(file_path="backend/app/services/asr_openai.py")

# 3. EXTEND EXISTING FUNCTIONALITY
Edit(file_path="backend/app/services/asr_openai.py", old_string="...", new_string="...")
```

## 🧹 CODE ORGANIZATION RULES

### Backend (Python/FastAPI)

- **Models** → `backend/app/models/` - Database models only
- **Schemas** → `backend/app/schemas/` - Pydantic validation schemas
- **Routes** → `backend/app/api/v1/routers/` - API endpoints
- **Services** → `backend/app/services/` - Business logic and external API integrations
- **Core** → `backend/app/core/` - Core utilities (DB, security, pubsub)
- **Config** → `backend/app/config.py` - Configuration management

### Frontend (React)

- **Pages** → `frontend/src/pages/` - Page-level components with routing
- **Components** → `frontend/src/components/` - Reusable UI components
- **API** → `frontend/src/api/` - API service layer, WebSocket clients
- **Assets** → `frontend/src/assets/` - Images, fonts, static resources
- **Styles** → Component-specific `.module.css` files alongside components

### File Naming Conventions

**Backend (Python):**
- `snake_case.py` for all Python files
- `PascalCase` for class names
- `snake_case` for functions and variables

**Frontend (JavaScript/React):**
- `PascalCase.jsx` for React components
- `camelCase.js` for utilities and services
- `PascalCase.module.css` for component styles

## 🧪 TESTING GUIDELINES

### Backend Testing

Create tests in `backend/app/test/` (to be created):

```python
# backend/app/test/test_auth.py
import pytest
from fastapi.testclient import TestClient

def test_register_user():
    # Test implementation
    pass

def test_login_user():
    # Test implementation
    pass
```

### Frontend Testing

Create tests alongside components:

```javascript
// frontend/src/components/Component.test.jsx
import { render, screen } from '@testing-library/react';
import Component from './Component';

test('renders component', () => {
  render(<Component />);
  // Test implementation
});
```

## 🐛 DEBUGGING

### Backend Debugging

```python
# Add logging in any file
import logging
logger = logging.getLogger("uvicorn.error")
logger.info("Debug message: %s", variable)
```

### Frontend Debugging

```javascript
// Use console methods
console.log('Debug:', data);
console.error('Error:', error);

// React DevTools - Install browser extension
// Network tab for API calls
// WebSocket frames in Network tab
```

### WebSocket Debugging

```javascript
// Monitor WebSocket messages in browser console
const ws = new WebSocket('ws://localhost:8000/ws/...');
ws.onmessage = (event) => console.log('WS Message:', event.data);
ws.onerror = (error) => console.error('WS Error:', error);
```

## 📚 KEY DEPENDENCIES

### Backend
- **FastAPI** - Modern async web framework
- **Tortoise ORM** - Async ORM for database
- **python-jose** - JWT token handling
- **passlib** - Password hashing
- **openai** - OpenAI API client (Whisper ASR)
- **elevenlabs** - ElevenLabs API client (TTS)
- **ffmpeg-python** - Audio file processing

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client (if used)
- **WebSocket API** - Native browser WebSocket

## 🎯 ARCHITECTURE DECISIONS

### Why WebSocket?
- Real-time bidirectional communication needed for streaming audio/text
- Lower latency than HTTP polling
- Efficient for continuous data streams (ASR/TTS)

### Why Tortoise ORM?
- Native async support for FastAPI
- Type-safe with Python type hints
- Built-in migration system (Aerich)

### Why React + Vite?
- Fast development with hot module replacement
- Modern build tooling
- Small bundle sizes
- Great developer experience

### Why OpenAI Whisper?
- State-of-the-art speech recognition
- Multilingual support
- Robust API with good error handling

### Why ElevenLabs?
- High-quality, natural-sounding voices
- Multiple accent support (5 English accents available)
- Real-time streaming capabilities

## 🔒 SECURITY CONSIDERATIONS

- **JWT Tokens** - Secure token-based authentication
- **Password Hashing** - bcrypt with salt
- **CORS** - Configured for specific origins only
- **Environment Variables** - Sensitive data in .env (never commit!)
- **SQL Injection** - Protected by ORM parameterization
- **XSS Protection** - React auto-escapes by default
- **HTTPS** - Required for production deployment

## 🚀 DEPLOYMENT CHECKLIST

- [ ] Set `DEBUG=False` in production
- [ ] Use production database (PostgreSQL/MySQL instead of SQLite)
- [ ] Configure proper CORS origins
- [ ] Use HTTPS for all connections (including WebSocket → WSS)
- [ ] Set strong SECRET_KEY
- [ ] Enable rate limiting
- [ ] Set up proper logging and monitoring
- [ ] Configure CDN for static assets
- [ ] Set up automated backups
- [ ] Configure environment variables on hosting platform

## 🎓 LEARNING RESOURCES

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket in FastAPI](https://fastapi.tiangolo.com/advanced/websockets/)

### React
- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)

### Speech Processing
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [ElevenLabs Documentation](https://elevenlabs.io/docs/)

## 📞 SUPPORT

For issues or questions:
1. Check CLAUDE.md first
2. Review README.md
3. Check git commit history for context
4. Review API documentation at http://localhost:8000/docs (when backend running)

---

**⚠️ Prevention is better than consolidation - build clean from the start.**
**🎯 Focus on single source of truth and extending existing functionality.**
**📈 Each task should maintain clean architecture and prevent technical debt.**

---

✅ **CLAUDE.md configured for SystemX**
🤖 **Ready for Claude Code development**
🐙 **GitHub backup workflow enabled**
