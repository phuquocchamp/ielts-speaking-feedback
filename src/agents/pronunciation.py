from langchain_core.prompts import ChatPromptTemplate
from src.utils.state import AgentState
from src.utils.config import get_llm
from src.schemas.schema import PronunciationFeedback
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def analyze_pronunciation(state: AgentState) -> AgentState:
    """
    Analyzes pronunciation and fluency based on transcript and duration.
    """
    agent_name = "Pronunciation Analyzer"
    
    try:
        log_step(logger, agent_name, "STARTED")
        
        transcript = state.get("transcript", "")
        duration = state.get("duration", 0)
        
        if not transcript:
            log_step(logger, agent_name, "SKIPPED")
            return {"pronunciation_analysis": None}
        
        # Calculate Words Per Minute (WPM)
        word_count = len(transcript.split())
        wpm = (word_count / duration) * 60 if duration > 0 else 0
        
        llm = get_llm()
        structured_llm = llm.with_structured_output(PronunciationFeedback)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert IELTS Speaking examiner specializing in Pronunciation and Fluency."),
            ("user", """
            Analyze the following transcript for Fluency and Coherence.
            
            Transcript: {transcript}
            Duration: {duration:.2f} seconds
            Speaking Rate: {wpm:.2f} Words Per Minute (WPM)
            
            Provide a structured assessment including:
            1. WPM (passed in)
            2. Fluency Score (0-9)
            3. Pronunciation Score (0-9) - inferred from text flow/clarity
            4. Detailed Feedback
            """)
        ])
        
        chain = prompt | structured_llm
        response = chain.invoke({"transcript": transcript, "duration": duration, "wpm": wpm})
        
        result = {"pronunciation_analysis": response.model_dump()}
        
        log_step(logger, agent_name, "COMPLETED")
        return result
        
    except Exception as e:
        log_step(logger, agent_name, "FAILED")
        logger.error(f"{agent_name} error: {str(e)}")
        raise
