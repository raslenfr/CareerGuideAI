"""
Report Viewer Utility
View and analyze AI diagnostic test reports
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


class ReportViewer:
    """Utility for viewing and analyzing test reports"""
    
    def __init__(self, logs_dir: str = "logs"):
        self.logs_dir = logs_dir
    
    def list_reports(self, test_type: str = None, status: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """List all test reports with optional filtering"""
        if not os.path.exists(self.logs_dir):
            return []
        
        reports = []
        
        for filename in os.listdir(self.logs_dir):
            if filename.startswith("ai_diagnostic_") and filename.endswith(".json"):
                filepath = os.path.join(self.logs_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)
                    
                    # Apply filters
                    if test_type and report_data.get("test_type") != test_type:
                        continue
                    
                    if status and report_data.get("status") != status:
                        continue
                    
                    reports.append({
                        "filename": filename,
                        "test_id": report_data.get("test_id"),
                        "test_name": report_data.get("test_name"),
                        "test_type": report_data.get("test_type"),
                        "status": report_data.get("status"),
                        "score": report_data.get("score"),
                        "timestamp": report_data.get("timestamp"),
                        "duration": report_data.get("duration_seconds"),
                        "errors": report_data.get("metadata", {}).get("errors_count", 0),
                        "warnings": report_data.get("metadata", {}).get("warnings_count", 0)
                    })
                
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        # Sort by timestamp (newest first)
        reports.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return reports[:limit]
    
    def get_report(self, test_id: str) -> Dict[str, Any]:
        """Get a specific report by test_id"""
        for filename in os.listdir(self.logs_dir):
            if test_id in filename:
                filepath = os.path.join(self.logs_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        return None
    
    def print_report_summary(self, test_id: str = None, filename: str = None):
        """Print a formatted summary of a report"""
        if filename:
            filepath = os.path.join(self.logs_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                report = json.load(f)
        elif test_id:
            report = self.get_report(test_id)
        else:
            print("Error: Must provide test_id or filename")
            return
        
        if not report:
            print("Report not found")
            return
        
        # Print header
        print("\n" + "="*70)
        print(f"  {report['test_name']}")
        print("="*70 + "\n")
        
        # Print summary
        status_symbol = "✅" if report['status'] == "PASS" else "❌" if report['status'] == "FAIL" else "⚠️"
        print(f"{status_symbol} Status: {report['status']}")
        print(f"📊 Score: {report['score']}/100")
        print(f"🕐 Timestamp: {report['timestamp']}")
        print(f"⏱️  Duration: {report['duration_seconds']}s")
        print(f"🔢 Test ID: {report['test_id']}")
        
        # Print test summary
        if report.get('summary'):
            print("\n📋 Summary:")
            for key, value in report['summary'].items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Print AI analysis
        if report.get('ai_analysis'):
            print("\n🤖 AI Analysis:")
            for key, value in report['ai_analysis'].items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Print issues
        if report.get('issues'):
            print(f"\n⚠️  Issues Found ({len(report['issues'])}):")
            for issue in report['issues']:
                print(f"  [{issue['severity']}] {issue['description']}")
                if issue.get('details'):
                    print(f"      Details: {issue['details'][:100]}")
        
        # Print recommendations
        if report.get('recommendations'):
            print(f"\n💡 Recommendations ({len(report['recommendations'])}):")
            for rec in report['recommendations']:
                print(f"  • {rec}")
        
        # Print metadata
        if report.get('metadata'):
            print("\n📊 Metadata:")
            for key, value in report['metadata'].items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print("\n" + "="*70 + "\n")
    
    def print_report_list(self, test_type: str = None, status: str = None, limit: int = 20):
        """Print a list of reports"""
        reports = self.list_reports(test_type, status, limit)
        
        if not reports:
            print("No reports found")
            return
        
        print("\n" + "="*70)
        print(f"  Test Reports ({len(reports)})")
        print("="*70 + "\n")
        
        for i, report in enumerate(reports, 1):
            status_symbol = "✅" if report['status'] == "PASS" else "❌" if report['status'] == "FAIL" else "⚠️"
            
            print(f"{i}. {status_symbol} {report['test_name']}")
            print(f"   ID: {report['test_id']}")
            print(f"   Score: {report['score']}/100 | Duration: {report['duration']}s")
            print(f"   Timestamp: {report['timestamp']}")
            if report['errors'] > 0 or report['warnings'] > 0:
                print(f"   Issues: {report['errors']} errors, {report['warnings']} warnings")
            print()
        
        print("="*70 + "\n")
    
    def get_statistics(self, test_type: str = None) -> Dict[str, Any]:
        """Get statistics across all reports"""
        reports = self.list_reports(test_type=test_type, limit=1000)
        
        if not reports:
            return {}
        
        total = len(reports)
        passed = sum(1 for r in reports if r['status'] == "PASS")
        failed = sum(1 for r in reports if r['status'] == "FAIL")
        warnings = sum(1 for r in reports if r['status'] == "WARNING")
        
        avg_score = sum(r['score'] for r in reports) / total if total > 0 else 0
        avg_duration = sum(r['duration'] for r in reports) / total if total > 0 else 0
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "avg_score": round(avg_score, 2),
            "avg_duration": round(avg_duration, 2),
            "latest_test": reports[0]['timestamp'] if reports else None
        }
    
    def print_statistics(self, test_type: str = None):
        """Print statistics"""
        stats = self.get_statistics(test_type)
        
        if not stats:
            print("No statistics available")
            return
        
        print("\n" + "="*70)
        print(f"  Test Statistics{f' - {test_type}' if test_type else ''}")
        print("="*70 + "\n")
        
        print(f"📊 Total Tests: {stats['total_tests']}")
        print(f"✅ Passed: {stats['passed']}")
        print(f"❌ Failed: {stats['failed']}")
        print(f"⚠️  Warnings: {stats['warnings']}")
        print(f"📈 Pass Rate: {stats['pass_rate']:.1f}%")
        print(f"📊 Average Score: {stats['avg_score']}/100")
        print(f"⏱️  Average Duration: {stats['avg_duration']}s")
        
        if stats['latest_test']:
            print(f"🕐 Latest Test: {stats['latest_test']}")
        
        print("\n" + "="*70 + "\n")


# CLI interface
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="View AI diagnostic test reports")
    parser.add_argument('--list', action='store_true', help='List all reports')
    parser.add_argument('--view', type=str, help='View specific report by test_id')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--type', type=str, choices=['career_suggester', 'chatbot', 'course_recommender'], help='Filter by test type')
    parser.add_argument('--status', type=str, choices=['PASS', 'FAIL', 'WARNING'], help='Filter by status')
    parser.add_argument('--limit', type=int, default=20, help='Limit number of reports (default: 20)')
    parser.add_argument('--logs-dir', type=str, default='logs', help='Logs directory (default: logs/)')
    
    args = parser.parse_args()
    
    viewer = ReportViewer(logs_dir=args.logs_dir)
    
    if args.list:
        viewer.print_report_list(test_type=args.type, status=args.status, limit=args.limit)
    elif args.view:
        viewer.print_report_summary(test_id=args.view)
    elif args.stats:
        viewer.print_statistics(test_type=args.type)
    else:
        # Default: show list
        viewer.print_report_list(limit=10)


if __name__ == "__main__":
    main()

