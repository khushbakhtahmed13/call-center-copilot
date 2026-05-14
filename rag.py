from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# Data Ingestion
loader = DirectoryLoader("data/policies/", glob = "*.txt", loader_cls = TextLoader, loader_kwargs = {"encoding" : "utf-8"})
documents = loader.load()

# Chunking
splitter = RecursiveCharacterTextSplitter(
           chunk_size = 500,
           chunk_overlap = 50
)

chunks = splitter.split_documents(documents)

# Embedding
from embeddings import embeddings

# Vector Database
vector_db = Chroma.from_documents(
            documents = chunks, 
            embedding = embeddings,
            persist_directory = "chroma_db")


