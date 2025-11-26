# IELTS Speaking Feedback API

An AI-powered IELTS Speaking assessment system that provides comprehensive feedback on pronunciation, fluency, grammar, and vocabulary using LangChain, LangGraph, and OpenAI.

## 🎯 Features

- **🎤 Audio Processing**: Accepts MP3, WAV, M4A, and OGG audio files
- **📝 Speech-to-Text**: High-quality transcription using OpenAI Whisper
- **🤖 Multi-Agent Analysis**: Specialized AI agents for:
  - Pronunciation and Fluency
  - Grammar and Accuracy
  - Vocabulary and Lexical Resource
- **📊 IELTS Band Scoring**: Comprehensive scoring (0.0-9.0) across all criteria
- **🔄 LangGraph Workflow**: Orchestrated multi-agent workflow with parallel processing
- **🚀 FastAPI REST API**: Production-ready RESTful API endpoint
- **🐳 Docker Support**: Containerized deployment with Docker Compose
- **📋 Status Logging**: Real-time tracking of workflow execution steps

## 📋 Requirements

- Python 3.11+ or Python 3.12+
- OpenAI API key
- Docker and Docker Compose (for containerized deployment)

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ielts-speaking-feedback
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your configuration:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   PORT=8000  # Optional, defaults to 8000
   ```

3. **Start with Docker Compose (Detached Mode)**
   ```bash
   docker-compose up -d
   ```
   
   This will:
   - Build the Docker image
   - Start the container in the background
   - Enable hot-reload for development
   - Map port 8000 to your localhost

4. **View logs** (optional)
   ```bash
   docker-compose logs -f
   ```

5. **Access the API**
   
   The API will be available at `http://localhost:8000`
   
   API Documentation: `http://localhost:8000/docs`

6. **Stop the service**
   ```bash
   docker-compose down
   ```

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ielts-speaking-feedback
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

5. **Run the API server**
   ```bash
   uvicorn src.api.handler:app --host 0.0.0.0 --port 8000 --reload
   ```

## 📁 Project Structure

```
ielts-speaking-feedback/
├── src/
│   ├── agents/              # AI agents for analysis
│   │   ├── transcriber.py   # Audio transcription agent (Whisper)
│   │   ├── pronunciation.py # Pronunciation & fluency analysis
│   │   ├── grammar.py       # Grammar analysis
│   │   ├── vocabulary.py    # Vocabulary analysis
│   │   └── feedback.py      # Final feedback aggregation
│   │
│   ├── api/                 # FastAPI application
│   │   └── handler.py       # API endpoints and request handling
│   │
│   ├── schemas/             # Pydantic models
│   │   └── schema.py        # Data models for feedback structure
│   │
│   ├── utils/               # Utility modules
│   │   ├── config.py        # LLM configuration (OpenAI)
│   │   ├── logger.py        # Logging utilities
│   │   └── state.py         # LangGraph state management
│   │
│   └── workflows/           # LangGraph workflows
│       └── wf_speaking_feedback.py  # Main workflow orchestration
│
├── logs/                    # Application logs (auto-generated)
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔌 API Usage

### Endpoint: POST `/process/speaking`

Process an audio file and receive IELTS speaking feedback.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Audio file (MP3, WAV, M4A, or OGG)

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/process/speaking" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_audio.mp3"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/process/speaking"
files = {"file": open("your_audio.mp3", "rb")}

response = requests.post(url, files=files)
feedback = response.json()

print(f"Overall Band Score: {feedback['overall_band_score']}")
print(f"Transcript: {feedback['transcript']}")
```

**Response Structure:**
```json
{
  "overall_band_score": 7.5,
  "transcript": "The transcribed text from your audio...",
  "detailed_breakdown": {
    "fluency_and_coherence": {
      "wpm": 145.5,
      "fluency_score": 7.5,
      "pronunciation_score": 7.0,
      "feedback": "Detailed feedback on fluency..."
    },
    "lexical_resource": {
      "vocabulary_score": 8.0,
      "suggestions": [
        {
          "original": "good",
          "suggestion": "excellent",
          "context": "Use 'excellent' to show stronger approval"
        }
      ],
      "feedback": "Detailed vocabulary feedback..."
    },
    "grammatical_range_and_accuracy": {
      "grammar_score": 7.0,
      "errors": [
        {
          "error": "I was went to the store",
          "correction": "I went to the store",
          "explanation": "Remove auxiliary 'was' with simple past"
        }
      ],
      "feedback": "Detailed grammar feedback..."
    },
    "pronunciation": {
      "wpm": 145.5,
      "fluency_score": 7.5,
      "pronunciation_score": 7.0,
      "feedback": "Detailed pronunciation feedback..."
    }
  },
  "general_suggestions": [
    "Practice using more advanced vocabulary",
    "Focus on complex sentence structures",
    "Work on pronunciation of specific sounds"
  ]
}
```

## 🏗️ Architecture

### Workflow Pipeline

The system uses LangGraph to orchestrate a multi-agent workflow:

```
Audio File Upload
    ↓
[Transcription Agent]
  - OpenAI Whisper
  - Word-level timestamps
    ↓
┌─────────────────────────────────┐
│   Parallel Analysis Agents      │
├─────────────────────────────────┤
│ • Pronunciation & Fluency       │
│ • Grammar & Accuracy            │
│ • Vocabulary & Lexical Resource │
└─────────────────────────────────┘
    ↓
[Feedback Aggregation Agent]
  - Combine all analyses
  - Calculate overall band score
  - Generate suggestions
    ↓
JSON Response
```

