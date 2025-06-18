from fastapi import APIRouter, UploadFile, File
from RAG.ingestion import PDFIngestor
from RAG.vectorstore import VectorStore

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
    metadatas = [{"source": file.filename, "chunk": i} for i in range(len(chunks))]
    
    
    # Store embeddings and metadata in the FAISS index
    vector_store.add_embeddings(embeddings, metadatas)
    vector_store.save_index("indexes/my_index.faiss")

    return {"message": f"{file.filename} uploaded and processed!"}