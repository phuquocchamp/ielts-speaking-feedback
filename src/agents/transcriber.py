import os
from openai import OpenAI
from src.utils.state import AgentState
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def transcribe_audio(state: AgentState) -> AgentState:
    """
    Transcribes audio using OpenAI's Whisper model.
    """
    agent_name = "Transcriber"
    
    try:
        log_step(logger, agent_name, "STARTED")
        
        audio_path = state["audio_path"]
        
        if not os.path.exists(audio_path):
            log_step(logger, agent_name, "FAILED")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        client = OpenAI()
        
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="verbose_json"
            )
        
        # Extract text and duration
        text = transcript.text
        duration = transcript.duration
        
        result = {
            "transcript": text,
            "duration": duration
        }
        
        log_step(logger, agent_name, "COMPLETED")
        return result
        
    except Exception as e:
        log_step(logger, agent_name, "FAILED")
        logger.error(f"{agent_name} error: {str(e)}")
        raise
