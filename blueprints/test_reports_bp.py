"""
Test Reports API Blueprint
Web UI endpoint for viewing AI diagnostic test reports
"""

from flask import Blueprint, jsonify, request
import os
import json
import sys

# Add tests directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests'))

from tests.report_viewer import ReportViewer
import logging

log = logging.getLogger(__name__)

test_reports_bp = Blueprint('test_reports_bp', __name__, url_prefix='/api/tests')


@test_reports_bp.route('/reports', methods=['GET'])
def get_reports():
    """Get list of all test reports with optional filtering"""
    try:
        test_type = request.args.get('type')
        status = request.args.get('status')
        limit = int(request.args.get('limit', 50))
        
        viewer = ReportViewer(logs_dir='logs')
        reports = viewer.list_reports(test_type=test_type, status=status, limit=limit)
        
        return jsonify({
            "success": True,
            "reports": reports,
            "total": len(reports)
        }), 200
    
    except Exception as e:
        log.error(f"Error fetching reports: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@test_reports_bp.route('/reports/<test_id>', methods=['GET'])
def get_report(test_id):
    """Get a specific test report"""
    try:
        viewer = ReportViewer(logs_dir='logs')
        report = viewer.get_report(test_id)
        
        if not report:
            return jsonify({
                "success": False,
                "error": "Report not found"
            }), 404
        
        return jsonify({
            "success": True,
            "report": report
        }), 200
    
    except Exception as e:
        log.error(f"Error fetching report {test_id}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@test_reports_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get statistics across all test reports"""
    try:
        test_type = request.args.get('type')
        
        viewer = ReportViewer(logs_dir='logs')
        stats = viewer.get_statistics(test_type=test_type)
        
        return jsonify({
            "success": True,
            "statistics": stats
        }), 200
    
    except Exception as e:
        log.error(f"Error fetching statistics: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@test_reports_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "message": "Test reports API is running",
        "endpoints": [
            "GET /api/tests/reports - List all reports",
            "GET /api/tests/reports/<test_id> - Get specific report",
            "GET /api/tests/statistics - Get test statistics"
        ]
    }), 200

