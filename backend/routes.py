from fastapi import APIRouter, UploadFile, File, Request
from backend.RAG.ingestion import PDFIngestor
from backend.RAG.vectorstore import VectorStore
from backend.agent import generate_answers
from pydantic import BaseModel
import os

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to your AI assistant!"}

# Initialize components globally (shared across requests)
ingestor = PDFIngestor()
vector_store = VectorStore(embedding_dim=384, index_path="indexes/my_index.faiss")


"""Need to implement an /upload endpoint. It needs to accept a file (PDF), 
pass it to the PDF ingestor, extract -> chunk -> embed, and store embeddings."""


# Route for uploading and processing a PDF
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True) # If no data file exists, a new one will be created automatically
    
    contents = await file.read()
    
    # Save file temporarily so the PDFIngestor can read it
    temp_path = f"data/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    # Ingestion pipeline: extract text → split into chunks → embed
    text = ingestor.extract_text(temp_path)
    chunks = ingestor.chunk_text(text)
    embeddings = ingestor.embed_chunks(chunks)

    # Create metadata per chunk 
    metadatas = [{"source": file.filename, "chunk": i, "text": chunk} for i, chunk in enumerate(chunks)]

    
    # Store embeddings and metadata in the FAISS index
    vector_store.add_embeddings(embeddings, metadatas)
    vector_store.save_index("indexes/my_index.faiss")

    return {"message": f"{file.filename} uploaded and processed!"}



"""Implementing the /query endpoint. It will accept a user query as a text input, 
embed the query, and use FAISS to find the best suited document chunks. Return the matches
as raw chunks. The generated output will be a separate concern."""

class QueryRequest(BaseModel):
    # Tells FastAPI to expect a JSON object 
    query:str 


@router.post("/query")
async def query_endpoint(request: QueryRequest):
    top_chunks = vector_store.query_search(request.query, k=5)
    return {"results": top_chunks}

"""The generate endpoint which will call the LLM to get a generated
response. """

@router.post("/generate")
async def generate_endpoint(request: QueryRequest):
    # Retrieve the top chunks from the vector DB
    top_chunks = vector_store.query_search(request.query, k=5)
    
    # Feed them into the LLM generator 
    response = generate_answers(request.query, top_chunks)
    
    return response

