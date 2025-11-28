from langchain_core.prompts import ChatPromptTemplate
from src.utils.state import AgentState
from src.utils.config import get_llm
from src.schemas.schema import FluencyFeedback
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def analyze_fluency(state: AgentState) -> AgentState:
    """
    Analyzes fluency and coherence based on transcript and duration.
    """
    agent_name = "Fluency Analyzer"
    
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
        structured_llm = llm.with_structured_output(FluencyFeedback)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert IELTS Speaking examiner specializing in Fluency and Coherence."),
            ("user", """
            Analyze the following transcript for Fluency and Coherence.
            
            Transcript: {transcript}
            Duration: {duration:.2f} seconds
            Speaking Rate: {wpm:.2f} Words Per Minute (WPM)
            
            Provide a structured assessment including:
            1. score (0-9): Fluency and coherence score based on IELTS criteria
            2. evaluation: List of evaluation details with criteria (e.g., 'Strengths', 'Weaknesses', 'Improvements') and detailed descriptions
            3. errors: List of fluency issues found (hesitations, repetitions, self-corrections) with:
               - original: The problematic text
               - suggested: How it could be improved
               - explanation: Why this is an issue
            4. feedback: Overall feedback on fluency and coherence
            5. wpm: {wpm:.2f} (use this exact value)
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
