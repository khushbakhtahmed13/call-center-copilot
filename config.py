from langchain_chroma import Chroma 
from rag import embeddings

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