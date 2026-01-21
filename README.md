# Automated Researcher

An AI-powered research agent that automatically searches, scrapes, summarizes, and saves research briefings to Google Drive.

## Features
- 🔍 Google search via Serper API
- 🌐 Intelligent web scraping
- 🤖 AI-powered summarization with Claude
- 📁 Automatic Google Drive upload
- 🔄 LangGraph workflow orchestration

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Keys
- **Serper API**: https://serper.dev (100 free searches)
- **Anthropic API**: https://console.anthropic.com

### 3. Google Drive Setup
1. Go to Google Cloud Console
2. Create a new project
3. Enable Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json`

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run
```bash
python -m src.main "Latest trends in EV batteries"
```

## Usage
```python
from src.main import run_research

result = run_research("Your research topic")
print(result["document_url"])
```

## Project Structure
- `src/agents/` - LangGraph workflow and state
- `src/services/` - Search, scraping, summarization, Drive
- `config/` - Settings and configuration
- `tests/` - Unit tests
