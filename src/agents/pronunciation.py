from langchain_core.prompts import ChatPromptTemplate
from src.utils.state import AgentState
from src.utils.config import get_llm
from src.schemas.schema import PronunciationFeedback
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def analyze_pronunciation(state: AgentState) -> AgentState:
    """
    Analyzes pronunciation quality based on the transcript.
    """
    agent_name = "Pronunciation Analyzer"
    
    try:
        log_step(logger, agent_name, "STARTED")
        
        transcript = state.get("transcript", "")
        
        if not transcript:
            log_step(logger, agent_name, "SKIPPED")
            return {"pronunciation_quality_analysis": None}
        
        llm = get_llm()
        structured_llm = llm.with_structured_output(PronunciationFeedback)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert IELTS Speaking examiner specializing in Pronunciation."),
            ("user", """
            Analyze the following transcript for Pronunciation quality.
            
            Transcript: {transcript}
            
            Provide a structured assessment including:
            1. score (0-9): Pronunciation score based on IELTS criteria
            2. evaluation: List of evaluation details with criteria (e.g., 'Strengths', 'Weaknesses', 'Improvements') and detailed descriptions
            3. errors: List of pronunciation issues inferred from the text with:
               - original: The text segment with potential pronunciation issues
               - suggested: Phonetic or pronunciation guidance
               - explanation: Why this might be challenging and how to improve
            4. feedback: Overall feedback on pronunciation quality
            
            Note: Since you're analyzing text, infer pronunciation issues from spelling errors, 
            word choice that might indicate mispronunciation, or patterns suggesting accent interference.
            """)
        ])
        
        chain = prompt | structured_llm
        response = chain.invoke({"transcript": transcript})
        
        result = {"pronunciation_quality_analysis": response.model_dump()}
        
        log_step(logger, agent_name, "COMPLETED")
        return result
        
    except Exception as e:
        log_step(logger, agent_name, "FAILED")
        logger.error(f"{agent_name} error: {str(e)}")
        raise
