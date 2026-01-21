from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.main import run_research
from src.utils.logger import get_logger
import os

# Initialize Logger
logger = get_logger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Automated Researcher API",
    description="API to trigger automated research tasks",
    version="1.0.0"
)

# Mount static directory
app.mount("/static", StaticFiles(directory="src/static"), name="static")

class ResearchRequest(BaseModel):
    topic: str

@app.get("/")
def read_root():
    return FileResponse('src/static/index.html')

@app.post("/research")
def trigger_research(request: ResearchRequest):
    """
    Trigger a research task synchronously (keeps connection open).
    For long running tasks, proper background queues like Celery/BullMQ are recommended,
    but for this demo we will run it and return the result.
    """
    try:
        logger.info(f"Received research request for: {request.topic}")
        result = run_research(request.topic)
        
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
            
        return {
            "status": "success",
            "topic": request.topic,
            "document_url": result.get("document_url"),
            "sources_count": len(result.get("scraped_contents", [])),
            "briefing_preview": result.get("briefing_document", "")[:500] + "..."
        }
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
