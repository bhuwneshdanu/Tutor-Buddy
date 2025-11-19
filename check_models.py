import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ No API Key found in .env file!")
else:
    print(f"✅ API Key found: {api_key[:5]}... (hidden)")
    
    try:
        genai.configure(api_key=api_key)
        print("\n🔍 Scanning for available models...")
        
        found_any = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name}")
                found_any = True
        
        if not found_any:
            print("❌ Connected, but no text-generation models found.")
            print("Please verify you enabled 'Generative Language API' in Google Cloud Console.")
            
    except Exception as e:
        print(f"\n❌ Error connecting to Google: {e}")