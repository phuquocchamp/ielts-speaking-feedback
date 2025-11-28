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
        fluency = state.get("pronunciation_analysis", {})
        pronunciation = state.get("pronunciation_quality_analysis", {})
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
            Fluency Analysis:
            {fluency}
            
            ---
            Pronunciation Analysis:
            {pronunciation}
            
            ---
            Grammar Analysis:
            {grammar}
            
            ---
            Vocabulary Analysis:
            {vocabulary}
            
            ---
            
            Provide a structured output including:
            1. overall_score (0-9): The overall IELTS band score
            2. transcript: The original transcript
            3. details: Contains four sections (fluency, pronunciation, grammar, vocabulary) - use the analyzed data above
               - For fluency: use the fluency analysis provided
               - For pronunciation: use the pronunciation analysis provided
               - For grammar: use the grammar analysis provided
               - For vocabulary: use the vocabulary analysis provided
            4. general_suggestions: List of general improvement suggestions
            
            Note: Each section in details should have score, evaluation, errors, and feedback fields.
            """)
        ])
        
        chain = prompt | structured_llm
        response = chain.invoke({
            "transcript": transcript,
            "fluency": fluency,
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
