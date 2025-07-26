

import os
import sys
import traceback

def check_imports():
    """Check if all required modules can be imported"""
    print("🔍 Checking imports...")
    
    required_modules = [
        'kagglehub',
        'pandas', 
        'seaborn',
        'matplotlib',
        'langchain',
        'faiss',
        'sentence_transformers',
        'rapidfuzz',
        'spacy',
        'streamlit',
        'plotly'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'faiss':
                import faiss
            else:
                __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {missing_modules}")
        print("Install with: pip install " + " ".join(missing_modules))
        return False
    
    print("✅ All imports successful!")
    return True

def check_spacy_model():
    """Check if spaCy English model is installed"""
    print("\n🔍 Checking spaCy model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy English model loaded successfully!")
        return True
    except OSError:
        print("❌ spaCy English model not found")
        print("Install with: python -m spacy download en_core_web_sm")
        return False
    except Exception as e:
        print(f"❌ Error loading spaCy model: {e}")
        return False

def check_custom_modules():
    """Check if custom modules can be imported"""
    print("\n🔍 Checking custom modules...")
    
    custom_modules = [
        'config',
        'data_processor', 
        'vectorstore_manager',
        'query_processor',
        'exercise_recommender',
        'visualizations'
    ]
    
    missing_custom = []
    for module in custom_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}.py")
        except ImportError as e:
            print(f"  ❌ {module}.py - {e}")
            missing_custom.append(module)
        except Exception as e:
            print(f"  ⚠️ {module}.py - Error: {e}")
    
    if missing_custom:
        print(f"\n❌ Missing custom modules: {missing_custom}")
        print("Make sure all the refactored Python files are in the same directory")
        return False
    
    print("✅ All custom modules found!")
    return True

def test_data_loading():
    """Test if data can be loaded"""
    print("\n🔍 Testing data loading...")
    
    try:
        from data_processor import GymDataProcessor
        processor = GymDataProcessor()
        
        print("  📥 Downloading dataset...")
        data = processor.download_and_load_data()
        print(f"  ✅ Dataset loaded: {len(data)} rows")
        
        print("  🧹 Cleaning data...")
        cleaned = processor.clean_data()
        print(f"  ✅ Data cleaned: {len(cleaned)} rows")
        
        print("  📝 Generating descriptions...")
        with_descriptions = processor.generate_exercise_descriptions()
        print(f"  ✅ Descriptions generated: {len(with_descriptions)} rows")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in data loading: {e}")
        traceback.print_exc()
        return False

def test_vectorstore():
    """Test vectorstore creation and loading"""
    print("\n🔍 Testing vectorstore...")
    
    try:
        from vectorstore_manager import VectorStoreManager
        manager = VectorStoreManager()
        
        print("  🔄 Loading or creating vectorstore...")
        vectorstore = manager.load_or_create_vectorstore()
        
        if vectorstore is None:
            print("  ❌ Vectorstore is None")
            return False
            
        print("  🔍 Testing similarity search...")
        results = vectorstore.similarity_search("chest exercises", k=2)
        print(f"  ✅ Vectorstore working: found {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in vectorstore: {e}")
        traceback.print_exc()
        return False

def test_recommender():
    """Test the full recommender system"""
    print("\n🔍 Testing recommender system...")
    
    try:
        from exercise_recommender import ExerciseRecommender
        recommender = ExerciseRecommender()
        
        print("  🔧 Initializing recommender...")
        recommender.initialize()
        
        if recommender.vectorstore is None:
            print("  ❌ Recommender vectorstore is None")
            return False
            
        print("  🔍 Testing exercise search...")
        exercises = recommender.get_exercises("5 chest exercises")
        
        if not exercises or exercises[0].startswith("No valid muscles"):
            print(f"  ❌ No exercises found: {exercises}")
            return False
            
        print(f"  ✅ Recommender working: found {len(exercises)} exercises")
        return True
        
    except Exception as e:
        print(f"  ❌ Error in recommender: {e}")
        traceback.print_exc()
        return False

def main():
    print("🏋️‍♂️ Gym Exercise Recommender - Setup Diagnostic")
    print("=" * 50)
    
    checks = [
        ("Import Check", check_imports),
        ("spaCy Model Check", check_spacy_model), 
        ("Custom Modules Check", check_custom_modules),
        ("Data Loading Test", test_data_loading),
        ("Vectorstore Test", test_vectorstore),
        ("Recommender Test", test_recommender)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ Unexpected error in {check_name}: {e}")
            results[check_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 DIAGNOSTIC SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, passed_check in results.items():
        status = "✅ PASS" if passed_check else "❌ FAIL"
        print(f"{check_name:.<30} {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your setup is ready.")
        print("You can now run: streamlit run streamlit_app.py")
    else:
        print("⚠️ Some checks failed. Please fix the issues above before running the app.")
        
        # Common solutions
        print("\n💡 Common Solutions:")
        if not results.get("Import Check", True):
            print("• Install missing packages: pip install -r requirements_streamlit.txt")
        if not results.get("spaCy Model Check", True):
            print("• Install spaCy model: python -m spacy download en_core_web_sm")
        if not results.get("Custom Modules Check", True):
            print("• Make sure all .py files are in the same directory")
        if not results.get("Data Loading Test", True):
            print("• Check your internet connection for dataset download")
        if not results.get("Vectorstore Test", True):
            print("• Delete vectorstore folder and let it recreate")

if __name__ == "__main__":
    main()