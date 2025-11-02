#!/usr/bin/env python3
"""
AI Diagnostic Test Runner
Runs comprehensive diagnostic tests on all AI features in the application
"""

import argparse
import sys
import os

# Add tests directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from tests.diagnostic_framework import TestRunner
from tests.test_career_suggester import CareerSuggesterTest
from tests.test_chatbot import ChatbotTest
from tests.test_course_recommender import CourseRecommenderTest


def main():
    parser = argparse.ArgumentParser(
        description="Run AI diagnostic tests with detailed reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python run_ai_tests.py
  
  # Run specific test
  python run_ai_tests.py --test career_suggester
  
  # Run with verbose output
  python run_ai_tests.py --verbose
  
  # Save reports to custom directory
  python run_ai_tests.py --output results/
  
  # Run specific test with verbose output
  python run_ai_tests.py --test chatbot --verbose
        """
    )
    
    parser.add_argument(
        '--test',
        choices=['career_suggester', 'chatbot', 'course_recommender', 'all'],
        default='all',
        help='Specific test to run (default: all)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed test output'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='logs',
        help='Output directory for test reports (default: logs/)'
    )
    
    parser.add_argument(
        '--url',
        default='http://localhost:5000',
        help='Base URL of the API server (default: http://localhost:5000)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("\n" + "="*70)
    print("  AI DIAGNOSTIC TEST SUITE")
    print("  Comprehensive AI Behavior Analysis")
    print("="*70 + "\n")
    
    # Initialize test runner
    runner = TestRunner(output_dir=args.output)
    
    # Determine which tests to run
    test_cases = []
    
    if args.test == 'all' or args.test == 'career_suggester':
        test_cases.append(CareerSuggesterTest(base_url=args.url))
    
    if args.test == 'all' or args.test == 'chatbot':
        test_cases.append(ChatbotTest(base_url=args.url))
    
    if args.test == 'all' or args.test == 'course_recommender':
        test_cases.append(CourseRecommenderTest(base_url=args.url))
    
    if not test_cases:
        print("❌ No tests selected")
        return 1
    
    # Run tests
    try:
        runner.run_all_tests(test_cases, verbose=args.verbose)
        
        # Determine exit code based on results
        all_passed = all(report.status.value == "PASS" for report in runner.reports)
        return 0 if all_passed else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\n❌ Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

