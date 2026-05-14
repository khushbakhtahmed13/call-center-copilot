# AI-Powered Call Center QA Copilot Using LangGraph and RAG

## Overview

AI-Powered Call Center QA Copilot is an end-to-end conversational intelligence system designed to automate call center quality assurance and customer interaction analysis.

The system processes recorded customer support calls, converts them into structured transcripts using speech recognition and speaker diarization, and then applies a multi-agent AI workflow to generate actionable insights including:

* Call summaries
* Sentiment analysis
* Compliance verification
* Agent performance evaluation
* Risk detection and escalation analysis

The final results are visualized through an interactive Streamlit dashboard for real-time analytics and operational monitoring.

---

## Features

* Automated speech-to-text transcription using Faster-Whisper
* Speaker diarization using Pyannote Audio
* Multi-agent orchestration using LangGraph
* Retrieval-Augmented Generation (RAG) for policy-aware compliance analysis
* Customer sentiment and escalation risk detection
* Agent coaching and performance evaluation
* Interactive Streamlit dashboard
* Structured AI outputs using Pydantic schemas

---

## System Architecture

```text
Audio Call (.wav)
        ↓
Speech Transcription + Speaker Diarization
        ↓
Structured Transcript
        ↓
LangGraph Multi-Agent Workflow
    ├── Call Summarization
    ├── Sentiment Analysis
    ├── Compliance Analysis (RAG)
    ├── Agent Performance Evaluation
    └── Risk Detection
        ↓
Streamlit Analytics Dashboard
```

---

## Tech Stack

### AI / LLM

* Groq API
* Llama 3.3 70B
* LangGraph
* LangChain

### Speech Processing

* Faster-Whisper
* Pyannote Audio

### RAG Pipeline

* ChromaDB
* HuggingFace Embeddings (BAAI/bge-small-en-v1.5)

### Frontend / Visualization

* Streamlit
* Plotly

### Backend

* Python

---

## Project Structure

```text
project/
│
├── data/
│   ├── calls/
│   └── policies/
│
├── chroma_db/
│
├── app.py
├── graph.py
├── audio_processing.py
├── config.py
├── prompts.py
├── schemas.py
├── rag.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <your-github-repo>
cd <repo-name>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
```

---

## Running the Application

Place `.wav` call recordings inside:

```text
data/calls/
```

Then run:

```bash
streamlit run app.py
```

The system will automatically:

1. Detect the latest audio file
2. Generate transcript and speaker labels
3. Run the LangGraph analysis pipeline
4. Display insights on the dashboard

---

## Dashboard Analytics

The dashboard provides:

* Overall customer sentiment
* Agent performance scoring
* Compliance monitoring
* Escalation and churn risk detection
* Talk ratio analysis
* Call duration analytics
* Coaching recommendations
* Operational insights

---

## Future Improvements

* Real-time streaming call analysis
* Multi-language support
* Database integration
* Human feedback loops
* Authentication and user roles
* Advanced agent memory and evaluation

---

## Author

Khushbakht Ahmed
