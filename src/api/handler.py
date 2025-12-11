import os
import shutil
import uuid
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.workflows.wf_speaking_feedback import create_graph
from src.schemas.schema import IELTSFeedback
from src.utils.logger import setup_logger, log_step
import uvicorn

logger = setup_logger(__name__)

app = FastAPI(title="IELTS Speaking Feedback API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development; restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process/speaking", response_model=IELTSFeedback)
async def process_speaking(file: UploadFile = File(...)):
    """
    Process an audio file and return IELTS speaking feedback.
    [TEMPORARY] Returning mock data for testing purposes.
    """
    request_id = str(uuid.uuid4())[:8]
    
    logger.info("=" * 80)
    logger.info(f"[REQUEST {request_id}] Processing audio: {file.filename}")
    logger.info(f"[REQUEST {request_id}] Content-Type: {file.content_type}")
    logger.info(f"[REQUEST {request_id}] ⚠️  RETURNING MOCK DATA FOR TESTING")
    logger.info("=" * 80)
    
    # Validate file type
    if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
        logger.error(f"[REQUEST {request_id}] Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an audio file.")
    
    # Mock response data for testing
    MOCK_FEEDBACK = {
        "overall_score": 6.0,
        "transcript": "Hello, my name is Woop, and this is the example how I can use this recorder to test my API. And I feel this build works well, and I hope that it will help everyone to use this feature too.",
        "details": {
            "fluency": {
                "score": 6.0,
                "evaluation": [
                    {
                        "criteria": "Strengths",
                        "description": "The speaker maintains a steady pace and is able to convey the main message clearly. The speaking rate of 116.96 WPM is within a reasonable range for natural speech."
                    },
                    {
                        "criteria": "Weaknesses",
                        "description": "The speech lacks variety in sentence structure and complexity, which can make it sound somewhat monotonous. There is also a minor issue with coherence as the transition between ideas is not very smooth."
                    },
                    {
                        "criteria": "Improvements",
                        "description": "To improve, the speaker could work on using a wider range of sentence structures and incorporating more complex ideas. Additionally, using linking words or phrases could help in making the speech more coherent and fluid."
                    }
                ],
                "errors": [
                    {
                        "original": "this is the example how I can use this recorder",
                        "suggested": "this is an example of how I can use this recorder",
                        "explanation": "The phrase 'this is the example how' is awkward and lacks clarity. Using 'an example of how' is more grammatically correct and clearer."
                    }
                ],
                "feedback": "The speaker demonstrates a basic level of fluency and coherence, with a clear message and a steady speaking rate. However, the speech could benefit from more varied sentence structures and smoother transitions between ideas. Addressing these areas would enhance the overall fluency and coherence of the speech.",
                "wpm": 116.96
            },
            "pronunciation": {
                "score": 6.0,
                "evaluation": [
                    {
                        "criteria": "Strengths",
                        "description": "The speaker demonstrates a clear understanding of the basic sounds of English and can be understood without much effort. The speech is generally intelligible."
                    },
                    {
                        "criteria": "Weaknesses",
                        "description": "There are some issues with word stress and intonation that may affect the natural flow of speech. Additionally, there might be some influence of the speaker's native language on certain sounds."
                    },
                    {
                        "criteria": "Improvements",
                        "description": "The speaker should focus on practicing word stress and intonation patterns typical of English. Listening to native speakers and mimicking their pronunciation can be beneficial. Additionally, working on specific sounds that are influenced by the speaker's native language can help improve clarity."
                    }
                ],
                "errors": [
                    {
                        "original": "Woop",
                        "suggested": "[wuːp]",
                        "explanation": "The name 'Woop' might be pronounced with a non-standard vowel sound. Ensuring the vowel sound is clear and matches the intended pronunciation can help."
                    },
                    {
                        "original": "example",
                        "suggested": "[ɪɡˈzæmpəl]",
                        "explanation": "The word 'example' might be mispronounced with incorrect stress or vowel sounds. The stress should be on the second syllable, and the vowel sounds should be clear."
                    },
                    {
                        "original": "recorder",
                        "suggested": "[rɪˈkɔːrdər]",
                        "explanation": "The word 'recorder' might be pronounced with incorrect stress or vowel sounds. The stress should be on the second syllable, and the 'r' sounds should be clear."
                    }
                ],
                "feedback": "The speaker's pronunciation is generally understandable, but there are areas that need improvement to achieve a more natural and fluent delivery. Focusing on word stress, intonation, and specific vowel and consonant sounds will enhance clarity and comprehensibility."
            },
            "grammar": {
                "score": 6.0,
                "evaluation": [
                    {
                        "criteria": "Strengths",
                        "description": "The speaker demonstrates a basic command of English grammar, with the ability to construct simple sentences that convey the intended message. The use of conjunctions like 'and' and 'that' shows an attempt to connect ideas."
                    },
                    {
                        "criteria": "Weaknesses",
                        "description": "There are noticeable errors in article usage and sentence structure, which can impede clarity. The sentence structure is somewhat repetitive, lacking variety and complexity."
                    },
                    {
                        "criteria": "Improvements",
                        "description": "The speaker should focus on improving article usage and sentence variety. Practicing more complex sentence structures and ensuring subject-verb agreement will enhance clarity and coherence."
                    }
                ],
                "errors": [
                    {
                        "original": "this is the example how I can use this recorder",
                        "suggested": "this is an example of how I can use this recorder",
                        "explanation": "The article 'the' is incorrectly used here. 'An' is needed before 'example' because it is a singular, countable noun. Additionally, 'of' is required to correctly form the phrase 'example of how'."
                    }
                ],
                "feedback": "The speaker shows a basic understanding of English grammar, but there are several areas for improvement. The use of articles and prepositions needs attention, and the speaker should work on varying sentence structures to enhance grammatical range. Overall, the message is understandable, but more complex structures and accurate grammar usage would improve the score."
            },
            "vocabulary": {
                "score": 5.0,
                "evaluation": [
                    {
                        "criteria": "Strengths",
                        "description": "The speaker uses basic vocabulary accurately and appropriately for the context. The message is clear and understandable."
                    },
                    {
                        "criteria": "Weaknesses",
                        "description": "The vocabulary is quite limited and lacks variety. There is a reliance on simple words and phrases, which does not demonstrate a wide range of vocabulary."
                    },
                    {
                        "criteria": "Improvements",
                        "description": "To improve, the speaker should incorporate more varied and sophisticated vocabulary. Using synonyms and more precise language can enhance the lexical resource."
                    }
                ],
                "errors": [
                    {
                        "original": "this is the example how I can use",
                        "suggested": "this is an example of how I can use",
                        "explanation": "The phrase 'this is the example how I can use' is awkward and incorrect. 'An example of how' is a more natural and grammatically correct expression."
                    },
                    {
                        "original": "this build works well",
                        "suggested": "this setup functions effectively",
                        "explanation": "'Build' is more commonly used in technical contexts related to software development. 'Setup' or 'configuration' might be more appropriate here, and 'functions effectively' is a more advanced way to express that something works well."
                    }
                ],
                "feedback": "The speaker demonstrates a basic level of vocabulary suitable for everyday communication. However, to achieve a higher score, it is important to use a wider range of vocabulary, including more complex and precise words. The speaker should also focus on using idiomatic expressions and collocations to enhance the naturalness and sophistication of their language."
            }
        },
        "general_suggestions": [
            "Work on using a wider range of sentence structures to avoid monotony and improve coherence.",
            "Practice word stress and intonation patterns to enhance pronunciation clarity.",
            "Focus on improving article usage and sentence variety to enhance grammatical accuracy.",
            "Incorporate more varied and sophisticated vocabulary to demonstrate a wider lexical range."
        ]
    }
    
    # Simulate some processing time
    time.sleep(0.5)
    
    logger.info(f"[REQUEST {request_id}] ✓ Returning mock feedback successfully")
    logger.info("=" * 80)
    
    return MOCK_FEEDBACK
    
    # ============================================================================
    # COMMENTED OUT: Real processing workflow (uncomment when ready for production)
    # ============================================================================
    # temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    # temp_path = os.path.join("/tmp", temp_filename)
    # 
    # try:
    #     with open(temp_path, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)
    #     
    #     # Initialize graph
    #     graph = create_graph()
    #     
    #     # Run workflow
    #     log_step(logger, f"[REQUEST {request_id}] Workflow Execution", "STARTED")
    #     
    #     initial_state = {
    #         "audio_path": temp_path
    #     }
    #     
    #     result = graph.invoke(initial_state)
    #     
    #     log_step(logger, f"[REQUEST {request_id}] Workflow Execution", "COMPLETED")
    #     
    #     final_feedback = result.get("final_feedback")
    #     
    #     if not final_feedback:
    #         logger.error(f"[REQUEST {request_id}] No feedback generated")
    #         raise HTTPException(status_code=500, detail="Failed to generate feedback.")
    #     
    #     logger.info(f"[REQUEST {request_id}] ✓ Request completed successfully")
    #     logger.info("=" * 80)
    #     
    #     return final_feedback
    #     
    # except HTTPException:
    #     raise
    # except Exception as e:
    #     log_step(logger, f"[REQUEST {request_id}] Workflow Execution", "FAILED")
    #     logger.error(f"[REQUEST {request_id}] Error: {str(e)}")
    #     logger.info("=" * 80)
    #     raise HTTPException(status_code=500, detail=str(e))
    #     
    # finally:
    #     # Cleanup
    #     if os.path.exists(temp_path):
    #         os.remove(temp_path)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "IELTS Speaking Feedback API"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting IELTS Speaking Feedback API server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

