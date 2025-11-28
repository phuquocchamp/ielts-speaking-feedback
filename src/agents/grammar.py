from langchain_core.prompts import ChatPromptTemplate
from src.utils.state import AgentState
from src.utils.config import get_llm
from src.schemas.schema import GrammarFeedback
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def analyze_grammar(state: AgentState) -> AgentState:
    """
    Analyzes grammar accuracy and range.
    """
    agent_name = "Grammar Analyzer"
    
    try:
        log_step(logger, agent_name, "STARTED")
        
        transcript = state.get("transcript", "")
        
        if not transcript:
            log_step(logger, agent_name, "SKIPPED")
            return {"grammar_analysis": None}
        
        llm = get_llm()
        structured_llm = llm.with_structured_output(GrammarFeedback)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert IELTS Speaking examiner specializing in Grammatical Range and Accuracy."),
            ("user", """
            Analyze the following transcript for Grammatical errors and sentence structure.
            
            Transcript: {transcript}
            
            Provide a structured assessment including:
            1. score (0-9): Grammar score based on IELTS criteria
            2. evaluation: List of evaluation details with criteria (e.g., 'Strengths', 'Weaknesses', 'Improvements') and detailed descriptions
            3. errors: List of grammatical errors found with:
               - original: The incorrect text
               - suggested: The corrected version
               - explanation: Explanation of the grammatical error
            4. feedback: General feedback on grammatical range and accuracy
            """)
        ])
        
        chain = prompt | structured_llm
        response = chain.invoke({"transcript": transcript})
        
        result = {"grammar_analysis": response.model_dump()}
        
        log_step(logger, agent_name, "COMPLETED")
        return result
        
    except Exception as e:
        log_step(logger, agent_name, "FAILED")
        logger.error(f"{agent_name} error: {str(e)}")
        raise
