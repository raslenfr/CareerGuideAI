"""
AI Diagnostic Testing Framework - Base Classes and Utilities
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum


class TestStatus(Enum):
    """Test status enumeration"""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


class TestStep:
    """Represents a single test step with detailed information"""
    
    def __init__(self, step_number: int, action: str):
        self.step = step_number
        self.action = action
        self.expected = ""
        self.actual = ""
        self.status = TestStatus.PASS
        self.timestamp = datetime.now().isoformat()
        self.duration_ms = 0
        self.error = None
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary"""
        return {
            "step": self.step,
            "action": self.action,
            "expected": self.expected,
            "actual": self.actual,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "duration_ms": self.duration_ms,
            "error": self.error,
            "metadata": self.metadata
        }


class DiagnosticReport:
    """Comprehensive diagnostic report for AI testing"""
    
    def __init__(self, test_name: str, test_type: str):
        self.test_id = f"{test_type}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        self.timestamp = datetime.now().isoformat()
        self.test_name = test_name
        self.test_type = test_type
        self.status = TestStatus.PASS
        self.score = 100
        self.duration_seconds = 0
        self.start_time = time.time()
        
        # Summary data
        self.summary = {}
        
        # Detailed test steps
        self.test_steps: List[TestStep] = []
        
        # AI analysis
        self.ai_analysis = {}
        
        # Issues found
        self.issues = []
        
        # Recommendations
        self.recommendations = []
        
        # Metadata
        self.metadata = {
            "api_calls": 0,
            "tokens_used": 0,
            "errors_count": 0,
            "warnings_count": 0
        }
    
    def add_step(self, step: TestStep):
        """Add a test step to the report"""
        self.test_steps.append(step)
        
        # Update metadata based on step status
        if step.status == TestStatus.ERROR or step.status == TestStatus.FAIL:
            self.metadata["errors_count"] += 1
            self.status = TestStatus.FAIL
        elif step.status == TestStatus.WARNING:
            self.metadata["warnings_count"] += 1
    
    def add_issue(self, severity: str, description: str, details: str = ""):
        """Add an issue to the report"""
        self.issues.append({
            "severity": severity,
            "description": description,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_recommendation(self, recommendation: str):
        """Add a recommendation to the report"""
        self.recommendations.append(recommendation)
    
    def calculate_score(self):
        """Calculate overall test score based on results"""
        if not self.test_steps:
            return 0
        
        passed = sum(1 for step in self.test_steps if step.status == TestStatus.PASS)
        total = len(self.test_steps)
        
        base_score = (passed / total) * 100 if total > 0 else 0
        
        # Deduct points for errors and warnings
        error_penalty = self.metadata["errors_count"] * 10
        warning_penalty = self.metadata["warnings_count"] * 5
        
        self.score = max(0, base_score - error_penalty - warning_penalty)
        return self.score
    
    def finalize(self):
        """Finalize the report by calculating duration and score"""
        self.duration_seconds = round(time.time() - self.start_time, 2)
        self.calculate_score()
        
        # Determine overall status
        if self.metadata["errors_count"] > 0:
            self.status = TestStatus.FAIL
        elif self.metadata["warnings_count"] > 0:
            self.status = TestStatus.WARNING
        else:
            self.status = TestStatus.PASS
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary"""
        return {
            "test_id": self.test_id,
            "timestamp": self.timestamp,
            "test_name": self.test_name,
            "test_type": self.test_type,
            "status": self.status.value,
            "score": round(self.score, 2),
            "duration_seconds": self.duration_seconds,
            "summary": self.summary,
            "test_steps": [step.to_dict() for step in self.test_steps],
            "ai_analysis": self.ai_analysis,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "metadata": self.metadata
        }
    
    def save_to_file(self, directory: str = "logs"):
        """Save report to JSON file"""
        os.makedirs(directory, exist_ok=True)
        
        filename = f"ai_diagnostic_{self.test_id}.json"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        
        return filepath


class AITestCase:
    """Base class for AI test cases"""
    
    def __init__(self, test_name: str, test_type: str):
        self.test_name = test_name
        self.test_type = test_type
        self.report = DiagnosticReport(test_name, test_type)
        self.step_counter = 0
    
    def create_step(self, action: str) -> TestStep:
        """Create a new test step"""
        self.step_counter += 1
        return TestStep(self.step_counter, action)
    
    def run(self) -> DiagnosticReport:
        """Run the test (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement run() method")
    
    def cleanup(self):
        """Cleanup after test (to be implemented by subclasses if needed)"""
        pass


class TestRunner:
    """Test runner that executes AI diagnostic tests"""
    
    def __init__(self, output_dir: str = "logs"):
        self.output_dir = output_dir
        self.reports: List[DiagnosticReport] = []
    
    def run_test(self, test_case: AITestCase, verbose: bool = False) -> DiagnosticReport:
        """Run a single test case"""
        print(f"\n{'='*70}")
        print(f"Running: {test_case.test_name}")
        print(f"{'='*70}\n")
        
        try:
            report = test_case.run()
            report.finalize()
            self.reports.append(report)
            
            if verbose:
                self._print_report(report)
            else:
                self._print_summary(report)
            
            # Save report
            filepath = report.save_to_file(self.output_dir)
            print(f"\n[REPORT] Report saved to: {filepath}")
            
            return report
            
        except Exception as e:
            print(f"\n[FAIL] Test execution failed: {str(e)}")
            test_case.report.add_issue("CRITICAL", f"Test execution error: {str(e)}", "")
            test_case.report.status = TestStatus.ERROR
            test_case.report.finalize()
            return test_case.report
        finally:
            test_case.cleanup()
    
    def run_all_tests(self, test_cases: List[AITestCase], verbose: bool = False):
        """Run all test cases"""
        print(f"\n{'#'*70}")
        print(f"  AI DIAGNOSTIC TEST SUITE")
        print(f"  Total Tests: {len(test_cases)}")
        print(f"{'#'*70}")
        
        for test_case in test_cases:
            self.run_test(test_case, verbose)
        
        self._print_final_summary()
    
    def _print_summary(self, report: DiagnosticReport):
        """Print test summary"""
        status_symbol = "[PASS]" if report.status == TestStatus.PASS else "[FAIL]" if report.status == TestStatus.FAIL else "[WARN]"
        
        print(f"{status_symbol} Status: {report.status.value}")
        print(f"[SCORE] Score: {report.score:.1f}/100")
        print(f"[TIME] Duration: {report.duration_seconds}s")
        print(f"[STEPS] Steps: {len(report.test_steps)} executed")
        
        if report.metadata["errors_count"] > 0:
            print(f"[ERROR] Errors: {report.metadata['errors_count']}")
        if report.metadata["warnings_count"] > 0:
            print(f"[WARN] Warnings: {report.metadata['warnings_count']}")
    
    def _print_report(self, report: DiagnosticReport):
        """Print detailed report"""
        self._print_summary(report)
        
        print(f"\n[DETAILS] Detailed Steps:")
        for step in report.test_steps:
            status_symbol = "[OK]" if step.status == TestStatus.PASS else "[X]" if step.status == TestStatus.FAIL else "[!]"
            print(f"  {status_symbol} Step {step.step}: {step.action}")
            if step.status != TestStatus.PASS:
                print(f"     Expected: {step.expected}")
                print(f"     Actual: {step.actual}")
        
        if report.issues:
            print(f"\n[ISSUES] Issues Found:")
            for issue in report.issues:
                print(f"  - [{issue['severity']}] {issue['description']}")
        
        if report.recommendations:
            print(f"\n[TIPS] Recommendations:")
            for rec in report.recommendations:
                print(f"  - {rec}")
    
    def _print_final_summary(self):
        """Print final summary of all tests"""
        print(f"\n{'#'*70}")
        print(f"  FINAL SUMMARY")
        print(f"{'#'*70}\n")
        
        total = len(self.reports)
        passed = sum(1 for r in self.reports if r.status == TestStatus.PASS)
        failed = sum(1 for r in self.reports if r.status == TestStatus.FAIL)
        warnings = sum(1 for r in self.reports if r.status == TestStatus.WARNING)
        
        avg_score = sum(r.score for r in self.reports) / total if total > 0 else 0
        total_duration = sum(r.duration_seconds for r in self.reports)
        
        print(f"Total Tests: {total}")
        print(f"[PASS] Passed: {passed}")
        print(f"[FAIL] Failed: {failed}")
        print(f"[WARN] Warnings: {warnings}")
        print(f"[SCORE] Average Score: {avg_score:.1f}/100")
        print(f"[TIME] Total Duration: {total_duration:.2f}s")
        print(f"\n[SAVE] All reports saved to: {self.output_dir}/")
        print(f"{'#'*70}\n")

