# deep_research_system.py - Interactive Version for User Input
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import time
import json
from pathlib import Path

# Import all agents (assuming you have these files)
from planning_agent import PlanningAgent
from research_agents import FactFinder, SourceChecker
from synthesis_agent import SynthesisAgent
from report_writer import ReportWriter

class DeepResearchSystem:
    def __init__(self):
        load_dotenv()
        
        # Clear screen for better presentation
        self.clear_screen()
        
        print("\n" + "="*70)
        print("DEEP RESEARCH SYSTEM - INTERACTIVE EDITION")
        print("Powered by Google Gemini AI")
        print("="*70)
        
        # Check for Gemini API key
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("\n ERROR: GEMINI_API_KEY not found!")
            print("\n Setup Instructions:")
            print("1. Create a .env file in your project directory")
            print("2. Add this line: GEMINI_API_KEY=your-actual-key-here")
            print("3. Get your free key at: https://makersuite.google.com/app/apikey")
            input("\nPress Enter to exit...")
            sys.exit(1)
        
        print(f"\n✓ Gemini API Key loaded: {self.api_key[:15]}...")
        
        # Initialize session
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.research_history = []
        self.reports_dir = Path("research_reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Initialize all agents
        print("\n🔧 Initializing AI Agents...")
        try:
            print("   • Loading Planning Agent...")
            self.planning_agent = PlanningAgent()
            
            print("   • Loading Research Agents...")
            self.fact_finder = FactFinder()
            self.source_checker = SourceChecker()
            
            print("   • Loading Synthesis Agent...")
            self.synthesis_agent = SynthesisAgent()
            
            print("   • Loading Report Writer...")
            self.report_writer = ReportWriter()
            
            print("\n All agents initialized successfully!")
            time.sleep(1)
            
        except Exception as e:
            print(f"\n Initialization failed: {e}")
            print("\n Troubleshooting:")
            print("1. Check your internet connection")
            print("2. Verify your API key is valid")
            print("3. Run: pip install --upgrade google-generativeai")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display the main menu"""
        self.clear_screen()
        print("\n" + "="*70)
        print("DEEP RESEARCH SYSTEM - MAIN MENU")
        print("="*70)
        print("\n [1] Start New Research")
        print("  [2] View Research History")
        print("  [3] Quick Research (Predefined Topics)")
        print("  [4] Settings & Configuration")
        print("  [5] Help & Examples")
        print("  [6] Exit")
        print("\n" + "="*70)
    
    def get_user_query(self):
        """Get research query from user with guidance"""
        self.clear_screen()
        print("\n" + "="*70)
        print("NEW RESEARCH QUERY")
        print("="*70)
        
        print("\n Tips for effective research queries:")
        print("  • Be specific and detailed")
        print("  • Include timeframes if relevant (e.g., '2020-2024')")
        print("  • Mention specific aspects you want to explore")
        print("  • Ask complex, multi-faceted questions for best results")
        
        print("\n Example queries:")
        print("  • How has AI transformed education, including benefits and challenges?")
        print("  • Compare renewable energy sources: solar, wind, and hydroelectric")
        print("  • What are the psychological effects of social media on teenagers?")
        
        print("\n" + "-"*70)
        query = input("\n Enter your research question:\n> ").strip()
        
        if not query:
            print("\n No query entered. Returning to menu...")
            time.sleep(2)
            return None
        
        # Confirm the query
        print(f"\n Your research question:")
        print(f"   {query}")
        confirm = input("\n Proceed with this query? (y/n): ").strip().lower()
        
        if confirm == 'y':
            return query
        else:
            return None
    
    def show_quick_research_menu(self):
        """Show predefined research topics"""
        self.clear_screen()
        print("\n" + "="*70)
        print("QUICK RESEARCH - PREDEFINED TOPICS")
        print("="*70)
        
        topics = [
            "How has artificial intelligence changed healthcare from 2020 to 2024?",
            "Environmental and economic impacts of electric vehicles vs traditional cars",
            "The rise of remote work: benefits, challenges, and future implications",
            "Impact of social media on mental health and society",
            "Cryptocurrency and blockchain: current state and future potential",
            "Climate change: latest scientific findings and mitigation strategies",
            "Gene editing and CRISPR: medical breakthroughs and ethical concerns",
            "The metaverse: hype vs reality in business and social applications",
            "Quantum computing: current capabilities and future applications",
            "Space exploration: recent achievements and upcoming missions"
        ]
        
        print("\nSelect a topic to research:\n")
        for i, topic in enumerate(topics, 1):
            print(f"  [{i}] {topic[:60]}...")
        
        print(f"\n  [0] ← Back to Main Menu")
        print("\n" + "="*70)
        
        try:
            choice = int(input("\n Select topic (0-10): "))
            if 0 < choice <= len(topics):
                return topics[choice - 1]
            else:
                return None
        except:
            return None
    
    def show_research_history(self):
        """Display research history"""
        self.clear_screen()
        print("\n" + "="*70)
        print("RESEARCH HISTORY")
        print("="*70)
        
        if not self.research_history:
            print("\n  No research conducted yet in this session.")
        else:
            print(f"\n Session: {self.session_id}")
            print(f" Total researches: {len(self.research_history)}")
            print("\n" + "-"*70)
            
            for i, item in enumerate(self.research_history, 1):
                print(f"\n [{i}] {item['timestamp']}")
                print(f"Query: {item['query'][:60]}...")
                print(f"Report: {item['filename']}")
                print(f"Duration: {item['duration']:.1f} seconds")
        
        input("\n\nPress Enter to continue...")
    
    def show_settings(self):
        """Show settings and configuration"""
        self.clear_screen()
        print("\n" + "="*70)
        print(" SETTINGS & CONFIGURATION")
        print("="*70)
        
        print(f"\n Reports Directory: {self.reports_dir.absolute()}")
        print(f"API Key Status: {'Configured' if self.api_key else 'Not configured'}")
        print(f"Session ID: {self.session_id}")
        print(f"Reports Generated: {len(self.research_history)}")
        
        print("\n" + "-"*70)
        print("\n  [1] Change reports directory")
        print("  [2] Test API connection")
        print("  [3] Clear research history")
        print("  [0] ← Back to Main Menu")
        
        choice = input("\n Select option: ").strip()
        
        if choice == '2':
            self.test_api_connection()
        elif choice == '3':
            self.research_history.clear()
            print("\n Research history cleared!")
            time.sleep(2)
    
    def test_api_connection(self):
        """Test the API connection"""
        print("\n Testing API connection...")
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say 'API connection successful' in 5 words")
            print(f"Connection successful!")
            print(f"   Response: {response.text[:100]}")
        except Exception as e:
            print(f"Connection failed: {e}")
        
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """Show help and examples"""
        self.clear_screen()
        print("\n" + "="*70)
        print("HELP & USAGE GUIDE")
        print("="*70)
        
        print("\n HOW TO USE THIS SYSTEM:")
        print("\n1. Choose 'Start New Research' from the main menu")
        print("2. Enter a detailed research question")
        print("3. The system will:")
        print("   • Break down your question into research tasks")
        print("   • Conduct detailed research on each task")
        print("   • Synthesize findings into a comprehensive analysis")
        print("   • Generate a professional research report")
        print("4. Reports are saved as Markdown files in the reports directory")
        
        print("\n TIPS FOR BEST RESULTS:")
        print("• Ask complex, multi-faceted questions")
        print("• Include specific timeframes or contexts")
        print("• Be clear about what aspects interest you")
        print("• Questions comparing multiple things work well")
        
        print("\n EXAMPLE QUERIES:")
        print("• 'How has remote work changed corporate culture and productivity?'")
        print("• 'Compare the effectiveness of different COVID-19 vaccines'")
        print("• 'What are the pros and cons of nuclear energy in 2024?'")
        
        input("\n\nPress Enter to continue...")
    
    def run_research(self, query):
        """Execute the research process with progress indicators"""
        start_time = datetime.now()
        
        self.clear_screen()
        print("\n" + "="*70)
        print("RESEARCH IN PROGRESS")
        print("="*70)
        print(f"\n Query: {query}")
        print(f"🕐 Started: {start_time.strftime('%H:%M:%S')}")
        print("\n" + "="*70)
        
        try:
            # Phase 1: Planning
            print("\n PHASE 1/4: RESEARCH PLANNING")
            print("-"*40)
            print("Breaking down your question into research tasks...")
            
            tasks = self.planning_agent.break_down_question(query)
            
            if not tasks or len(tasks) < 2:
                print("Failed to generate research tasks")
                input("\nPress Enter to continue...")
                return None
            
            print(f"\n Generated {len(tasks)} research tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"   {i}. {task[:80]}...")
                time.sleep(0.5)  # Visual effect
            
            # Phase 2: Research
            print("\n🔍 PHASE 2/4: CONDUCTING RESEARCH")
            print("-"*40)
            
            all_findings = []
            for i, task in enumerate(tasks, 1):
                print(f"\n[{i}/{len(tasks)}] Researching: {task[:60]}...")
                
                # Progress bar
                self.show_progress_bar(i, len(tasks))
                
                # Add delay to avoid rate limiting
                if i > 1:
                    time.sleep(2)
                
                findings = self.fact_finder.run(task)
                
                if findings and len(findings) > 100:
                    all_findings.append(findings)
                    quality = self.source_checker.run(findings)
                    print(f"   ✓ Collected {len(findings)} chars | Quality: {quality[:30]}...")
                    self.report_writer.add_citation(f"{task[:100]}")
            
            if not all_findings:
                print("\nNo substantial findings collected")
                input("\nPress Enter to continue...")
                return None
            
            # Phase 3: Synthesis
            print("\nPHASE 3/4: SYNTHESIZING FINDINGS")
            print("-"*40)
            print("Analyzing and combining research findings...")
            self.show_progress_bar(1, 1)
            
            time.sleep(2)
            synthesized_content = self.synthesis_agent.synthesize_research(all_findings)
            
            if not synthesized_content or len(synthesized_content) < 200:
                print("Synthesis failed")
                input("\nPress Enter to continue...")
                return None
            
            print(f"Synthesized {len(synthesized_content)} characters of analysis")
            
            # Phase 4: Report Writing
            print("\n PHASE 4/4: GENERATING REPORT")
            print("-"*40)
            print("Creating comprehensive research report...")
            self.show_progress_bar(1, 1)
            
            time.sleep(2)
            final_report = self.report_writer.write_report(synthesized_content, query)
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"research_{timestamp}.md"
            filepath = self.reports_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_report)
            
            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Add to history
            self.research_history.append({
                'timestamp': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'query': query,
                'filename': filename,
                'duration': duration,
                'path': str(filepath)
            })
            
            # Show completion
            print("\n" + "="*70)
            print("RESEARCH COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"\n Summary:")
            print(f"   • Duration: {duration:.1f} seconds")
            print(f"   • Report size: {len(final_report)} characters")
            print(f"   • Tasks completed: {len(all_findings)}")
            print(f"   • Report saved: {filepath}")
            
            # Offer to open report
            print("\n" + "-"*70)
            open_report = input("\n Open report now? (y/n): ").strip().lower()
            
            if open_report == 'y':
                self.display_report(final_report)
            
            return filepath
            
        except Exception as e:
            print(f"\n Research failed: {e}")
            input("\nPress Enter to continue...")
            return None
    
    def show_progress_bar(self, current, total, width=40):
        """Display a progress bar"""
        progress = current / total
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        print(f"Progress: [{bar}] {progress*100:.0f}%")
    
    def display_report(self, report):
        """Display the report with pagination"""
        self.clear_screen()
        lines = report.split('\n')
        page_size = 20
        
        for i in range(0, len(lines), page_size):
            self.clear_screen()
            print("\n" + "="*70)
            print("RESEARCH REPORT")
            print("="*70)
            print()
            
            # Display page
            for line in lines[i:i+page_size]:
                print(line)
            
            if i + page_size < len(lines):
                input("\n--- Press Enter for next page ---")
            else:
                input("\n--- End of report. Press Enter to continue ---")
    
    def save_session(self):
        """Save session history to file"""
        if self.research_history:
            session_file = self.reports_dir / f"session_{self.session_id}.json"
            with open(session_file, 'w') as f:
                json.dump(self.research_history, f, indent=2)
            print(f"\n Session saved: {session_file}")
    
    def run(self):
        """Main application loop"""
        while True:
            self.display_menu()
            choice = input("\n Select option (1-6): ").strip()
            
            if choice == '1':
                # Start new research
                query = self.get_user_query()
                if query:
                    self.run_research(query)
            
            elif choice == '2':
                # View history
                self.show_research_history()
            
            elif choice == '3':
                # Quick research
                query = self.show_quick_research_menu()
                if query:
                    confirm = input(f"\n Research: '{query[:60]}...'? (y/n): ").lower()
                    if confirm == 'y':
                        self.run_research(query)
            
            elif choice == '4':
                # Settings
                self.show_settings()
            
            elif choice == '5':
                # Help
                self.show_help()
            
            elif choice == '6':
                # Exit
                self.clear_screen()
                print("\n" + "="*70)
                print("Thank you for using Deep Research System!")
                print("="*70)
                
                if self.research_history:
                    save = input("\n Save session history? (y/n): ").lower()
                    if save == 'y':
                        self.save_session()
                
                print("\n  Goodbye!")
                print("="*70)
                sys.exit(0)
            
            else:
                print("\n Invalid option. Please try again.")
                time.sleep(1)

def main():
    """Entry point for the application"""
    try:
        # Create and run the system
        system = DeepResearchSystem()
        system.run()
        
    except KeyboardInterrupt:
        print("\n\n Application interrupted by user")
        print("Exiting gracefully...")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n Fatal error: {e}")
        print("\n💡 Please check:")
        print("1. Your .env file contains GEMINI_API_KEY")
        print("2. All agent files are present")
        print("3. Required packages are installed")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()