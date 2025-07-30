import os

def main():
    # Check if already set up
    if os.path.exists("./data/vectorstore/index.faiss"):
        print("✅ Already set up! Running Streamlit app...")
        os.system("streamlit run streamlit_app.py")
    else:
        print("🔧 First time setup required...")
        import easy_setup
        easy_setup.main()
        
        # After setup, run the app
        if os.path.exists("./data/vectorstore/index.faiss"):
            print("\n🚀 Starting Streamlit app...")
            os.system("streamlit run streamlit_app.py")
        else:
            print("❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()