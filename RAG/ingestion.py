from PyPDF2 import PdfReader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import CharacterTextSplitter


"""The data ingestion file of the project. As of now, the intended 
capability is to just handle the text within PDF-files, ignoring handwritten text
and images. This functionality will hopefully be added in the future."""

class PDFIngestor:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2"):
        # Initialize the embedding model once
        self.embedding_model = SentenceTransformerEmbeddings(model_name=embedding_model_name)
        self.text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base", chunk_size=1000, chunk_overlap=200
        )


    def extract_text(self, file_path):
        # Load PDF and extract text 
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
            
        return text 
        
        

    def chunk_text(self, text, chunk_size=1000, chunk_overlap = 200):
        # Chunks the text based on tokens
        chunks = self.text_splitter.split_text(text)
        return chunks



    def embed_chunks(self, chunks):
        # Use our initialized embedding model 
        embeddings = self.embedding_model.embed_documents(chunks)
        return embeddings
        
        