from typing import List, Optional
from pydantic import BaseModel, Field

class PronunciationFeedback(BaseModel):
    wpm: float = Field(description="Words per minute calculation")
    fluency_score: float = Field(description="Estimated fluency score 0-9")
    pronunciation_score: float = Field(description="Estimated pronunciation score 0-9")
    feedback: str = Field(description="Detailed feedback on pronunciation and fluency")

class GrammarError(BaseModel):
    error: str = Field(description="The grammatical error found")
    correction: str = Field(description="The corrected version")
    explanation: str = Field(description="Explanation of the error")

class GrammarFeedback(BaseModel):
    grammar_score: float = Field(description="Estimated grammar score 0-9")
    errors: List[GrammarError] = Field(description="List of grammatical errors found")
    feedback: str = Field(description="General feedback on grammatical range and accuracy")

class VocabularySuggestion(BaseModel):
    original: str = Field(description="The original word or phrase used")
    suggestion: str = Field(description="A better synonym or idiom")
    context: str = Field(description="How to use the suggestion")

class VocabularyFeedback(BaseModel):
    vocabulary_score: float = Field(description="Estimated vocabulary score 0-9")
    suggestions: List[VocabularySuggestion] = Field(description="List of vocabulary suggestions")
    feedback: str = Field(description="General feedback on lexical resource")

class DetailedBreakdown(BaseModel):
    fluency_and_coherence: PronunciationFeedback
    lexical_resource: VocabularyFeedback
    grammatical_range_and_accuracy: GrammarFeedback
    pronunciation: PronunciationFeedback # Reusing PronunciationFeedback for simplicity, or separate if needed

class IELTSFeedback(BaseModel):
    overall_band_score: float = Field(description="Overall IELTS Band Score 0-9")
    transcript: str = Field(description="Transcribed text from the audio")
    detailed_breakdown: DetailedBreakdown
    general_suggestions: List[str] = Field(description="General suggestions for improvement")
