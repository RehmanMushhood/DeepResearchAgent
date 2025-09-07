import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")

print("="*60)
print("GEMINI API KEY DIAGNOSTIC")
print("="*60)

# Check if key exists
if not api_key:
    print("No API key found in .env file!")
    print("\n Fix: Create .env file with:")
    print("GEMINI_API_KEY=your-actual-key-here")
else:
    # Show key info (hidden for security)
    print(f"API Key found: {api_key[:20]}...")
    print(f"Key length: {len(api_key)} characters")
    
    # Check key format
    if api_key.startswith("AIzaSy"):
        print("Key format looks correct (starts with AIzaSy)")
    else:
        print("Key format incorrect - should start with 'AIzaSy'")
    
    # Test the key
    print("\n Testing API connection...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say 'Hello World' in exactly 2 words")
        print("API KEY IS VALID AND WORKING!")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"API KEY FAILED: {e}")
        
        if "API_KEY_INVALID" in str(e):
            print("\n SOLUTIONS:")
            print("1. Your key is invalid or expired")
            print("2. Get a new key at: https://makersuite.google.com/app/apikey")
            print("3. Make sure you're using the correct Google account")
            print("4. Check if the API is enabled for your project")

print("\n" + "="*60)