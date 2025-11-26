from langchain_core.prompts import ChatPromptTemplate
from src.utils.state import AgentState
from src.utils.config import get_llm
from src.schemas.schema import VocabularyFeedback
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def analyze_vocabulary(state: AgentState) -> AgentState:
    """
    Analyzes lexical resource (vocabulary).
    """
    agent_name = "Vocabulary Analyzer"
    
    try:
        log_step(logger, agent_name, "STARTED")
        
        transcript = state.get("transcript", "")
        
        if not transcript:
            log_step(logger, agent_name, "SKIPPED")
            return {"vocabulary_analysis": None}
        
        llm = get_llm()
        structured_llm = llm.with_structured_output(VocabularyFeedback)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert IELTS Speaking examiner specializing in Lexical Resource."),
            ("user", """
            Analyze the following transcript for Vocabulary usage.
            
            Transcript: {transcript}
            
            Provide a structured assessment including:
            1. Vocabulary Score (0-9)
            2. Suggestions for improvement (better synonyms/idioms)
            3. General Feedback
            """)
        ])
        
        chain = prompt | structured_llm
        response = chain.invoke({"transcript": transcript})
        
        result = {"vocabulary_analysis": response.model_dump()}
        
        log_step(logger, agent_name, "COMPLETED")
        return result
        
    except Exception as e:
        log_step(logger, agent_name, "FAILED")
        logger.error(f"{agent_name} error: {str(e)}")
        raise
