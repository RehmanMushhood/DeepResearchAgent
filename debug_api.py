# debug_api.py - Comprehensive API Key Debugger
import os
import sys
from pathlib import Path

print("="*70)
print("COMPREHENSIVE GEMINI API KEY DEBUGGER")
print("="*70)

# Step 1: Check Python environment
print("\n PYTHON ENVIRONMENT")
print("-"*40)
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Step 2: Check .env file
print("\n CHECKING .ENV FILE")
print("-"*40)

env_path = Path(".env")
if env_path.exists():
    print(f".env file found at: {env_path.absolute()}")
    with open(".env", "r") as f:
        content = f.read()
    print(f"File size: {len(content)} bytes")
    
    # Check for common issues
    lines = content.strip().split('\n')
    for line in lines:
        if 'GEMINI_API_KEY' in line:
            print(f"Found line: {line[:30]}...")
            
            # Check for common problems
            if '"' in line or "'" in line:
                print("ERROR: Remove quotes from your API key!")
            if ' = ' in line:
                print("ERROR: Remove spaces around the = sign!")
            if line.strip() == "GEMINI_API_KEY=":
                print("ERROR: No API key value found!")
            if "your-key-here" in line or "your-actual-key" in line:
                print("ERROR: You haven't replaced the placeholder text!")
else:
    print("No .env file found!")
    print("Creating .env file...")

# Step 3: Load and check the key
print("\n LOADING API KEY")
print("-"*40)

# Try multiple loading methods
methods = []

# Method 1: dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
    key1 = os.getenv("GEMINI_API_KEY")
    methods.append(("dotenv", key1))
    print(f"Method 1 (dotenv): {key1[:20] if key1 else 'None'}...")
except Exception as e:
    print(f"Method 1 failed: {e}")

# Method 2: Direct file read
try:
    if env_path.exists():
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY"):
                    key2 = line.split("=", 1)[1].strip()
                    methods.append(("direct", key2))
                    print(f"Method 2 (direct): {key2[:20] if key2 else 'None'}...")
except Exception as e:
    print(f"Method 2 failed: {e}")

# Method 3: Manual environment variable
key3 = os.environ.get("GEMINI_API_KEY")
if key3:
    methods.append(("environ", key3))
    print(f"Method 3 (environ): {key3[:20]}...")

# Step 4: Analyze the key
print("\n API KEY ANALYSIS")
print("-"*40)

api_key = None
for method, key in methods:
    if key:
        api_key = key
        break

if not api_key:
    print(" NO API KEY FOUND!")
    print("\n SOLUTION:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Click 'Create API Key' or 'Get API Key'")
    print("3. Copy the ENTIRE key")
    print("4. Run this command:")
    print('   echo "GEMINI_API_KEY=YOUR_KEY_HERE" > .env')
else:
    # Analyze the key
    print(f"API Key found: {api_key[:15]}...{api_key[-5:]}")
    print(f"Key length: {len(api_key)} characters")
    
    # Check format
    issues = []
    if not api_key.startswith("AIzaSy"):
        issues.append("Doesn't start with 'AIzaSy' - might be wrong key type")
    if len(api_key) < 39:
        issues.append(f"Too short ({len(api_key)} chars) - should be 39+ chars")
    if len(api_key) > 50:
        issues.append(f"Too long ({len(api_key)} chars) - might have extra characters")
    if " " in api_key:
        issues.append("Contains spaces - remove all spaces")
    if '"' in api_key or "'" in api_key:
        issues.append("Contains quotes - remove all quotes")
    
    if issues:
        print("\n KEY FORMAT ISSUES:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✓ Key format looks correct")

# Step 5: Test the API
print("\n TESTING API CONNECTION")
print("-"*40)

if api_key and api_key.startswith("AIzaSy"):
    # Clean the key
    clean_key = api_key.strip().replace('"', '').replace("'", '')
    
    print(f"Testing with key: {clean_key[:20]}...")
    
    try:
        import google.generativeai as genai
        
        # Configure with clean key
        genai.configure(api_key=clean_key)
        
        # Try different models
        models_to_try = ['gemini-pro', 'gemini-1.5-flash', 'gemini-1.5-pro']
        
        for model_name in models_to_try:
            try:
                print(f"\nTrying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Reply with: SUCCESS")
                print(f"{model_name} WORKS! Response: {response.text[:50]}")
                
                # Save working configuration
                print("\n WORKING CONFIGURATION FOUND!")
                print("-"*40)
                print("Your .env file should contain EXACTLY this line:")
                print(f"GEMINI_API_KEY={clean_key}")
                
                # Offer to fix it
                fix = input("\n Do you want me to fix your .env file? (y/n): ")
                if fix.lower() == 'y':
                    with open('.env', 'w') as f:
                        f.write(f"GEMINI_API_KEY={clean_key}\n")
                    print(".env file fixed!")
                
                break
                
            except Exception as e:
                error_str = str(e)
                if "API_KEY_INVALID" in error_str:
                    print(f"{model_name}: Invalid API key")
                elif "not found" in error_str.lower():
                    print(f"{model_name}: Model not available")
                else:
                    print(f"{model_name}: {error_str[:100]}")
        
    except Exception as e:
        print(f"API test failed: {e}")
        
        if "API_KEY_INVALID" in str(e):
            print("\n YOUR API KEY IS INVALID!")
            print("\n COMPLETE SOLUTION:")
            print("1. Go to: https://makersuite.google.com/app/apikey")
            print("2. Sign in with your Google account")
            print("3. Click 'Get API Key' button")
            print("4. If you see existing keys, create a NEW one")
            print("5. Copy the ENTIRE key (starts with AIzaSy)")
            print("6. Paste it when running this script again")

# Step 6: Manual key input option
print("\n MANUAL KEY INPUT")
print("-"*40)
print("If all above failed, let's try manually entering a new key.")
manual = input("Do you want to enter a new API key? (y/n): ")

if manual.lower() == 'y':
    print("\nGet your key from: https://makersuite.google.com/app/apikey")
    new_key = input("Paste your COMPLETE API key here: ").strip()
    
    # Clean it
    new_key = new_key.replace('"', '').replace("'", '').replace(' ', '')
    
    if new_key.startswith("AIzaSy") and len(new_key) >= 39:
        print(f"\nTesting new key: {new_key[:20]}...")
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=new_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say hello")
            
            print("NEW KEY WORKS!")
            
            # Save it
            with open('.env', 'w') as f:
                f.write(f"GEMINI_API_KEY={new_key}\n")
            print("Saved to .env file!")
            print("\n You can now run your research system!")
            
        except Exception as e:
            print(f"New key failed: {e}")
            print("\nThis key is not valid. Please get a new one from Google.")
    else:
        print("Invalid key format")

print("\n" + "="*70)
print("DEBUGGING COMPLETE")
print("="*70)