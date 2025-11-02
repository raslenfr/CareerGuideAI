"""
Career Chatbot AI Diagnostic Test Suite
Tests the conversational career guidance AI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
from diagnostic_framework import AITestCase, DiagnosticReport, TestStep, TestStatus


class ChatbotTest(AITestCase):
    """Test suite for Career Chatbot AI"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        super().__init__("Career Chatbot AI Test", "chatbot")
        self.base_url = base_url
        self.api_url = f"{base_url}/api/chatbot"
        self.test_messages = [
            "Hello, I need career advice",
            "What skills are most important for data science?",
            "How can I transition from marketing to data analytics?",
            "What certifications should I get for cloud computing?",
            "Tell me about career opportunities in AI"
        ]
        self.conversation_history = []
    
    def run(self) -> DiagnosticReport:
        """Execute the Chatbot AI test"""
        
        print("[TEST] Testing Career Chatbot AI...")
        
        total_response_time = 0
        responses_received = 0
        
        # Test each message
        for i, message in enumerate(self.test_messages):
            step = self.create_step(f"Send message {i+1}: '{message[:40]}...'")
            step.expected = "Receive relevant career guidance response"
            start_time = time.time()
            
            try:
                payload = {
                    "message": message,
                    "history": self.conversation_history
                }
                
                response = requests.post(f"{self.api_url}/message", json=payload)
                step.duration_ms = int((time.time() - start_time) * 1000)
                total_response_time += step.duration_ms
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success") and data.get("reply"):
                        reply = data["reply"]
                        responses_received += 1
                        
                        # Update conversation history
                        self.conversation_history.append({"role": "user", "content": message})
                        self.conversation_history.append({"role": "assistant", "content": reply})
                        
                        # Analyze response quality
                        quality = self._analyze_response_quality(message, reply)
                        
                        step.actual = f"Received reply ({len(reply)} chars): {reply[:60]}..."
                        step.metadata = {
                            "message": message,
                            "reply": reply,
                            "reply_length": len(reply),
                            "quality_score": quality["score"],
                            "relevance": quality["relevance"],
                            "completeness": quality["completeness"]
                        }
                        
                        if quality["score"] >= 70:
                            step.status = TestStatus.PASS
                        elif quality["score"] >= 50:
                            step.status = TestStatus.WARNING
                            self.report.add_issue("WARNING", f"Message {i+1}: Low quality response", f"Score: {quality['score']}")
                        else:
                            step.status = TestStatus.FAIL
                            self.report.add_issue("ERROR", f"Message {i+1}: Poor quality response", f"Score: {quality['score']}")
                        
                        # Check for career relevance
                        if not quality["career_relevant"]:
                            self.report.add_issue("WARNING", f"Message {i+1}: Response not career-focused", reply[:100])
                    else:
                        step.actual = f"API returned success=false or no reply: {data.get('error', 'Unknown')}"
                        step.status = TestStatus.FAIL
                        self.report.add_issue("ERROR", f"Message {i+1} failed", data.get("error", "No reply received"))
                else:
                    step.actual = f"HTTP {response.status_code}"
                    step.status = TestStatus.FAIL
                    self.report.add_issue("ERROR", f"API error at message {i+1}", f"Status: {response.status_code}")
            
            except Exception as e:
                step.actual = f"Exception: {str(e)}"
                step.status = TestStatus.ERROR
                step.error = str(e)
                self.report.add_issue("CRITICAL", f"Error at message {i+1}", str(e))
            
            self.report.add_step(step)
            self.report.metadata["api_calls"] += 1
        
        # Build summary
        self.report.summary = {
            "total_messages": len(self.test_messages),
            "messages_sent": len(self.test_messages),
            "responses_received": responses_received,
            "avg_response_time_ms": int(total_response_time / responses_received) if responses_received > 0 else 0,
            "conversation_length": len(self.conversation_history),
            "errors": self.report.metadata["errors_count"],
            "warnings": self.report.metadata["warnings_count"]
        }
        
        # Calculate quality metrics
        quality_scores = [
            step.metadata.get("quality_score", 0) 
            for step in self.report.test_steps 
            if "quality_score" in step.metadata
        ]
        
        # AI Analysis
        self.report.ai_analysis = {
            "all_messages_processed": responses_received == len(self.test_messages),
            "avg_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            "response_time_acceptable": self.report.summary["avg_response_time_ms"] < 5000,
            "conversation_coherent": len(self.conversation_history) == len(self.test_messages) * 2,
            "career_focused": self._check_career_focus(),
            "response_completeness": responses_received / len(self.test_messages) * 100 if self.test_messages else 0
        }
        
        # Add recommendations
        if self.report.summary["avg_response_time_ms"] > 3000:
            self.report.add_recommendation("Consider optimizing response time (currently averaging > 3 seconds)")
        
        if self.report.ai_analysis["avg_quality_score"] < 70:
            self.report.add_recommendation("Improve response quality and relevance to career topics")
        
        return self.report
    
    def _analyze_response_quality(self, message: str, reply: str) -> dict:
        """Analyze the quality of a chatbot response"""
        score = 100
        
        # Check response length
        if len(reply) < 20:
            score -= 30  # Too short
        elif len(reply) > 1000:
            score -= 10  # Possibly too verbose
        
        # Check for career-related keywords
        career_keywords = [
            "career", "job", "skill", "education", "certification", 
            "industry", "profession", "role", "experience", "training",
            "development", "path", "opportunity", "salary", "work"
        ]
        
        career_keyword_count = sum(1 for keyword in career_keywords if keyword.lower() in reply.lower())
        career_relevant = career_keyword_count > 0
        
        if not career_relevant:
            score -= 40
        
        # Check if response is relevant to the question
        message_words = set(message.lower().split())
        reply_words = set(reply.lower().split())
        overlap = len(message_words & reply_words)
        
        relevance = "high" if overlap >= 3 else "medium" if overlap >= 1 else "low"
        if relevance == "low":
            score -= 20
        
        # Check for completeness (has proper sentences, punctuation)
        has_punctuation = any(char in reply for char in ['.', '!', '?'])
        if not has_punctuation:
            score -= 15
        
        completeness = "complete" if has_punctuation and len(reply) > 50 else "partial"
        
        return {
            "score": max(0, score),
            "relevance": relevance,
            "completeness": completeness,
            "career_relevant": career_relevant,
            "length": len(reply)
        }
    
    def _check_career_focus(self) -> bool:
        """Check if the conversation stayed focused on career topics"""
        career_focused_count = 0
        
        for step in self.report.test_steps:
            if "quality_score" in step.metadata:
                if step.metadata.get("quality_score", 0) >= 60:
                    career_focused_count += 1
        
        return career_focused_count / len(self.report.test_steps) >= 0.7 if self.report.test_steps else False


# Standalone test execution
if __name__ == "__main__":
    from diagnostic_framework import TestRunner
    
    print("Starting Career Chatbot AI Diagnostic Test...")
    
    runner = TestRunner(output_dir="logs")
    test = ChatbotTest()
    report = runner.run_test(test, verbose=True)
    
    print(f"\n{'='*70}")
    print(f"Test completed with status: {report.status.value}")
    print(f"Final score: {report.score:.1f}/100")
    print(f"{'='*70}\n")

