"""Vector store creation and management"""
import pickle
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from data_processor import GymDataProcessor
from config import VECTORSTORE_PATH, EMBEDDING_MODEL

class VectorStoreManager:
    def __init__(self):
        self.vectorstore = None
        self.embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    def load_or_create_vectorstore(self):
        """Load existing vectorstore or create new one"""
        if os.path.exists(VECTORSTORE_PATH):
            print("Loading existing vectorstore...")
            
            allow_dangerous_deserialization=True
            #self.vectorstore = FAISS.load_local(VECTORSTORE_PATH, self.embedding)
            
        else:
            print("Creating new vectorstore...")
            self._create_vectorstore()
            self._save_vectorstore()
        
        return self.vectorstore
    
    def _create_vectorstore(self):
        """Create vectorstore from gym data"""
        processor = GymDataProcessor()
        data = processor.generate_exercise_descriptions()
        
        docs = [
            Document(page_content=row['llm_entry'], metadata={'Main_muscle': row['Main_muscle']})
            for _, row in data.iterrows()
        ]
        
        self.vectorstore = FAISS.from_documents(docs, self.embedding)
    
    def _save_vectorstore(self):
        """Save vectorstore to disk"""
        if self.vectorstore:
            self.vectorstore.save_local(VECTORSTORE_PATH)
            print(f"Vectorstore saved to {VECTORSTORE_PATH}")