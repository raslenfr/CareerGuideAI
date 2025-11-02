"""
Course Recommender AI Diagnostic Test Suite
Tests the course recommendation system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
from diagnostic_framework import AITestCase, DiagnosticReport, TestStep, TestStatus


class CourseRecommenderTest(AITestCase):
    """Test suite for Course Recommender AI"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        super().__init__("Course Recommender AI Test", "course_recommender")
        self.base_url = base_url
        self.api_url = f"{base_url}/api/recommender"
        self.test_scenarios = [
            {"keywords": "Python programming", "location": "Tunisia"},
            {"keywords": "Data science machine learning", "location": "Tunisia"},
            {"keywords": "Web development React", "location": "Tunisia"},
        ]
    
    def run(self) -> DiagnosticReport:
        """Execute the Course Recommender AI test"""
        
        print("🧪 Testing Course Recommender AI...")
        
        total_courses_found = 0
        total_response_time = 0
        scenarios_passed = 0
        
        for i, scenario in enumerate(self.test_scenarios):
            # Step 1: Start recommendation
            step = self.create_step(f"Scenario {i+1}: Start recommendation for '{scenario['keywords']}'")
            step.expected = "Receive request ID and first survey question"
            start_time = time.time()
            
            try:
                response = requests.post(f"{self.api_url}/start", json=scenario)
                step.duration_ms = int((time.time() - start_time) * 1000)
                total_response_time += step.duration_ms
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success") and data.get("request_id"):
                        request_id = data["request_id"]
                        step.actual = f"Received request_id: {request_id[:20]}..."
                        step.status = TestStatus.PASS
                        step.metadata = {"request_id": request_id}
                    else:
                        step.actual = f"Failed: {data.get('error', 'Unknown error')}"
                        step.status = TestStatus.FAIL
                        self.report.add_issue("ERROR", f"Scenario {i+1}: Failed to start", str(data))
                        self.report.add_step(step)
                        continue
                else:
                    step.actual = f"HTTP {response.status_code}"
                    step.status = TestStatus.FAIL
                    self.report.add_issue("ERROR", f"Scenario {i+1}: API error", f"Status: {response.status_code}")
                    self.report.add_step(step)
                    continue
            
            except Exception as e:
                step.actual = f"Exception: {str(e)}"
                step.status = TestStatus.ERROR
                step.error = str(e)
                self.report.add_issue("CRITICAL", f"Scenario {i+1}: Connection error", str(e))
                self.report.add_step(step)
                continue
            
            self.report.add_step(step)
            self.report.metadata["api_calls"] += 1
            
            # Step 2: Submit survey answers
            request_id = step.metadata.get("request_id")
            if request_id:
                submit_step = self.create_step(f"Scenario {i+1}: Submit survey answers")
                submit_step.expected = "Receive course recommendations"
                start_time = time.time()
                
                try:
                    survey_answers = {
                        "experience_level": "intermediate",
                        "learning_style": "video",
                        "time_commitment": "5-10 hours/week"
                    }
                    
                    payload = {
                        "request_id": request_id,
                        "answers": survey_answers
                    }
                    
                    response = requests.post(f"{self.api_url}/submit", json=payload)
                    submit_step.duration_ms = int((time.time() - start_time) * 1000)
                    total_response_time += submit_step.duration_ms
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data.get("success") and data.get("recommendations"):
                            courses = data["recommendations"]
                            total_courses_found += len(courses)
                            
                            submit_step.actual = f"Received {len(courses)} course recommendations"
                            submit_step.status = TestStatus.PASS
                            submit_step.metadata = {
                                "courses": courses,
                                "keywords": scenario["keywords"]
                            }
                            
                            scenarios_passed += 1
                            
                            # Validate courses
                            self._validate_courses(courses, scenario["keywords"], i+1)
                        else:
                            submit_step.actual = f"Failed: {data.get('error', 'No recommendations')}"
                            submit_step.status = TestStatus.FAIL
                            self.report.add_issue("ERROR", f"Scenario {i+1}: No recommendations", str(data))
                    else:
                        submit_step.actual = f"HTTP {response.status_code}"
                        submit_step.status = TestStatus.FAIL
                        self.report.add_issue("ERROR", f"Scenario {i+1}: Submit failed", f"Status: {response.status_code}")
                
                except Exception as e:
                    submit_step.actual = f"Exception: {str(e)}"
                    submit_step.status = TestStatus.ERROR
                    submit_step.error = str(e)
                    self.report.add_issue("CRITICAL", f"Scenario {i+1}: Submit error", str(e))
                
                self.report.add_step(submit_step)
                self.report.metadata["api_calls"] += 1
        
        # Build summary
        self.report.summary = {
            "total_scenarios": len(self.test_scenarios),
            "scenarios_passed": scenarios_passed,
            "total_courses_found": total_courses_found,
            "avg_response_time_ms": int(total_response_time / (len(self.test_scenarios) * 2)) if self.test_scenarios else 0,
            "errors": self.report.metadata["errors_count"],
            "warnings": self.report.metadata["warnings_count"]
        }
        
        # AI Analysis
        self.report.ai_analysis = {
            "all_scenarios_completed": scenarios_passed == len(self.test_scenarios),
            "sufficient_recommendations": total_courses_found >= len(self.test_scenarios) * 3,
            "response_time_acceptable": self.report.summary["avg_response_time_ms"] < 3000,
            "success_rate": (scenarios_passed / len(self.test_scenarios) * 100) if self.test_scenarios else 0
        }
        
        # Add recommendations
        if total_courses_found < len(self.test_scenarios) * 3:
            self.report.add_recommendation("Increase the number of course recommendations per query")
        
        if self.report.summary["avg_response_time_ms"] > 2000:
            self.report.add_recommendation("Optimize course search and recommendation algorithm")
        
        return self.report
    
    def _validate_courses(self, courses: list, keywords: str, scenario_num: int):
        """Validate the quality and relevance of course recommendations"""
        step = self.create_step(f"Scenario {scenario_num}: Validate course recommendations")
        step.expected = "Courses relevant to search keywords"
        
        issues = []
        
        if len(courses) == 0:
            issues.append("No courses recommended")
            step.status = TestStatus.FAIL
        elif len(courses) < 3:
            issues.append(f"Only {len(courses)} courses recommended (expected at least 3)")
            step.status = TestStatus.WARNING
        
        # Check each course for required fields
        for i, course in enumerate(courses):
            if not course.get("title"):
                issues.append(f"Course {i+1}: Missing title")
                step.status = TestStatus.FAIL
            
            if not course.get("provider"):
                issues.append(f"Course {i+1}: Missing provider")
                step.status = TestStatus.WARNING
            
            if not course.get("url"):
                issues.append(f"Course {i+1}: Missing URL")
                step.status = TestStatus.WARNING
        
        # Check relevance to keywords
        keyword_list = keywords.lower().split()
        relevant_courses = 0
        
        for course in courses:
            title = course.get("title", "").lower()
            description = course.get("description", "").lower()
            
            if any(keyword in title or keyword in description for keyword in keyword_list):
                relevant_courses += 1
        
        relevance_ratio = relevant_courses / len(courses) if courses else 0
        
        if relevance_ratio < 0.5:
            issues.append(f"Low relevance: Only {relevant_courses}/{len(courses)} courses match keywords")
            step.status = TestStatus.WARNING
            self.report.add_recommendation(f"Improve keyword matching for '{keywords}'")
        
        if issues:
            step.actual = f"Issues found: {', '.join(issues)}"
            for issue in issues:
                self.report.add_issue("WARNING", f"Scenario {scenario_num}: Course validation", issue)
        else:
            step.actual = f"All {len(courses)} courses are valid and relevant"
            step.status = TestStatus.PASS
        
        self.report.add_step(step)


# Standalone test execution
if __name__ == "__main__":
    from diagnostic_framework import TestRunner
    
    print("Starting Course Recommender AI Diagnostic Test...")
    
    runner = TestRunner(output_dir="logs")
    test = CourseRecommenderTest()
    report = runner.run_test(test, verbose=True)
    
    print(f"\n{'='*70}")
    print(f"Test completed with status: {report.status.value}")
    print(f"Final score: {report.score:.1f}/100")
    print(f"{'='*70}\n")

