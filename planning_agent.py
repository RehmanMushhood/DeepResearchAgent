import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

class PlanningAgent:
    def __init__(self):
        """Initialize the Planning Agent with Gemini 1.5 Flash model"""
        load_dotenv()
        
        # Get API key
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 1.5 Flash - the free, fast model
        try:
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            print("Planning Agent initialized with Gemini 1.5 Flash")
        except Exception as e:
            print(f"Failed to initialize Gemini 1.5 Flash: {e}")
            raise
    
    def break_down_question(self, question):
        """
        Break down a complex research question into 3-5 specific research tasks
        
        Args:
            question (str): The research question to break down
            
        Returns:
            list: A list of 3-5 specific research tasks
        """
        print(f"\n Analyzing question: {question[:80]}...")
        
        # Create a well-structured prompt for better results
        prompt = f"""You are an expert research planner. Your task is to break down complex research questions into specific, actionable research tasks.

RESEARCH QUESTION:
{question}

YOUR TASK:
Break this down into exactly 5 specific research tasks that comprehensively cover all aspects of the question.

REQUIREMENTS:
1. Each task must be specific and actionable
2. Tasks should cover different aspects of the main question
3. Write one task per line
4. Do NOT use numbers, bullets, or any prefixes
5. Each task should be a complete sentence describing what to research
6. Tasks should be detailed enough to guide research but concise
7. Cover: current state, benefits, challenges, real examples, and future implications

EXAMPLE OUTPUT FORMAT:
Investigate current AI diagnostic tools being used in major hospitals worldwide
Analyze measurable benefits of AI in improving patient diagnosis accuracy rates
Examine documented concerns from healthcare professionals about AI reliability
Research specific case studies of AI implementation in radiology departments
Evaluate upcoming AI healthcare technologies and their potential impact

NOW PROVIDE 5 RESEARCH TASKS FOR THE GIVEN QUESTION:"""
        
        # Try to get good results with retries
        max_retries = 3
        best_tasks = []
        
        for attempt in range(max_retries):
            try:
                # Add delay between retries to avoid rate limiting
                if attempt > 0:
                    time.sleep(2)
                    print(f"Retry attempt {attempt + 1}...")
                
                # Generate response
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,  # Balanced creativity
                        max_output_tokens=500,  # Enough for 5 tasks
                    )
                )
                
                if response and response.text:
                    # Parse the response into tasks
                    tasks = self._parse_tasks(response.text)
                    
                    # Validate tasks
                    if len(tasks) >= 3:
                        # Success! Return up to 5 tasks
                        print(f"Generated {len(tasks)} research tasks")
                        return tasks[:5]
                    elif len(tasks) > len(best_tasks):
                        # Keep the best attempt so far
                        best_tasks = tasks
                        
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"Rate limit hit, waiting 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Attempt {attempt + 1} error: {error_msg[:80]}")
        
        # If we have some tasks from attempts, use them
        if best_tasks:
            print(f"Using best attempt with {len(best_tasks)} tasks")
            return best_tasks
        
        # Last resort: Create intelligent fallback tasks based on the question
        print("Using intelligent fallback task generation")
        return self._generate_fallback_tasks(question)
    
    def _parse_tasks(self, text):
        """
        Parse the model's response into a clean list of tasks
        
        Args:
            text (str): Raw text from the model
            
        Returns:
            list: Cleaned list of research tasks
        """
        tasks = []
        lines = text.strip().split('\n')
        
        for line in lines:
            # Clean up the line
            task = line.strip()
            
            # Remove common prefixes (numbers, bullets, etc.)
            task = task.lstrip('0123456789.-•*†‡§¶#) ').strip()
            
            # Remove quotes if present
            task = task.strip('"\'')
            
            # Skip empty lines or very short lines
            if len(task) < 20:
                continue
            
            # Skip lines that look like headers or meta text
            skip_phrases = ['task:', 'research:', 'example:', 'note:', 'requirement:']
            if any(phrase in task.lower()[:15] for phrase in skip_phrases):
                continue
            
            # Add valid tasks
            if task and not task.endswith(':'):
                tasks.append(task)
        
        return tasks
    
    def _generate_fallback_tasks(self, question):
        """
        Generate intelligent fallback tasks when API calls fail
        
        Args:
            question (str): The original research question
            
        Returns:
            list: A list of 5 research tasks
        """
        # Extract key terms from the question for more relevant fallbacks
        question_lower = question.lower()
        
        # Determine the focus area
        if "ai" in question_lower or "artificial intelligence" in question_lower:
            domain = "AI technology"
        elif "health" in question_lower or "medical" in question_lower:
            domain = "healthcare"
        elif "education" in question_lower:
            domain = "education"
        elif "business" in question_lower or "economic" in question_lower:
            domain = "business"
        elif "environment" in question_lower or "climate" in question_lower:
            domain = "environmental"
        else:
            domain = "this topic"
        
        # Generate contextual fallback tasks
        tasks = [
            f"Investigate the current state and latest developments in {domain} related to {question[:40]}",
            f"Analyze the key benefits and positive outcomes of {question[:50]}",
            f"Examine the main challenges, risks, and concerns regarding {question[:40]}",
            f"Research real-world implementations and case studies of {question[:40]}",
            f"Evaluate future trends and potential implications of {question[:40]}"
        ]
        
        return tasks
    
    def validate_connection(self):
        """
        Test if the API connection is working
        
        Returns:
            bool: True if connection is working, False otherwise
        """
        try:
            response = self.model.generate_content("Say 'OK' in one word")
            return response and response.text
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

# Testing function (optional - can be removed in production)
def test_planning_agent():
    """Test the planning agent with a sample question"""
    print("="*60)
    print("TESTING PLANNING AGENT")
    print("="*60)
    
    try:
        agent = PlanningAgent()
        
        # Test connection
        if agent.validate_connection():
            print("API connection verified")
        
        # Test with a sample question
        test_question = "How has artificial intelligence changed healthcare from 2020 to 2024?"
        tasks = agent.break_down_question(test_question)
        
        print("\n Generated Research Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task}")
        
        return True
        
    except Exception as e:
        print(f"\n Test failed: {e}")
        return False

# Run test if this file is executed directly
if __name__ == "__main__":
    test_planning_agent()