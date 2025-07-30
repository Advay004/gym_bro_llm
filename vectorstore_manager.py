import pickle
import os
import json
from datetime import datetime
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from data_processor import GymDataProcessor
from config import VECTORSTORE_PATH, EMBEDDING_MODEL

class VectorStoreManager:
    def __init__(self):
        self.vectorstore = None
        self.embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.metadata_file = os.path.join(VECTORSTORE_PATH, "metadata.json")
    
    def _get_data_hash(self):
        """Get a hash of the current data to detect changes"""
        try:
            processor = GymDataProcessor()
            data = processor.generate_exercise_descriptions()
            # Simple hash based on data shape and first few entries
            data_info = f"{len(data)}_{data.iloc[0]['llm_entry'][:100] if len(data) > 0 else ''}"
            return hash(data_info)
        except:
            return None
    
    def _save_metadata(self, data_hash):
        """Save metadata about the vectorstore"""
        metadata = {
            "created_at": datetime.now().isoformat(),
            "data_hash": data_hash,
            "embedding_model": EMBEDDING_MODEL,
            "num_documents": self._get_vectorstore_size()
        }
        
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _load_metadata(self):
        """Load metadata about the existing vectorstore"""
        if not os.path.exists(self.metadata_file):
            return None
        
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def _get_vectorstore_size(self):
        """Get the number of documents in the vectorstore"""
        if self.vectorstore is None:
            return 0
        try:
            # This is a rough estimate - FAISS doesn't have a direct count method
            test_search = self.vectorstore.similarity_search("test", k=1000)
            return len(test_search)
        except:
            return 0
    
    def _vectorstore_exists(self):
        """Check if vectorstore files exist"""
        return os.path.exists(VECTORSTORE_PATH) and os.path.exists(os.path.join(VECTORSTORE_PATH, "index.faiss"))
    
    def _should_rebuild_vectorstore(self):
        """Determine if vectorstore needs to be rebuilt"""
        if not self._vectorstore_exists():
            print("📁 No existing vectorstore found")
            return True
        
        metadata = self._load_metadata()
        if metadata is None:
            print("📁 No metadata found, rebuilding vectorstore")
            return True
        
        current_hash = self._get_data_hash()
        if current_hash is None:
            print("⚠️ Cannot get data hash, using existing vectorstore")
            return False
        
        if metadata.get("data_hash") != current_hash:
            print("📊 Data has changed, rebuilding vectorstore")
            return True
        
        if metadata.get("embedding_model") != EMBEDDING_MODEL:
            print("🔄 Embedding model changed, rebuilding vectorstore")
            return True
        
        print("✅ Existing vectorstore is up to date")
        return False
    
    def load_or_create_vectorstore(self, force_rebuild=False):
        """Load existing vectorstore or create new one if needed"""
        try:
            # Check if we need to rebuild
            if force_rebuild or self._should_rebuild_vectorstore():
                print("🔨 Creating new vectorstore...")
                return self._create_new_vectorstore()
            else:
                print("📂 Loading existing vectorstore...")
                return self._load_existing_vectorstore()
                
        except Exception as e:
            print(f"❌ Error in vectorstore management: {e}")
            # Fallback: try to create new vectorstore
            print("🔄 Attempting to create new vectorstore as fallback...")
            return self._create_new_vectorstore()
    
    def _load_existing_vectorstore(self):
        """Load existing vectorstore from disk"""
        try:
            self.vectorstore = FAISS.load_local(VECTORSTORE_PATH, self.embedding, allow_dangerous_deserialization=True)
            
            # Test the vectorstore
            test_results = self.vectorstore.similarity_search("test", k=1)
            if not test_results:
                raise ValueError("Vectorstore appears to be empty")
            
            print(f"✅ Loaded existing vectorstore with ~{len(test_results)} documents")
            return self.vectorstore
            
        except Exception as e:
            print(f"❌ Failed to load existing vectorstore: {e}")
            raise e
    
    def _create_new_vectorstore(self):
        """Create a new vectorstore from scratch"""
        try:
            print("📊 Loading and processing gym data...")
            processor = GymDataProcessor()
            data = processor.generate_exercise_descriptions()
            
            if len(data) == 0:
                raise ValueError("No data loaded for vectorstore creation")
            
            print(f"📝 Creating embeddings for {len(data)} exercises...")
            docs = [
                Document(
                    page_content=row['llm_entry'], 
                    metadata={
                        'Main_muscle': row['Main_muscle'],
                        'Exercise_Name': row.get('Exercise Name', 'Unknown'),
                        'Difficulty': row.get('Difficulty (1-5)', 'Unknown')
                    }
                )
                for _, row in data.iterrows()
            ]
            
            print("🧠 Computing embeddings (this may take a few minutes)...")
            self.vectorstore = FAISS.from_documents(docs, self.embedding)
            
            # Save to disk
            print("💾 Saving vectorstore to disk...")
            self._save_vectorstore()
            
            # Save metadata
            data_hash = self._get_data_hash()
            self._save_metadata(data_hash)
            
            print(f"✅ Created and saved new vectorstore with {len(docs)} documents")
            return self.vectorstore
            
        except Exception as e:
            print(f"❌ Failed to create vectorstore: {e}")
            raise e
    
    def _save_vectorstore(self):
        """Save vectorstore to disk"""
        if self.vectorstore:
            os.makedirs(VECTORSTORE_PATH, exist_ok=True)
            self.vectorstore.save_local(VECTORSTORE_PATH)
            print(f"💾 Vectorstore saved to {VECTORSTORE_PATH}")
    
    def get_info(self):
        """Get information about the current vectorstore"""
        if not self.vectorstore:
            return {"status": "not_loaded"}
        
        metadata = self._load_metadata()
        info = {
            "status": "loaded",
            "path": VECTORSTORE_PATH,
            "embedding_model": EMBEDDING_MODEL,
            "estimated_documents": self._get_vectorstore_size()
        }
        
        if metadata:
            info.update({
                "created_at": metadata.get("created_at"),
                "data_hash": metadata.get("data_hash")
            })
        
        return info
    
    def rebuild_vectorstore(self):
        """Force rebuild of the vectorstore"""
        print("🔄 Force rebuilding vectorstore...")
        return self.load_or_create_vectorstore(force_rebuild=True)
    
    def delete_vectorstore(self):
        """Delete the existing vectorstore files"""
        try:
            if os.path.exists(VECTORSTORE_PATH):
                import shutil
                shutil.rmtree(VECTORSTORE_PATH)
                print(f"🗑️ Deleted vectorstore at {VECTORSTORE_PATH}")
            else:
                print("📁 No vectorstore to delete")
        except Exception as e:
            print(f"❌ Error deleting vectorstore: {e}")