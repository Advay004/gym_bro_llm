def main():
    print("🏋️‍♂️ Gym Exercise Recommender - Vectorstore Setup")
    print("=" * 50)
    
    try:
        from vectorstore_manager import VectorStoreManager
        
        manager = VectorStoreManager()
        
        print("🔍 Checking current status...")
        info = manager.get_info()
        print(f"Current status: {info}")
        
        if info["status"] == "loaded":
            choice = input("\n📁 Vectorstore already exists. Rebuild? (y/N): ").lower()
            if choice != 'y':
                print("✅ Using existing vectorstore")
                return
        
        print("\n🔨 Creating vectorstore...")
        vectorstore = manager.load_or_create_vectorstore(force_rebuild=True)
        
        if vectorstore:
            print("\n✅ Vectorstore setup complete!")
            
            # Test the vectorstore
            print("\n🧪 Testing vectorstore...")
            test_results = vectorstore.similarity_search("chest exercises", k=3)
            print(f"Test search returned {len(test_results)} results")
            
            if test_results:
                print("Sample result:", test_results[0].page_content[:100] + "...")
            
            print("\n🎉 Setup successful! You can now run the Streamlit app.")
            
        else:
            print("❌ Failed to create vectorstore")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()