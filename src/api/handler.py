import os
import shutil
import uuid
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.workflows.wf_speaking_feedback import create_graph
from src.schemas.schema import IELTSFeedback
from src.utils.logger import setup_logger, log_step
import uvicorn

logger = setup_logger(__name__)

app = FastAPI(title="IELTS Speaking Feedback API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development; restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process/speaking", response_model=IELTSFeedback)
async def process_speaking(file: UploadFile = File(...)):
    """
    Process an audio file and return IELTS speaking feedback.
    """
    request_id = str(uuid.uuid4())[:8]
    
    logger.info("=" * 80)
    logger.info(f"[REQUEST {request_id}] Processing audio: {file.filename}")
    logger.info(f"[REQUEST {request_id}] Content-Type: {file.content_type}")
    logger.info("=" * 80)
    
    # Validate file type
    if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
        logger.error(f"[REQUEST {request_id}] Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an audio file.")
    
    # Save uploaded file temporarily
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join("/tmp", temp_filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize graph
        graph = create_graph()
        
        # Run workflow
        log_step(logger, f"[REQUEST {request_id}] Workflow Execution", "STARTED")
        
        initial_state = {
            "audio_path": temp_path
        }
        
        result = graph.invoke(initial_state)
        
        log_step(logger, f"[REQUEST {request_id}] Workflow Execution", "COMPLETED")
        
        final_feedback = result.get("final_feedback")
        
        if not final_feedback:
            logger.error(f"[REQUEST {request_id}] No feedback generated")
            raise HTTPException(status_code=500, detail="Failed to generate feedback.")
        
        logger.info(f"[REQUEST {request_id}] ✓ Request completed successfully")
        logger.info("=" * 80)
        
        return final_feedback
        
    except HTTPException:
        raise
    except Exception as e:
        log_step(logger, f"[REQUEST {request_id}] Workflow Execution", "FAILED")
        logger.error(f"[REQUEST {request_id}] Error: {str(e)}")
        logger.info("=" * 80)
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "IELTS Speaking Feedback API"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting IELTS Speaking Feedback API server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

