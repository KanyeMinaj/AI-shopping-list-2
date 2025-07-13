#!/usr/bin/env python3
"""
Test script to verify all components are working
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        import groq
        print("✅ Groq imported successfully")
        
        from youtube_transcript_api import YouTubeTranscriptApi
        print("✅ YouTube Transcript API imported successfully")
        
        from googleapiclient.discovery import build
        print("✅ Google API Client imported successfully")
        
        import spacy
        print("✅ spaCy imported successfully")
        
        import nltk
        print("✅ NLTK imported successfully")
        
        # Test spaCy model
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy English model loaded successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    try:
        from config import Config
        config = Config()
        print("✅ Configuration loaded successfully")
        
        if config.GROQ_API_KEY and config.GROQ_API_KEY != "your_groq_api_key_here":
            print("✅ Groq API key configured")
        else:
            print("⚠️  Groq API key not configured (required)")
            
        if config.YOUTUBE_API_KEY and config.YOUTUBE_API_KEY != "your_youtube_api_key_here":
            print("✅ YouTube API key configured")
        else:
            print("ℹ️  YouTube API key not configured (optional)")
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_components():
    """Test custom components"""
    try:
        from recipe_processor import RecipeProcessor
        processor = RecipeProcessor()
        print("✅ Recipe processor initialized successfully")
        
        from youtube_collector import YouTubeRecipeCollector
        collector = YouTubeRecipeCollector()
        print("✅ YouTube collector initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Component error: {e}")
        return False

def main():
    print("🧪 Testing AI Shopping List Generator...")
    print("=" * 50)
    
    # Test imports
    print("\n📦 Testing imports...")
    imports_ok = test_imports()
    
    # Test configuration
    print("\n⚙️  Testing configuration...")
    config_ok = test_configuration()
    
    # Test components
    print("\n🔧 Testing components...")
    components_ok = test_components()
    
    print("\n" + "=" * 50)
    if imports_ok and config_ok and components_ok:
        print("🎉 All tests passed! Your application is ready to run.")
        print("\n📋 Next steps:")
        print("1. Configure your API keys in the .env file")
        print("2. Run: streamlit run app.py")
        print("3. Start generating shopping lists!")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
