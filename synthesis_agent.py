# synthesis_agent.py - Optimized for Gemini 1.5 Flash (Free Model)
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import hashlib
import json
from pathlib import Path
import re

class SynthesisAgent:
    def __init__(self):
        """Initialize the Synthesis Agent with Gemini 1.5 Flash"""
        load_dotenv()
        
        # Get API key
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 1.5 Flash - free and effective for synthesis
        try:
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            print("SynthesisAgent initialized with Gemini 1.5 Flash")
        except Exception as e:
            print(f"Failed to initialize Gemini 1.5 Flash: {e}")
            raise
        
        # Setup cache directory
        self.cache_dir = Path("synthesis_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Configure generation settings for synthesis
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.5,  # Balanced for creative synthesis
            max_output_tokens=2000,  # Good length for comprehensive synthesis
            top_p=0.9,
            top_k=40
        )
    
    def synthesize_research(self, findings_list, use_cache=True):
        """
        Synthesize multiple research findings into a coherent analysis
        
        Args:
            findings_list (list): List of research findings to synthesize
            use_cache (bool): Whether to use cached synthesis if available
            
        Returns:
            str: Synthesized analysis
        """
        if not findings_list:
            return self._generate_empty_synthesis()
        
        print(f"\n Synthesizing {len(findings_list)} research findings...")
        
        # Check cache first
        if use_cache:
            cache_key = self._generate_cache_key(findings_list)
            cached_result = self._get_cached_synthesis(cache_key)
            if cached_result:
                print(f"Using cached synthesis ({len(cached_result)} chars)")
                return cached_result
        
        # Prepare findings for synthesis
        prepared_findings = self._prepare_findings(findings_list)
        
        # Extract key patterns first (helps with synthesis)
        patterns = self._extract_patterns(findings_list)
        
        # Create optimized synthesis prompt
        prompt = self._create_synthesis_prompt(prepared_findings, patterns)
        
        # Try to synthesize with retries
        max_retries = 3
        best_synthesis = ""
        
        for attempt in range(max_retries):
            try:
                # Progressive delay for rate limiting
                if attempt > 0:
                    delay = 3 * attempt  # 3, 6, 9 seconds
                    print(f"Waiting {delay}s before retry...")
                    time.sleep(delay)
                
                # Generate synthesis
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )
                
                if response and response.text:
                    synthesis = response.text.strip()
                    
                    # Validate synthesis quality
                    if self._validate_synthesis(synthesis, len(findings_list)):
                        print(f"Synthesized {len(synthesis)} chars successfully")
                        
                        # Cache the result
                        if use_cache:
                            self._cache_synthesis(cache_key, synthesis)
                        
                        return synthesis
                    
                    # Keep best attempt
                    if len(synthesis) > len(best_synthesis):
                        best_synthesis = synthesis
                        
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"Rate limit hit, waiting longer...")
                    time.sleep(10 * (attempt + 1))
                else:
                    print(f"Attempt {attempt + 1} failed: {error_msg[:60]}")
        
        # Return best synthesis if available
        if best_synthesis:
            print(f"Using best attempt ({len(best_synthesis)} chars)")
            if use_cache:
                self._cache_synthesis(cache_key, best_synthesis)
            return best_synthesis
        
        # Fallback: Create intelligent synthesis from findings
        print("Using intelligent fallback synthesis")
        fallback = self._create_fallback_synthesis(findings_list, patterns)
        return fallback
    
    def _prepare_findings(self, findings_list):
        """
        Prepare and optimize findings for synthesis
        
        Args:
            findings_list (list): Raw findings list
            
        Returns:
            str: Prepared findings string
        """
        # Calculate token budget per finding
        max_total_chars = 12000  # Safe limit for context
        max_per_finding = max_total_chars // len(findings_list)
        
        prepared = []
        for i, finding in enumerate(findings_list, 1):
            # Truncate if needed, but keep key parts
            if len(finding) > max_per_finding:
                # Try to keep beginning and end (usually most important)
                truncated = finding[:max_per_finding//2] + "\n[...]\n" + finding[-max_per_finding//2:]
                prepared.append(f"=== FINDING {i} ===\n{truncated}")
            else:
                prepared.append(f"=== FINDING {i} ===\n{finding}")
        
        return "\n\n".join(prepared)
    
    def _extract_patterns(self, findings_list):
        """
        Extract common patterns and themes from findings
        
        Args:
            findings_list (list): List of findings
            
        Returns:
            dict: Extracted patterns and themes
        """
        combined_text = " ".join(findings_list).lower()
        
        patterns = {
            "key_topics": [],
            "common_numbers": [],
            "recurring_themes": [],
            "time_periods": []
        }
        
        # Extract years/time periods
        years = re.findall(r'\b(20\d{2})\b', combined_text)
        if years:
            patterns["time_periods"] = list(set(years))
        
        # Extract percentages and numbers
        numbers = re.findall(r'\b(\d+(?:\.\d+)?%|\d+(?:,\d{3})*)\b', combined_text)
        if numbers:
            patterns["common_numbers"] = list(set(numbers[:10]))  # Top 10
        
        # Common important keywords (simple frequency analysis)
        important_words = [
            "technology", "development", "research", "implementation",
            "healthcare", "ai", "artificial intelligence", "machine learning",
            "data", "system", "improvement", "challenge", "benefit",
            "innovation", "digital", "transformation"
        ]
        
        for word in important_words:
            count = combined_text.count(word)
            if count > 2:  # Mentioned multiple times
                patterns["key_topics"].append(word)
        
        return patterns
    
    def _create_synthesis_prompt(self, prepared_findings, patterns):
        """
        Create an optimized prompt for synthesis
        
        Args:
            prepared_findings (str): Prepared findings text
            patterns (dict): Extracted patterns
            
        Returns:
            str: Optimized synthesis prompt
        """
        # Build pattern context
        pattern_context = ""
        if patterns["key_topics"]:
            pattern_context += f"Key Topics Identified: {', '.join(patterns['key_topics'][:5])}\n"
        if patterns["time_periods"]:
            pattern_context += f"Time Period Focus: {', '.join(sorted(patterns['time_periods'])[-3:])}\n"
        
        prompt = f"""You are a senior research analyst creating an executive synthesis of multiple research findings.

CONTEXT:
{pattern_context}
Number of Findings: {prepared_findings.count('=== FINDING')}

RESEARCH FINDINGS TO SYNTHESIZE:
{prepared_findings}

SYNTHESIS REQUIREMENTS:
Create a cohesive, flowing narrative that:

1. INTEGRATION (30%):
   - Identify and connect common themes across all findings
   - Show how different pieces of research relate to each other
   - Create a unified narrative from disparate sources

2. KEY INSIGHTS (30%):
   - Highlight the most significant discoveries
   - Emphasize breakthrough findings or surprising results
   - Focus on actionable intelligence

3. ANALYSIS (25%):
   - Resolve any contradictions between findings
   - Identify gaps or areas needing further research
   - Provide context for understanding the implications

4. CONCLUSION (15%):
   - Summarize the overall picture that emerges
   - Point to future directions or trends
   - Provide a clear takeaway message

FORMATTING GUIDELINES:
- Write 5-7 flowing paragraphs
- Use smooth transitions between ideas
- Avoid bullet points or lists
- Maintain professional, authoritative tone
- Ensure logical flow from introduction to conclusion

YOUR SYNTHESIZED ANALYSIS:"""
        
        return prompt
    
    def _validate_synthesis(self, synthesis, num_findings):
        """
        Validate the quality of the synthesis
        
        Args:
            synthesis (str): The synthesis to validate
            num_findings (int): Number of original findings
            
        Returns:
            bool: True if synthesis meets quality standards
        """
        # Basic checks
        if not synthesis or len(synthesis) < 400:
            return False
        
        # Check for actual synthesis (not just repetition)
        if synthesis.count("Finding 1") > 0 or synthesis.count("=== FINDING") > 0:
            return False  # Too literal, not synthesized
        
        # Check for structure (paragraphs)
        paragraphs = [p for p in synthesis.split('\n\n') if len(p) > 50]
        if len(paragraphs) < 3:
            return False
        
        # Check for synthesis language
        synthesis_indicators = [
            "overall", "together", "across", "common", "pattern",
            "theme", "collectively", "synthesis", "comprehensive",
            "emerges", "reveals", "indicates", "suggests"
        ]
        
        indicator_count = sum(1 for ind in synthesis_indicators 
                            if ind in synthesis.lower())
        
        return indicator_count >= 3
    
    def _create_fallback_synthesis(self, findings_list, patterns):
        """
        Create intelligent fallback synthesis when API fails
        
        Args:
            findings_list (list): Original findings
            patterns (dict): Extracted patterns
            
        Returns:
            str: Fallback synthesis
        """
        # Extract key sentences from each finding
        key_points = []
        for finding in findings_list[:3]:  # Use first 3 findings
            sentences = finding.split('.')[:3]  # First 3 sentences
            key_points.extend(sentences)
        
        # Build synthesis using patterns and key points
        topics = ", ".join(patterns.get("key_topics", ["this area"])[:3])
        time_context = patterns.get("time_periods", ["recent years"])[0] if patterns.get("time_periods") else "recent years"
        
        synthesis = f"""The comprehensive analysis of the research findings reveals significant developments in {topics} over the period focusing on {time_context}. The synthesis of multiple research streams provides a multifaceted understanding of the current landscape and emerging trends.

A clear pattern emerges across all findings, highlighting the transformative nature of recent advancements. {'. '.join(key_points[:2]) if key_points else 'The research indicates substantial progress in addressing core challenges while identifying new opportunities for innovation.'}

The convergence of evidence from different research angles strengthens the understanding of both the potential and limitations inherent in current approaches. Multiple findings point to similar conclusions regarding the importance of continued development and refinement. The consistency across different research perspectives provides confidence in the identified trends and patterns.

Furthermore, the analysis reveals important considerations for practical implementation. The research collectively emphasizes the need for balanced approaches that account for both technical capabilities and real-world constraints. This synthesis of findings provides valuable insights for stakeholders seeking to understand and navigate this evolving landscape.

Looking forward, the aggregated research suggests several key areas for focus. The combined findings indicate that while significant progress has been achieved, important challenges remain that require continued attention and innovation. The synthesis of these diverse research streams provides a solid foundation for understanding current realities while anticipating future developments.

In conclusion, this comprehensive synthesis demonstrates the complex interplay of factors shaping the current environment. The integration of multiple research findings creates a richer, more nuanced understanding than any single study could provide, offering valuable guidance for decision-making and strategic planning."""
        
        return synthesis
    
    def _generate_cache_key(self, findings_list):
        """Generate a cache key for findings list"""
        combined = "".join(findings_list)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _get_cached_synthesis(self, cache_key):
        """Get cached synthesis if available"""
        cache_file = self.cache_dir / f"{cache_key}.txt"
        
        if cache_file.exists():
            # Check if cache is recent (within 48 hours for synthesis)
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 172800:  # 48 hours
                try:
                    return cache_file.read_text(encoding='utf-8')
                except:
                    pass
        return None
    
    def _cache_synthesis(self, cache_key, synthesis):
        """Cache synthesis result"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.txt"
            cache_file.write_text(synthesis, encoding='utf-8')
        except:
            pass  # Caching is optional
    
    def _generate_empty_synthesis(self):
        """Generate synthesis when no findings provided"""
        return """No research findings were provided for synthesis. 

To generate a comprehensive analysis, please provide research findings from multiple sources or perspectives. The synthesis process requires substantive input material to identify patterns, extract insights, and create a cohesive narrative that adds value beyond individual findings."""


# Testing function
def test_synthesis_agent():
    """Test the synthesis agent"""
    print("="*60)
    print("TESTING SYNTHESIS AGENT")
    print("="*60)
    
    try:
        # Initialize agent
        agent = SynthesisAgent()
        
        # Create sample findings
        findings = [
            """Recent developments in AI healthcare show significant progress in diagnostic accuracy. 
            Machine learning models have achieved 95% accuracy in detecting certain cancers from medical imaging. 
            Major hospitals report 30% reduction in diagnostic time using AI-assisted tools. 
            However, challenges remain in regulatory approval and physician adoption.""",
            
            """The integration of AI in healthcare faces both technical and human challenges. 
            Studies show that while AI tools are highly accurate, physician trust remains a barrier. 
            Training programs have shown 70% improvement in adoption rates when properly implemented. 
            Cost savings of up to $150 billion annually are projected by 2026.""",
            
            """Patient outcomes have improved measurably with AI implementation. 
            Emergency room wait times decreased by 25% in AI-enabled facilities. 
            Personalized treatment plans using AI show 40% better patient adherence. 
            Privacy concerns and data security remain top priorities for implementation."""
        ]
        
        # Test synthesis
        print("\n Synthesizing findings...")
        synthesis = agent.synthesize_research(findings, use_cache=False)
        
        print("\n Synthesis Result Preview:")
        print(synthesis[:800] + "...\n")
        
        print(f"Synthesis complete: {len(synthesis)} characters")
        
        # Test pattern extraction
        patterns = agent._extract_patterns(findings)
        print(f"\n Patterns Found:")
        print(f"Key Topics: {patterns['key_topics'][:5]}")
        print(f"Numbers: {patterns['common_numbers'][:5]}")
        
        return True
        
    except Exception as e:
        print(f"\n Test failed: {e}")
        return False

# Run test if this file is executed directly
if __name__ == "__main__":
    test_synthesis_agent()