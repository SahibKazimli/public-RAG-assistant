from langchain.vectorstores import FAISS
from ingestion import PDFIngestor
import numpy as np 
import faiss
import pickle
import os


"""The file creating the vector store database, where the user's uploaded files 
will be stored. """

class VectorStore(): 
    def __init__(self, embedding_dim : int, index_path: str = None):
        self.index_path = index_path
        self.embedding_dim = embedding_dim
        self.metadata = {} # Map vector id to data
        
        if index_path and os.path.exists(index_path):
            # Load existing index
            self.index = faiss.read_index(index_path)
            print(f"Loaded index from {index_path}")
            
            # Load metadata
            meta_path = index_path + ".meta"
            if os.path.exists(meta_path):
                with open(meta_path, "rb") as f:
                    self.metadata = pickle.load(f)
                print(f"Loaded metadata from {meta_path}")
            else:
                print("No metadata file found, starting with empty metadata.")
              
            
        else: 
            # Create a new index 
            self.index = faiss.IndexFlatL2(embedding_dim)
            print("Created new FAISS index.")



    def add_embeddings(self, embeddings: list[list[float]], metadatas: list[dict]=None):
        # Add new embeddings (vectors) and metadata (optional) to the index
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Handle optional metadata
        if metadatas: 
            start_id = len(self.metadata)
            for i, meta in enumerate(metadatas):
                self.metadata[start_id + i] = meta
    
    
    def save_index(self, index_path: str):
        # Saves index and metadata to disk. 
        path = index_path or self.index_path
        if path is None: 
            raise ValueError("No path specified for saving index.")
        
        faiss.write_index(self.index, path)
        with open(path + ".meta", "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"Saved FAISS index and metadata to {path} and {path}.meta")
        
                
        
    
    
        
        
        
