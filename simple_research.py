# simple_research.py - Simplified Research System
import os
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ No API key found!")
        print("Run 'python fix_api.py' first to set up your API key.")
        return
    
    # Configure API
    genai.configure(api_key=api_key)
    
    print("="*60)
    print("SIMPLE RESEARCH SYSTEM")
    print("="*60)
    
    # Get user query
    query = input("\nWhat do you want to research?\n> ")
    
    if not query:
        query = "What is the current state of AI in medicine?"
        print(f"Using default query: {query}")
    
    print("\n🔍 Researching...")
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Simple research
        prompt = f"""
        Research this topic: {query}
        
        Provide a detailed, comprehensive response with:
        1. Current state and developments
        2. Key benefits and applications
        3. Challenges and concerns
        4. Future outlook
        
        Be thorough and specific.
        """
        
        response = model.generate_content(prompt)
        
        print("\n" + "="*60)
        print("RESEARCH RESULTS")
        print("="*60)
        print(response.text)
        
        # Save to file
        filename = "research_output.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Research: {query}\n\n")
            f.write(response.text)
        
        print(f"\n✅ Saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")