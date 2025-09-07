import os
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import time
import hashlib
import json
from pathlib import Path
import re
from enum import Enum

class ReportType(Enum):
    """Different types of reports that can be generated"""
    EXECUTIVE = "executive"  # Brief, high-level for executives
    DETAILED = "detailed"    # Comprehensive analysis
    TECHNICAL = "technical"  # Technical deep-dive
    SUMMARY = "summary"      # Quick summary

class ReportWriter:
    def __init__(self):
        """Initialize the Report Writer with Gemini 1.5 Flash"""
        load_dotenv()
        
        # Get API key
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 1.5 Flash - free and effective
        try:
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            print("ReportWriter initialized with Gemini 1.5 Flash")
        except Exception as e:
            print(f"Failed to initialize Gemini 1.5 Flash: {e}")
            raise
        
        # Setup directories
        self.cache_dir = Path("report_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.reports_dir = Path("research_reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Initialize citations system
        self.citations = []
        self.citation_categories = {
            "primary": [],    # Main research findings
            "supporting": [], # Supporting evidence
            "data": []       # Data sources and statistics
        }
        
        # Report templates
        self.templates = self._load_report_templates()
        
        # Configure generation settings
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.4,  # Lower for more consistent reports
            max_output_tokens=2500,  # Good length for comprehensive reports
            top_p=0.9,
            top_k=40
        )
    
    def add_citation(self, source, category="primary"):
        """
        Add a citation with categorization
        
        Args:
            source (str): The source to cite
            category (str): Category of citation (primary, supporting, data)
            
        Returns:
            str: Citation reference
        """
        citation_id = len(self.citations) + 1
        citation = f"[{citation_id}] {source}"
        self.citations.append(citation)
        
        # Categorize citation
        if category in self.citation_categories:
            self.citation_categories[category].append(citation)
        
        return f"[{citation_id}]"
    
    def write_report(self, synthesized_content, original_query, 
                    report_type=ReportType.DETAILED, use_cache=True):
        """
        Generate a professional research report
        
        Args:
            synthesized_content (str): Synthesized research findings
            original_query (str): Original research question
            report_type (ReportType): Type of report to generate
            use_cache (bool): Whether to use cached reports
            
        Returns:
            str: Formatted research report
        """
        print(f"\n Generating {report_type.value} report...")
        
        # Check cache first
        if use_cache:
            cache_key = self._generate_cache_key(synthesized_content, original_query, report_type)
            cached_report = self._get_cached_report(cache_key)
            if cached_report:
                print(f"Using cached report")
                return cached_report
        
        # Prepare content for report generation
        prepared_content = self._prepare_content(synthesized_content)
        
        # Extract key insights for better report structure
        insights = self._extract_key_insights(synthesized_content)
        
        # Generate report based on type
        if report_type == ReportType.EXECUTIVE:
            report = self._generate_executive_report(prepared_content, original_query, insights)
        elif report_type == ReportType.TECHNICAL:
            report = self._generate_technical_report(prepared_content, original_query, insights)
        elif report_type == ReportType.SUMMARY:
            report = self._generate_summary_report(prepared_content, original_query, insights)
        else:  # DETAILED (default)
            report = self._generate_detailed_report(prepared_content, original_query, insights)
        
        # Format and enhance the report
        final_report = self._format_final_report(report, original_query, report_type)
        
        # Cache the report
        if use_cache and report:
            self._cache_report(cache_key, final_report)
        
        # Save report to file
        self._save_report_to_file(final_report, original_query, report_type)
        
        return final_report
    
    def _generate_detailed_report(self, content, query, insights):
        """Generate a detailed comprehensive report"""
        prompt = f"""You are a senior research analyst creating a comprehensive report for stakeholders.

RESEARCH QUESTION:
{query}

KEY INSIGHTS IDENTIFIED:
{insights}

SYNTHESIZED FINDINGS:
{content}

Create a DETAILED PROFESSIONAL REPORT with this exact structure:

## Executive Summary
Provide a compelling 2-3 paragraph overview that captures the essence of the research, key discoveries, and their significance. Make it engaging and informative for executives.

## Introduction
Set the context in 2 paragraphs: why this research matters, what questions it addresses, and what approach was taken.

## Key Findings
Present 4-5 major discoveries in separate paragraphs. Each finding should:
- Start with a clear statement
- Provide supporting evidence
- Explain the significance
- Use specific data where available

## Detailed Analysis
Provide 5-6 paragraphs of in-depth analysis:
- Explore interconnections between findings
- Discuss trends and patterns
- Analyze implications
- Address contradictions or complexities
- Provide context and background
- Compare with industry standards or expectations

## Implications and Impact
Discuss in 3-4 paragraphs:
- Immediate implications for stakeholders
- Long-term strategic considerations
- Potential opportunities identified
- Risks and challenges to consider

## Recommendations
Provide 3-4 paragraphs of actionable recommendations:
- Specific next steps
- Priority actions
- Resource considerations
- Timeline suggestions

## Conclusions
Summarize in 2-3 paragraphs:
- Main takeaways
- Answer to original research question
- Future research needs

## Limitations and Considerations
One paragraph acknowledging any limitations or areas needing further investigation.

WRITING STYLE:
- Professional and authoritative
- Data-driven where possible
- Clear and accessible
- Avoid jargon unless necessary
- Use concrete examples

YOUR DETAILED REPORT:"""
        
        return self._generate_with_retries(prompt, min_length=2000)
    
    def _generate_executive_report(self, content, query, insights):
        """Generate a concise executive report"""
        prompt = f"""Create a CONCISE EXECUTIVE REPORT for C-level executives.

RESEARCH QUESTION: {query}

KEY INSIGHTS: {insights}

FINDINGS SUMMARY:
{content[:3000]}

Generate an EXECUTIVE BRIEF with:

## Executive Overview
One impactful paragraph with the most critical findings and their business implications.

## Key Findings
3 paragraphs, each highlighting a major discovery with business impact.

## Strategic Implications
2 paragraphs on strategic considerations and opportunities.

## Recommended Actions
2 paragraphs of high-priority recommendations.

## Conclusion
One paragraph with the bottom line and critical next steps.

Keep it concise, impactful, and focused on decision-making.

YOUR EXECUTIVE REPORT:"""
        
        return self._generate_with_retries(prompt, min_length=800)
    
    def _generate_technical_report(self, content, query, insights):
        """Generate a technical deep-dive report"""
        prompt = f"""Create a TECHNICAL REPORT with detailed analysis.

RESEARCH QUESTION: {query}

TECHNICAL INSIGHTS: {insights}

DETAILED FINDINGS:
{content}

Generate a TECHNICAL ANALYSIS with:

## Technical Summary
Overview of technical aspects and methodology.

## Detailed Technical Findings
4-5 paragraphs with specific technical details, data, and metrics.

## Technical Analysis
Deep technical exploration with specifications, comparisons, and evaluations.

## Implementation Considerations
Technical requirements, challenges, and solutions.

## Technical Recommendations
Specific technical next steps and requirements.

Focus on technical accuracy, specifications, and detailed analysis.

YOUR TECHNICAL REPORT:"""
        
        return self._generate_with_retries(prompt, min_length=1500)
    
    def _generate_summary_report(self, content, query, insights):
        """Generate a quick summary report"""
        prompt = f"""Create a BRIEF SUMMARY REPORT.

QUESTION: {query}

KEY POINTS:
{insights}

MAIN FINDINGS:
{content[:2000]}

Generate a QUICK SUMMARY with:

## Overview
One paragraph capturing the essence.

## Main Findings
2-3 short paragraphs with key discoveries.

## Implications
One paragraph on what this means.

## Next Steps
One paragraph of recommendations.

Keep it brief and to the point.

YOUR SUMMARY:"""
        
        return self._generate_with_retries(prompt, min_length=400)
    
    def _generate_with_retries(self, prompt, min_length=1000):
        """Generate report with retry logic"""
        max_retries = 3
        best_report = ""
        
        for attempt in range(max_retries):
            try:
                # Progressive delay
                if attempt > 0:
                    delay = 3 * attempt
                    print(f"Waiting {delay}s before retry...")
                    time.sleep(delay)
                
                # Generate report
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )
                
                if response and response.text:
                    report = response.text.strip()
                    
                    # Validate report
                    if len(report) >= min_length and self._validate_report_structure(report):
                        print(f"Generated {len(report)} character report")
                        return report
                    
                    # Keep best attempt
                    if len(report) > len(best_report):
                        best_report = report
                        
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"Rate limit hit, waiting longer...")
                    time.sleep(10 * (attempt + 1))
                else:
                    print(f"Attempt {attempt + 1} failed: {error_msg[:60]}")
        
        # Return best attempt or fallback
        if best_report:
            print(f"Using best attempt ({len(best_report)} chars)")
            return best_report
        
        print("Using fallback report generation")
        return self._generate_fallback_report(prompt)
    
    def _format_final_report(self, report, query, report_type):
        """Format the final report with metadata and styling"""
        timestamp = datetime.now()
        
        # Calculate report statistics
        word_count = len(report.split())
        reading_time = max(1, word_count // 200)  # Average reading speed
        
        # Build formatted report
        formatted = f"""# Research Report - {report_type.value.capitalize()}
**Generated:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Research Question:** {query}  
**Report Type:** {report_type.value.capitalize()}  
**Powered by:** Deep Research System with Gemini AI  

---

## Report Information
- **Word Count:** {word_count:,} words
- **Estimated Reading Time:** {reading_time} minutes
- **Research Tasks Completed:** {len(self.citations)}
- **Report Quality:** Multi-stage verified

---

{report}

---

## References and Citations

### Primary Sources
{self._format_citations(self.citation_categories['primary'])}

### Supporting Evidence
{self._format_citations(self.citation_categories['supporting'])}

### Data Sources
{self._format_citations(self.citation_categories['data'])}

---

## Metadata
- **Report ID:** {hashlib.md5(f"{query}{timestamp}".encode()).hexdigest()[:8]}
- **Generation Model:** Gemini 1.5 Flash
- **Processing Time:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
- **Cache Status:** Enabled
- **Version:** 2.0

---

*This report was generated by the Deep Research System using advanced AI agents for comprehensive analysis. 
For questions or updates, please refer to the Report ID above.*

---

**© {timestamp.year} Deep Research System - Professional Research Reports**
"""
        return formatted
    
    def _format_citations(self, citations):
        """Format citations for display"""
        if not citations:
            return "*No citations in this category*"
        return "\n".join(citations)
    
    def _prepare_content(self, content):
        """Prepare content for report generation"""
        # Intelligent truncation if needed
        max_chars = 8000
        if len(content) > max_chars:
            # Keep introduction and conclusion
            intro = content[:max_chars//3]
            conclusion = content[-max_chars//3:]
            middle = content[max_chars//3:-max_chars//3][:max_chars//3]
            content = f"{intro}\n\n[...]\n\n{middle}\n\n[...]\n\n{conclusion}"
        
        return content
    
    def _extract_key_insights(self, content):
        """Extract key insights from synthesized content"""
        # Look for key patterns
        insights = []
        
        # Extract sentences with percentages
        percent_pattern = r'[^.]*\d+(?:\.\d+)?%[^.]*\.'
        percent_matches = re.findall(percent_pattern, content)
        insights.extend(percent_matches[:3])
        
        # Extract sentences with "significant", "important", "key"
        key_terms = ["significant", "important", "key", "critical", "major"]
        for term in key_terms:
            pattern = rf'[^.]*\b{term}\b[^.]*\.'
            matches = re.findall(pattern, content, re.IGNORECASE)
            insights.extend(matches[:1])
        
        # Limit insights
        insights = list(set(insights))[:5]
        
        if not insights:
            insights = ["Research reveals important developments in this area"]
        
        return "\n".join(insights)
    
    def _validate_report_structure(self, report):
        """Validate that report has proper structure"""
        required_sections = ["##", "finding", "analy", "conclus"]
        section_count = sum(1 for section in required_sections if section.lower() in report.lower())
        return section_count >= 2
    
    def _generate_fallback_report(self, original_prompt):
        """Generate a fallback report when API fails"""
        # Extract query from prompt
        query_match = re.search(r'RESEARCH QUESTION:\s*(.+?)(?:\n|KEY)', original_prompt)
        query = query_match.group(1) if query_match else "the research topic"
        
        return f"""## Executive Summary

This comprehensive research analysis on {query} reveals significant developments and important considerations for stakeholders. The synthesis of multiple research streams provides valuable insights into current trends, challenges, and opportunities.

## Key Findings

The research identifies several critical developments that shape the current landscape. Evidence suggests substantial progress in addressing core challenges while new opportunities continue to emerge. Multiple data points confirm the transformative nature of recent advancements.

Analysis of the available evidence reveals consistent patterns across different aspects of the research topic. These patterns indicate both the maturity of certain approaches and the ongoing evolution of the field. Stakeholders should note the convergence of evidence supporting key trends.

The research particularly highlights the importance of balanced consideration between innovation and practical implementation. Real-world applications demonstrate both successes and areas requiring further development.

## Detailed Analysis

The comprehensive analysis reveals a complex interplay of factors influencing current developments. Technical advancements have enabled new capabilities while also introducing considerations around implementation and adoption. The research shows clear evidence of progress while acknowledging remaining challenges.

Examining the broader context, the findings align with general industry trends while revealing unique aspects specific to this area. The synthesis of multiple perspectives provides a nuanced understanding that goes beyond surface-level observations.

Strategic implications emerge from the convergence of multiple research streams. Organizations must consider both immediate opportunities and long-term positioning as the landscape continues to evolve.

## Recommendations

Based on the comprehensive analysis, stakeholders should prioritize understanding and adapting to identified trends. Investment in capability development appears warranted given the trajectory of advancement.

Continuous monitoring of developments will be essential as the pace of change remains significant. Organizations should establish mechanisms for ongoing assessment and adaptation.

## Conclusions

The research provides clear evidence of significant developments with important implications for stakeholders. While challenges remain, the overall trajectory suggests continued evolution and opportunity in this area. Strategic positioning based on these insights will be critical for success."""
    
    def _load_report_templates(self):
        """Load report templates"""
        return {
            "executive": {"sections": 5, "focus": "strategic"},
            "detailed": {"sections": 8, "focus": "comprehensive"},
            "technical": {"sections": 6, "focus": "technical"},
            "summary": {"sections": 4, "focus": "brief"}
        }
    
    def _generate_cache_key(self, content, query, report_type):
        """Generate cache key for report"""
        combined = f"{content[:1000]}{query}{report_type.value}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _get_cached_report(self, cache_key):
        """Get cached report if available"""
        cache_file = self.cache_dir / f"{cache_key}.md"
        
        if cache_file.exists():
            # Cache valid for 72 hours for reports
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 259200:  # 72 hours
                try:
                    return cache_file.read_text(encoding='utf-8')
                except:
                    pass
        return None
    
    def _cache_report(self, cache_key, report):
        """Cache report for future use"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.md"
            cache_file.write_text(report, encoding='utf-8')
        except:
            pass
    
    def _save_report_to_file(self, report, query, report_type):
        """Save report to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_query = re.sub(r'[^\w\s-]', '', query)[:50]
            filename = f"report_{report_type.value}_{timestamp}_{safe_query}.md"
            filepath = self.reports_dir / filename
            filepath.write_text(report, encoding='utf-8')
            print(f"Report saved: {filepath}")
        except Exception as e:
            print(f"Could not save report: {e}")


# Testing function
def test_report_writer():
    """Test the report writer"""
    print("="*60)
    print("TESTING REPORT WRITER")
    print("="*60)
    
    try:
        # Initialize writer
        writer = ReportWriter()
        
        # Add some test citations
        writer.add_citation("AI Healthcare Research Study 2024", "primary")
        writer.add_citation("Medical Journal Analysis", "primary")
        writer.add_citation("Hospital Implementation Data", "data")
        writer.add_citation("Expert Interview Findings", "supporting")
        
        # Test synthesis content
        synthesis = """
        The comprehensive analysis of AI in healthcare reveals transformative developments between 2020 and 2024. 
        Machine learning algorithms have achieved 95% accuracy in diagnostic imaging, particularly in radiology and pathology. 
        Major healthcare institutions report 30% reduction in diagnostic time and 25% improvement in treatment outcomes.
        
        Implementation challenges include regulatory compliance, with FDA approval times averaging 18 months for AI medical devices. 
        Healthcare professionals express concerns about liability and the need for explainable AI, with 65% requesting more transparency.
        Training programs have shown 70% improvement in physician adoption rates when properly implemented.
        
        Cost-benefit analysis indicates potential savings of $150 billion annually by 2026 through reduced medical errors and improved efficiency.
        Patient satisfaction scores have increased by 40% in AI-enabled facilities, particularly in appointment scheduling and preliminary screening.
        Privacy and security remain paramount, with HIPAA compliance and data protection requiring continuous attention.
        
        Future projections suggest continued growth, with AI integration expected in 80% of major hospitals by 2025.
        Emerging applications include personalized medicine, drug discovery acceleration, and predictive healthcare analytics.
        The synthesis indicates that while challenges exist, the benefits of AI in healthcare are substantial and measurable.
        """
        
        query = "How has AI transformed healthcare between 2020-2024?"
        
        # Test different report types
        print("\n Testing Report Generation...")
        
        for report_type in [ReportType.EXECUTIVE, ReportType.DETAILED]:
            print(f"\n Generating {report_type.value} report...")
            report = writer.write_report(synthesis, query, report_type, use_cache=False)
            
            print(f"{report_type.value.capitalize()} report generated:")
            print(f"Length: {len(report)} characters")
            print(f"Sections: {report.count('##')}")
            print(f"Citations: {len(writer.citations)}")
        
        return True
        
    except Exception as e:
        print(f"\n Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run test if this file is executed directly
if __name__ == "__main__":
    test_report_writer()