### Technology Stack

- **Framework**: FastAPI
- **AI Orchestration**: LangChain, LangGraph
- **AI Models**: OpenAI GPT-4 (analysis), Whisper (transcription)
- **Audio Processing**: pydub, ffmpeg
- **Data Validation**: Pydantic
- **Containerization**: Docker, Docker Compose

## 🔧 Development

### Quick Development Start (Recommended)

Start the development server with Docker Compose in detached mode:

```bash
# Start in background with hot-reload
docker-compose up -d

# View logs in real-time
docker-compose logs -f

# Stop the service
docker-compose down
```

The docker-compose setup includes:
- ✅ **Hot-reload**: Code changes in `./src` are reflected immediately
- ✅ **Background mode**: Runs in detached mode with `-d` flag
- ✅ **Port mapping**: Access API at `http://localhost:8000`
- ✅ **Auto-restart**: Container restarts automatically on failure

### Running in Development Mode (Without Docker)

With hot-reload enabled:

```bash
uvicorn src.api.handler:app --host 0.0.0.0 --port 8000 --reload
```

### Useful Docker Commands

```bash
# Rebuild and start (after dependency changes)
docker-compose up -d --build

# View running containers
docker-compose ps

# View logs
docker-compose logs -f api

# Stop and remove containers
docker-compose down

# Stop, remove containers and volumes
docker-compose down -v

# Execute commands inside container
docker-compose exec api bash
```

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key for GPT-4 and Whisper | - |
| `PORT` | No | Port number for the API server | 8000 |

### Logging System

The application includes a simplified logging system that tracks the status of each step and agent:

**Log Format:**
```
YYYY-MM-DD HH:MM:SS - LEVEL - message
```

**Status Types:**
- `[STARTED]` - Step/Agent begins execution
- `[COMPLETED]` - Step/Agent completes successfully
- `[FAILED]` - Step/Agent encounters an error
- `[SKIPPED]` - Step/Agent is skipped (conditions not met)

**Example Log Output:**
```
2025-11-26 21:46:00 - INFO - [REQUEST a1b2c3d4] Processing audio: sample.mp3
2025-11-26 21:46:01 - INFO - [STARTED] Workflow Graph Initialization
2025-11-26 21:46:01 - INFO - [COMPLETED] Workflow Graph Initialization
2025-11-26 21:46:02 - INFO - [STARTED] Transcriber
2025-11-26 21:46:05 - INFO - [COMPLETED] Transcriber
2025-11-26 21:46:05 - INFO - [STARTED] Pronunciation Analyzer
2025-11-26 21:46:05 - INFO - [STARTED] Grammar Analyzer
2025-11-26 21:46:05 - INFO - [STARTED] Vocabulary Analyzer
2025-11-26 21:46:08 - INFO - [COMPLETED] Pronunciation Analyzer
2025-11-26 21:46:09 - INFO - [COMPLETED] Grammar Analyzer
2025-11-26 21:46:10 - INFO - [COMPLETED] Vocabulary Analyzer
2025-11-26 21:46:10 - INFO - [STARTED] Feedback Generator
2025-11-26 21:46:12 - INFO - [COMPLETED] Feedback Generator
```

**View Logs:**
```bash
# With Docker
docker-compose logs -f

# Local development - logs appear in console
```

## 🐳 Docker Configuration

### Dockerfile

The Dockerfile is based on `python:3.12-slim` and includes:
- System dependency: `ffmpeg` (required for audio processing)
- Python dependencies from `requirements.txt`
- Application source code
- Configurable port via `PORT` environment variable (default: 8000)
- Dynamic `EXPOSE` directive based on `PORT`

### Docker Compose

The `docker-compose.yml` provides:
- Automatic build configuration
- Dynamic port mapping using `PORT` environment variable
- Environment variable loading from `.env`
- Volume mounting for development (`./src:/app/src`)
- Auto-restart policy

**Custom Port Example:**

To run on a different port, update your `.env` file:
```bash
PORT=9000
```

Then restart the service:
```bash
docker-compose down
docker-compose up -d
```

The API will be available at `http://localhost:9000`

## 📊 IELTS Scoring Criteria

The system evaluates speaking performance across four key criteria:

1. **Fluency and Coherence** (0-9)
   - Speech rate (words per minute)
   - Pauses and hesitations
   - Logical flow of ideas

2. **Lexical Resource** (0-9)
   - Vocabulary range
   - Appropriate word choice
   - Idiomatic expressions

3. **Grammatical Range and Accuracy** (0-9)
   - Sentence complexity
   - Grammar errors
   - Tense usage

4. **Pronunciation** (0-9)
   - Clarity and intelligibility
   - Intonation and stress
   - Individual sound production

**Overall Band Score**: Average of all four criteria

## 💰 Cost Estimation

Per audio file (~5 minutes):
- **Whisper API**: ~$0.036 (transcription)
- **GPT-4 API**: ~$0.15-$0.30 (analysis)
- **Total**: ~$0.20-$0.35 per request

## 🔒 Security Notes

- Never commit your `.env` file with real API keys
- Use environment variables for all sensitive configuration
- The API currently has no authentication - add authentication for production use
- Temporary audio files are automatically cleaned up after processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🔗 Resources

- [LangChain Documentation](https://docs.langchain.com)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

## 📞 Support

For issues or questions:
- Create an issue in this repository
- Check the API documentation at `/docs` endpoint
- Review the code examples above

---

**Status**: ✅ Production Ready

**Last Updated**: 2025-11-26