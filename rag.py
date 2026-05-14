from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
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
embeddings = HuggingFaceEmbeddings(
           model_name = "BAAI/bge-small-en-v1.5",
           model_kwargs = {"device" : "cpu"},
           encode_kwargs = {"normalize_embeddings" : True}
)

# Vector Database
vector_db = Chroma.from_documents(
            documents = chunks, 
            embedding = embeddings,
            persist_directory = "chroma_db")

# Retriever
retriever = vector_db.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k" : 5}
)

if __name__ == "__main__":
    answers = retriever.invoke("identity verification and refund dispute handling")
    for answer in answers:
        print(answer.page_content, " -> ", answer.metadata)