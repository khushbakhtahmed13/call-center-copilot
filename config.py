from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# API KEYS
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Transcription
whisper_model = WhisperModel("base", device = "cpu", compute_type = "int8")

# Diarization
diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token = HF_TOKEN
    )

# Embeddings 
embeddings = HuggingFaceEmbeddings(
           model_name = "BAAI/bge-small-en-v1.5",
           model_kwargs = {"device" : "cpu"},
           encode_kwargs = {"normalize_embeddings" : True}
)

# Load vector database
vector_db = Chroma(
            persist_directory = "chroma_db",
            embedding_function = embeddings 
)

# Create retriever
retriever = vector_db.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k" : 5}
)

# LLM
llm = ChatGroq(
      model = "llama-3.3-70b-versatile",
      temperature = 0,
      api_key = GROQ_API_KEY
)