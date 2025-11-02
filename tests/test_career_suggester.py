"""
Career Suggester AI Diagnostic Test Suite
Tests the 11-question career path suggestion system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
from diagnostic_framework import AITestCase, DiagnosticReport, TestStep, TestStatus


class CareerSuggesterTest(AITestCase):
    """Test suite for Career Suggester AI"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        super().__init__("Career Suggester AI Test", "career_suggester")
        self.base_url = base_url
        self.api_url = f"{base_url}/api/suggester"
        self.test_answers = [
            "I enjoyed mathematics, computer science, and problem-solving activities",
            "Problem-solving, analytical thinking, and Python programming",
            "I prefer independent work with occasional collaboration, and a structured environment",
            "Technical challenges involving algorithms and data analysis",
            "Competitive salary with growth potential, around $60,000-$80,000 initially",
            "I'm interested in technology and software companies, avoiding sales-heavy roles",
            "Bachelor's degree in Computer Science",
            "Completed 2 internships in software development and built 3 personal projects",
            "AWS Certified Cloud Practitioner, Python certification from Coursera",
            "Technical role with some research opportunities",
            "Open to relocation for the right opportunity"
        ]
    
    def run(self) -> DiagnosticReport:
        """Execute the Career Suggester AI test"""
        
        print("🧪 Testing Career Suggester AI...")
        
        # Step 1: Initialize suggester
        step = self.create_step("Initialize Career Suggester")
        step.expected = "Receive first question"
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.api_url}/start")
            step.duration_ms = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("next_question"):
                    step.actual = f"Received question: {data['next_question']['text'][:50]}..."
                    step.status = TestStatus.PASS
                    self.report.summary["initialization"] = "SUCCESS"
                else:
                    step.actual = "Failed to get first question"
                    step.status = TestStatus.FAIL
                    self.report.add_issue("ERROR", "Initialization failed", str(data))
            else:
                step.actual = f"HTTP {response.status_code}"
                step.status = TestStatus.FAIL
                self.report.add_issue("ERROR", "API request failed", f"Status code: {response.status_code}")
        except Exception as e:
            step.actual = f"Exception: {str(e)}"
            step.status = TestStatus.ERROR
            step.error = str(e)
            self.report.add_issue("CRITICAL", "Connection error", str(e))
        
        self.report.add_step(step)
        self.report.metadata["api_calls"] += 1
        
        # Step 2-12: Answer all 11 questions
        current_question_index = 0
        answers_so_far = {}
        questions_asked = []
        
        for i, answer in enumerate(self.test_answers):
            step = self.create_step(f"Submit answer {i+1}/11")
            step.expected = "Receive next question or final suggestions"
            start_time = time.time()
            
            try:
                payload = {
                    "answer": answer,
                    "current_question_index": current_question_index,
                    "answers_so_far": answers_so_far
                }
                
                response = requests.post(f"{self.api_url}/answer", json=payload)
                step.duration_ms = int((time.time() - start_time) * 1000)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        # Store the answer
                        if i < len(self.test_answers) - 1:
                            # Expect next question
                            if data.get("next_question"):
                                next_q = data['next_question']['text']
                                questions_asked.append(next_q)
                                step.actual = f"Question {i+2}: {next_q[:40]}..."
                                step.status = TestStatus.PASS
                                
                                # Update for next iteration
                                current_question_index = data.get("current_question_index", current_question_index + 1)
                                answers_so_far = data.get("answers_so_far", answers_so_far)
                            else:
                                step.actual = "No next question received"
                                step.status = TestStatus.FAIL
                                self.report.add_issue("ERROR", f"Missing next question at step {i+1}", "")
                        else:
                            # Last question - expect suggestions
                            if data.get("suggestions"):
                                suggestions = data["suggestions"]
                                step.actual = f"Received {len(suggestions.get('suggestions', []))} career suggestions"
                                step.status = TestStatus.PASS
                                step.metadata["suggestions"] = suggestions
                            else:
                                step.actual = "No suggestions received"
                                step.status = TestStatus.FAIL
                                self.report.add_issue("ERROR", "No career suggestions generated", "")
                    else:
                        step.actual = f"API returned success=false: {data.get('error', 'Unknown')}"
                        step.status = TestStatus.FAIL
                        self.report.add_issue("ERROR", f"Answer {i+1} failed", data.get("error", ""))
                else:
                    step.actual = f"HTTP {response.status_code}"
                    step.status = TestStatus.FAIL
                    self.report.add_issue("ERROR", f"API error at question {i+1}", f"Status: {response.status_code}")
            
            except Exception as e:
                step.actual = f"Exception: {str(e)}"
                step.status = TestStatus.ERROR
                step.error = str(e)
                self.report.add_issue("CRITICAL", f"Error at question {i+1}", str(e))
            
            self.report.add_step(step)
            self.report.metadata["api_calls"] += 1
        
        # Analyze final suggestions
        final_step = self.test_steps[-1] if self.test_steps else None
        if final_step and "suggestions" in final_step.metadata:
            self._analyze_suggestions(final_step.metadata["suggestions"])
        
        # Build summary
        self.report.summary = {
            "total_questions": 11,
            "questions_asked": len(questions_asked) + 1,  # +1 for initial question
            "answers_provided": len(self.test_answers),
            "suggestions_generated": len(final_step.metadata.get("suggestions", {}).get("suggestions", [])) if final_step and "suggestions" in final_step.metadata else 0,
            "errors": self.report.metadata["errors_count"],
            "warnings": self.report.metadata["warnings_count"]
        }
        
        # AI Analysis
        self.report.ai_analysis = {
            "all_questions_completed": self.report.summary["questions_asked"] == 11,
            "all_answers_processed": self.report.summary["answers_provided"] == 11,
            "suggestions_generated": self.report.summary["suggestions_generated"] > 0,
            "suggestion_quality": self._assess_quality(final_step.metadata.get("suggestions") if final_step else None),
            "response_time_avg_ms": sum(s.duration_ms for s in self.test_steps) / len(self.test_steps) if self.test_steps else 0,
            "logical_flow": len(questions_asked) + 1 == 11
        }
        
        return self.report
    
    def _analyze_suggestions(self, suggestions_data: dict):
        """Analyze the quality and validity of career suggestions"""
        suggestions = suggestions_data.get("suggestions", [])
        summary = suggestions_data.get("summary", "")
        
        step = self.create_step("Analyze Career Suggestions")
        step.expected = "Valid career suggestions with reasons"
        
        issues = []
        
        # Check if suggestions exist
        if not suggestions:
            issues.append("No career suggestions provided")
            step.status = TestStatus.FAIL
        
        # Check if summary exists
        if not summary:
            issues.append("No summary provided")
            step.status = TestStatus.WARNING
        
        # Validate each suggestion
        for i, suggestion in enumerate(suggestions):
            if not suggestion.get("career"):
                issues.append(f"Suggestion {i+1}: Missing career title")
                step.status = TestStatus.FAIL
            
            if not suggestion.get("reason"):
                issues.append(f"Suggestion {i+1}: Missing reason/justification")
                step.status = TestStatus.WARNING
            
            # Check if reason is substantive (more than 20 characters)
            if suggestion.get("reason") and len(suggestion["reason"]) < 20:
                issues.append(f"Suggestion {i+1}: Reason too short")
                step.status = TestStatus.WARNING
        
        # Check for tech-related careers (based on our test profile)
        tech_keywords = ["software", "engineer", "developer", "data", "cloud", "tech", "IT", "computer"]
        has_tech_career = any(
            any(keyword.lower() in suggestion.get("career", "").lower() for keyword in tech_keywords)
            for suggestion in suggestions
        )
        
        if not has_tech_career:
            issues.append("No technology-related careers suggested despite tech-focused profile")
            step.status = TestStatus.WARNING
            self.report.add_recommendation("Improve AI's ability to match suggestions to user profile")
        
        if issues:
            step.actual = f"Issues found: {', '.join(issues)}"
            for issue in issues:
                self.report.add_issue("WARNING", "Suggestion validation", issue)
        else:
            step.actual = f"All {len(suggestions)} suggestions are valid and well-reasoned"
            step.status = TestStatus.PASS
        
        self.report.add_step(step)
    
    def _assess_quality(self, suggestions_data: dict) -> str:
        """Assess the overall quality of suggestions"""
        if not suggestions_data:
            return "none"
        
        suggestions = suggestions_data.get("suggestions", [])
        
        if len(suggestions) >= 3 and all(s.get("career") and s.get("reason") for s in suggestions):
            return "high"
        elif len(suggestions) >= 2:
            return "medium"
        else:
            return "low"


# Standalone test execution
if __name__ == "__main__":
    from diagnostic_framework import TestRunner
    
    print("Starting Career Suggester AI Diagnostic Test...")
    
    runner = TestRunner(output_dir="logs")
    test = CareerSuggesterTest()
    report = runner.run_test(test, verbose=True)
    
    print(f"\n{'='*70}")
    print(f"Test completed with status: {report.status.value}")
    print(f"Final score: {report.score:.1f}/100")
    print(f"{'='*70}\n")

