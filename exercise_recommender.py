
"""Main recommendation engine with improved error handling"""
import os
import traceback
from vectorstore_manager import VectorStoreManager
from query_processor import QueryProcessor

class ExerciseRecommender:
    def __init__(self):
        self.vectorstore_manager = VectorStoreManager()
        self.query_processor = QueryProcessor()
        self.vectorstore = None
        self._initialized = False
    
    def initialize(self):
        """Initialize the recommender system with proper error handling"""
        try:
            print("Initializing Exercise Recommender...")
            
            # Initialize vectorstore
            print("Loading vectorstore...")
            self.vectorstore = self.vectorstore_manager.load_or_create_vectorstore()
            
            if self.vectorstore is None:
                raise ValueError("Failed to create or load vectorstore")
            
            # Test the vectorstore with a simple query
            print("Testing vectorstore...")
            test_results = self.vectorstore.similarity_search("test", k=1)
            
            if not test_results:
                raise ValueError("Vectorstore is empty or not working properly")
            
            self._initialized = True
            print("Exercise recommender initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing recommender: {str(e)}")
            print("Full traceback:")
            traceback.print_exc()
            self.vectorstore = None
            self._initialized = False
            raise e
    
    def is_initialized(self):
        """Check if the recommender is properly initialized"""
        return self._initialized and self.vectorstore is not None
    
    def get_exercises(self, query: str):
        """Get exercise recommendations based on user query"""
        if not self.is_initialized():
            return ["❌ Recommender not properly initialized. Please check the setup."]
        
        try:
            num_exercises, muscles = self.query_processor.parse_query(query)
            
            if not muscles:
                return ["❌ No valid muscles found. Try muscle names like: Chest, Back, Shoulder, Arms, Legs, etc."]
            
            per_muscle = max(1, num_exercises // len(muscles))
            all_results = []
            seen = set()
            
            # Get exercises for each muscle group
            for muscle in muscles:
                try:
                    results = self.vectorstore.similarity_search(f"exercises for {muscle}", k=per_muscle * 2)
                    count = 0
                    for res in results:
                        if res.page_content not in seen and count < per_muscle:
                            all_results.append(res)
                            seen.add(res.page_content)
                            count += 1
                except Exception as e:
                    print(f"Error searching for muscle {muscle}: {e}")
                    continue
            
            # Fill remaining slots if needed
            if len(all_results) < num_exercises:
                try:
                    extra_needed = num_exercises - len(all_results)
                    fallback = self.vectorstore.similarity_search(query, k=extra_needed * 2)
                    for res in fallback:
                        if res.page_content not in seen and len(all_results) < num_exercises:
                            all_results.append(res)
                            seen.add(res.page_content)
                except Exception as e:
                    print(f"Error in fallback search: {e}")
            
            if not all_results:
                return ["❌ No exercises found. Try different muscle groups or check your spelling."]
            
            return [doc.page_content for doc in all_results[:num_exercises]]
            
        except Exception as e:
            print(f"Error in get_exercises: {str(e)}")
            traceback.print_exc()
            return [f"❌ Error searching for exercises: {str(e)}"]
    
    def get_status(self):
        """Get detailed status information about the recommender"""
        status = {
            'initialized': self._initialized,
            'vectorstore_loaded': self.vectorstore is not None,
            'query_processor_ready': self.query_processor is not None
        }
        
        if self.vectorstore:
            try:
                # Try to get the number of documents
                test_search = self.vectorstore.similarity_search("test", k=1)
                status['vectorstore_working'] = len(test_search) > 0
            except:
                status['vectorstore_working'] = False
        else:
            status['vectorstore_working'] = False
        
        return status