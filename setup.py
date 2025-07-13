#!/usr/bin/env python3
"""
Setup script for the AI Shopping List Generator
"""
import subprocess
import sys
import os

def install_spacy_model():
    """Install the spaCy English model"""
    try:
        print("Installing spaCy English model...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        print("✅ spaCy model installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install spaCy model: {e}")
        print("You can install it manually with: python -m spacy download en_core_web_sm")

def create_env_file():
    """Create a sample .env file"""
    env_content = """# AI Shopping List Generator Environment Variables
# Get your Groq API key from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Get your YouTube API key from: https://console.cloud.google.com/
# This is optional but enables enhanced recipe features
YOUTUBE_API_KEY=your_youtube_api_key_here
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("📝 Please edit .env file and add your API keys")
    else:
        print("ℹ️  .env file already exists")

def main():
    print("🚀 Setting up AI Shopping List Generator...")
    
    # Install spaCy model
    install_spacy_model()
    
    # Create environment file
    create_env_file()
    
    # Create data directories
    os.makedirs("data/recipes", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Run: streamlit run app.py")
    print("3. Start generating shopping lists!")

if __name__ == "__main__":
    main()
