# Automated Research Agent 🤖🔎

A powerful AI-driven application that autonomously conducts deep web research on any given topic. It searches the web, scrapes relevant content, synthesizes findings using advanced LLMs (OpenAI GPT-4), and generates a professional briefing document uploaded directly to Google Drive.

![Project Banner](https://img.shields.io/badge/Status-Active-success)
![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/Built%20With-LangGraph-orange)

## 🌟 Key Features

- **Automated Workflow**: Uses a state graph to orchestrate searching, scraping, and analyzing.
- **Smart Search**: Leverages Google Search API (Serper) to find high-quality sources.
- **Intelligent Scraping**: Extracts clean text from web pages, removing ads and clutter.
- **AI Summarization**: Uses OpenAI GPT-4 to generate executive summaries and insights.
- **Google Drive Integration**: Automatically formats and uploads the final report as a Word document.
- **Interactive Web UI**: vivid, dark-themed frontend for easy interaction.

## 🚀 How It Works

1.  **Input**: User enters a topic (e.g., "Future of Quantum Computing").
2.  **Search**: The agent queries Google for top articles.
3.  **Scrape**: It visits the links and extracts the core content.
4.  **Synthesize**: The AI analyzes the data and writes a structured briefing.
5.  **Deliver**: The document is uploaded to Google Drive, and a link is provided.

## 🛠️ Technology Stack

-   **Backend**: Python, FastAPI, LangGraph, LangChain
-   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
-   **AI/LLM**: OpenAI GPT-4o / GPT-3.5
-   **Services**: Google Drive API, Serper.dev
-   **Deployment**: Docker, Render

## 📋 Installation & Local Setup

### Prerequisites
- Python 3.10+
- OpenAI API Key
- Serper API Key
- Google Cloud Credentials (`credentials.json`)

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/rkotesh/Automation-Researcher.git
    cd automated-researcher
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file:
    ```env
    OPENAI_API_KEY=your_key_here
    SERPER_API_KEY=your_key_here
    GOOGLE_DRIVE_CREDENTIALS_PATH=credentials.json
    GOOGLE_DRIVE_TOKEN_PATH=token.json
    ```

4.  **Run the Server**
    ```bash
    uvicorn src.server:app --reload
    ```
    Access the app at `http://localhost:8000`

## 🌐 API Usage

**Endpoint:** `POST /research`

```json
{
  "topic": "Impact of Generative AI on Education"
}
```

## 📄 License
MIT License
