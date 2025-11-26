from langchain_core.prompts import ChatPromptTemplate
from src.utils.state import AgentState
from src.utils.config import get_llm
from src.schemas.schema import IELTSFeedback
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def generate_feedback(state: AgentState) -> AgentState:
    """
    Aggregates all analysis and generates a final IELTS feedback report with a band score.
    """
    agent_name = "Feedback Generator"
    
    try:
        log_step(logger, agent_name, "STARTED")
        
        transcript = state.get("transcript", "")
        pronunciation = state.get("pronunciation_analysis", {})
        grammar = state.get("grammar_analysis", {})
        vocabulary = state.get("vocabulary_analysis", {})
        
        if not transcript:
            log_step(logger, agent_name, "SKIPPED")
            return {"final_feedback": None}
        
        llm = get_llm()
        structured_llm = llm.with_structured_output(IELTSFeedback)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a senior IELTS Speaking Examiner. Your task is to provide a final score and comprehensive feedback report."),
            ("user", """
            Based on the following analyses, provide a final IELTS Speaking Report.
            
            Transcript: {transcript}
            
            ---
            Pronunciation & Fluency Analysis:
            {pronunciation}
            
            ---
            Grammar Analysis:
            {grammar}
            
            ---
            Vocabulary Analysis:
            {vocabulary}
            
            ---
            
            Provide a structured output including:
            1. Overall Band Score (0-9)
            2. Detailed Breakdown (Fluency, Lexical, Grammar, Pronunciation) - You can reuse the sub-scores or adjust them for the final holistic score.
            3. General Suggestions for Improvement
            """)
        ])
        
        chain = prompt | structured_llm
        response = chain.invoke({
            "transcript": transcript,
            "pronunciation": pronunciation,
            "grammar": grammar,
            "vocabulary": vocabulary
        })
        
        result = {"final_feedback": response.model_dump()}
        
        log_step(logger, agent_name, "COMPLETED")
        return result
        
    except Exception as e:
        log_step(logger, agent_name, "FAILED")
        logger.error(f"{agent_name} error: {str(e)}")
        raise
