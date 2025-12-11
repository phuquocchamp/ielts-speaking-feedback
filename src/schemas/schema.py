from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    original: str = Field(description="The original text with error")
    suggested: str = Field(description="The suggested correction")
    explanation: str = Field(description="Explanation of the error and correction")

class EvaluationDetail(BaseModel):
    criteria: str = Field(description="The evaluation criteria (e.g., Strengths, Weaknesses, Improvements)")
    description: str = Field(description="Detailed description for this criteria")

class SectionFeedback(BaseModel):
    score: float = Field(description="Score for this section (0-9)")
    evaluation: List[EvaluationDetail] = Field(default_factory=list, description="Evaluation details by level/criteria")
    errors: List[ErrorDetail] = Field(default_factory=list, description="List of errors found in this section")
    feedback: str = Field(default="", description="Overall feedback for this section")

class FluencyFeedback(SectionFeedback):
    wpm: Optional[float] = Field(default=None, description="Words per minute calculation")

class PronunciationFeedback(SectionFeedback):
    pass

class GrammarFeedback(SectionFeedback):
    pass

class VocabularyFeedback(SectionFeedback):
    pass

class DetailsFeedback(BaseModel):
    fluency: FluencyFeedback = Field(description="Fluency and coherence feedback")
    pronunciation: PronunciationFeedback = Field(description="Pronunciation feedback")
    grammar: GrammarFeedback = Field(description="Grammatical range and accuracy feedback")
    vocabulary: VocabularyFeedback = Field(description="Lexical resource feedback")

class IELTSFeedback(BaseModel):
    overall_score: float = Field(description="Overall IELTS Band Score (0-9)")
    questions: List[str] = Field(default_factory=list, description="List of questions asked")
    transcript: str = Field(description="Transcribed text from the audio")
    details: DetailsFeedback = Field(description="Detailed breakdown by section")
    general_suggestions: List[str] = Field(default_factory=list, description="General suggestions for improvement")
