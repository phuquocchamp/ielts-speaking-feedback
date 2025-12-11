from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    """
    Represents the state of the IELTS Speaking Feedback agent.
    """
    audio_path: str
    transcript: Optional[str]
    duration: Optional[float]  # in seconds
    questions: Optional[list[str]]  # List of questions asked
    
    # Analysis results (stored as dictionaries matching the Pydantic models)
    pronunciation_analysis: Optional[Dict[str, Any]]  # Fluency analysis
    pronunciation_quality_analysis: Optional[Dict[str, Any]]  # Pronunciation analysis
    grammar_analysis: Optional[Dict[str, Any]]
    vocabulary_analysis: Optional[Dict[str, Any]]
    
    # Final output
    final_feedback: Optional[Dict[str, Any]]
