
import os
import sys
import subprocess
import time

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    packages = [
        "kagglehub",
        "pandas", 
        "seaborn",
        "matplotlib",
        "langchain",
        "faiss-cpu",
        "sentence-transformers",
        "rapidfuzz",
        "spacy",
        "streamlit",
        "plotly"
    ]
    
    for package in packages:
        try:
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ {package}")
        except:
            print(f"  ❌ Failed to install {package}")
    
    # Install spaCy model
    print("  Installing spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("  ✅ spaCy model")
    except:
        print("  ❌ Failed to install spaCy model")

def create_vectorstore():
    """Create the vectorstore (one-time operation)"""
    print("\n🔨 Creating vectorstore (this will take a few minutes)...")
    
    try:
        from vectorstore_manager import VectorStoreManager
        manager = VectorStoreManager()
        
        start_time = time.time()
        vectorstore = manager.load_or_create_vectorstore(force_rebuild=True)
        end_time = time.time()
        
        if vectorstore:
            print(f"✅ Vectorstore created in {end_time - start_time:.2f} seconds")
            
            # Test it
            test_results = vectorstore.similarity_search("chest exercises", k=2)
            print(f"✅ Test successful: found {len(test_results)} results")
            return True
        else:
            print("❌ Failed to create vectorstore")
            return False
            
    except Exception as e:
        print(f"❌ Error creating vectorstore: {e}")
        return False

def test_setup():
    """Test if everything is working"""
    print("\n🧪 Testing complete setup...")
    
    try:
        from exercise_recommender import ExerciseRecommender
        
        recommender = ExerciseRecommender()
        recommender.initialize()
        
        if not recommender.is_initialized():
            print("❌ Recommender failed to initialize")
            return False
        
        # Test search
        exercises = recommender.get_exercises("3 chest exercises")
        
        if exercises and not exercises[0].startswith("❌"):
            print(f"✅ Test search successful: found {len(exercises)} exercises")
            return True
        else:
            print(f"❌ Test search failed: {exercises}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("🏋️‍♂️ Gym Exercise Recommender - Easy Setup")
    print("=" * 50)
    print("This will set up everything you need to run the app.")
    print("This is a ONE-TIME setup process.\n")
    
    # Check if already set up
    if os.path.exists("./data/vectorstore/index.faiss"):
        print("✅ Vectorstore already exists!")
        choice = input("Do you want to rebuild it? (y/N): ").lower()
        if choice != 'y':
            print("Skipping setup. You can run: streamlit run streamlit_app.py")
            return
    
    steps = [
        ("Installing packages", install_requirements),
        ("Creating vectorstore", create_vectorstore), 
        ("Testing setup", test_setup)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        success = step_func()
        
        if not success and step_name == "Creating vectorstore":
            print("❌ Setup failed at vectorstore creation")
            print("This is usually due to:")
            print("• Internet connection issues (can't download dataset)")
            print("• Insufficient memory")
            print("• Missing dependencies")
            return
    
    print(f"\n{'='*50}")
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    print("Your gym exercise recommender is ready!")
    print("\nTo start the app, run:")
    print("  streamlit run streamlit_app.py")
    print("\nOr use the runner script:")
    print("  python run_app.py")
    print("\n💡 The vectorstore is now saved and won't be recreated unless you delete it.")

if __name__ == "__main__":
    main()