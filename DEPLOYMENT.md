# Deployment Guide to Render

This guide explains how to deploy the "Automated Researcher" as a web API to [Render](https://render.com).

## Prerequisites
1.  A GitHub repository containing this project code.
2.  A Render account.
3.  Your API Keys (`OPENAI_API_KEY`, `SERPER_API_KEY`, etc.).
4.  Your Google Drive credentials files (`credentials.json` and `token.json`).

## Deployment Steps

### Method 1: Connect GitHub (Recommended)

1.  **Push to GitHub**: Ensure your latest code (including `Dockerfile` and `src/server.py`) is pushed to your GitHub repository.
2.  **New Web Service**:
    - Go to your Render Dashboard.
    - Click **New +** -> **Web Service**.
    - Connect your GitHub repository.
3.  **Configure**:
    - **Runtime**: Select **Docker**.
    - **Name**: Give it a name (e.g., `automated-researcher`).
    - **Region**: Choose a region close to you.
    - **Instance Type**: Free (or higher).
4.  **Environment Variables**:
    Add the following Environment Variables in the "Environment" tab:
    - `SERPER_API_KEY`: Your Serper API key.
    - `OPENAI_API_KEY`: Your OpenAI API key.
    - `LLM_PROVIDER`: `openai`
    - `LLM_MODEL`: `gpt-4-turbo-preview` (or your preferred model)
    - `GOOGLE_DRIVE_CREDENTIALS_PATH`: `/app/secrets/credentials.json`
    - `GOOGLE_DRIVE_TOKEN_PATH`: `/app/secrets/token.json`
    - `GOOGLE_DRIVE_FOLDER_ID`: (Optional) Your Drive Folder ID.

### Handling Google Credentials (Secret Files)

Since you cannot commit `credentials.json` and `token.json` to GitHub for security reasons, you must upload them to Render.

1.  In your Render Service Dashboard, go to **"Secret Files"** (left sidebar).
2.  Click **"Add Secret File"**.
3.  **File 1**:
    - **Filename**: `secrets/credentials.json` (Make sure the path matches your ENV var, Render mounts secret files at `/etc/secrets/` usually, but we can map them).
    - **Review**: Render typically mounts secret files at `/etc/secrets/<filename>`.
    - **Correction**: Set your Environment Variables to:
        - `GOOGLE_DRIVE_CREDENTIALS_PATH`: `/etc/secrets/credentials.json`
        - `GOOGLE_DRIVE_TOKEN_PATH`: `/etc/secrets/token.json`
    - **Content**: Paste the content of your local `credentials.json`.
4.  **File 2**:
    - **Filename**: `token.json` (Note: if you adding multiple, check Render docs; usually they are individual).
    - **Content**: Paste the content of your local `token.json`.

### Method 2: Blueprint (Infrastructure as Code)

1.  In Render, go to "Blueprints".
2.  Connect your repo.
3.  It will read `render.yaml`.
4.  Complete the setup wizard.

## Usage after Deployment

Once deployed, Render will provide a URL (e.g., `https://automated-researcher.onrender.com`).

**To run a research task:**

Use a tool like Postman, curl, or your browser's console.

**Request:**
```bash
curl -X POST https://your-app-url.onrender.com/research \
     -H "Content-Type: application/json" \
     -d '{"topic": "Future of AI in Healthcare"}'
```

**Response:**
```json
{
    "status": "success",
    "topic": "Future of AI in Healthcare",
    "document_url": "https://docs.google.com/...",
    "briefing_preview": "..."
}
```
