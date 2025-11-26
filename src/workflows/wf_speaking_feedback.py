from langgraph.graph import StateGraph, END
from src.utils.state import AgentState
from src.agents.transcriber import transcribe_audio
from src.agents.pronunciation import analyze_pronunciation
from src.agents.grammar import analyze_grammar
from src.agents.vocabulary import analyze_vocabulary
from src.agents.feedback import generate_feedback
from src.utils.logger import setup_logger, log_step

logger = setup_logger(__name__)

def create_graph():
    """
    Constructs the IELTS Speaking Feedback LangGraph.
    """
    log_step(logger, "Workflow Graph Initialization", "STARTED")
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("transcribe", transcribe_audio)
    workflow.add_node("analyze_pronunciation", analyze_pronunciation)
    workflow.add_node("analyze_grammar", analyze_grammar)
    workflow.add_node("analyze_vocabulary", analyze_vocabulary)
    workflow.add_node("generate_feedback", generate_feedback)
    
    # Define edges
    workflow.set_entry_point("transcribe")
    
    # After transcription, run analyses in parallel
    workflow.add_edge("transcribe", "analyze_pronunciation")
    workflow.add_edge("transcribe", "analyze_grammar")
    workflow.add_edge("transcribe", "analyze_vocabulary")
    
    # After all analyses are done, generate feedback
    workflow.add_edge("analyze_pronunciation", "generate_feedback")
    workflow.add_edge("analyze_grammar", "generate_feedback")
    workflow.add_edge("analyze_vocabulary", "generate_feedback")
    
    # End
    workflow.add_edge("generate_feedback", END)
    
    compiled_graph = workflow.compile()
    
    log_step(logger, "Workflow Graph Initialization", "COMPLETED")
    
    return compiled_graph
