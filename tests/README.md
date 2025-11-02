# AI Diagnostic Tests

Comprehensive testing framework for AI features with detailed diagnostic reporting.

## Quick Start

### 1. Run All Tests
```bash
cd Backend
python run_ai_tests.py
```

### 2. Run Specific Test
```bash
# Career Suggester
python run_ai_tests.py --test career_suggester

# Chatbot
python run_ai_tests.py --test chatbot

# Course Recommender
python run_ai_tests.py --test course_recommender
```

### 3. View Reports
```bash
# List all reports
python tests/report_viewer.py --list

# View specific report
python tests/report_viewer.py --view <test_id>

# Show statistics
python tests/report_viewer.py --stats
```

## Test Files

- `diagnostic_framework.py` - Base framework classes
- `test_career_suggester.py` - Career suggester AI tests
- `test_chatbot.py` - Chatbot AI tests
- `test_course_recommender.py` - Course recommender AI tests
- `report_viewer.py` - CLI tool for viewing reports

## Output

Reports are saved to `Backend/logs/` as JSON files:
- `ai_diagnostic_career_suggester_YYYY-MM-DD_HH-MM-SS.json`
- `ai_diagnostic_chatbot_YYYY-MM-DD_HH-MM-SS.json`
- `ai_diagnostic_course_recommender_YYYY-MM-DD_HH-MM-SS.json`

## Web API

Access reports via HTTP:
- `GET /api/tests/reports` - List all reports
- `GET /api/tests/reports/<test_id>` - Get specific report
- `GET /api/tests/statistics` - Get statistics

## Documentation

See `Backend/AI_DIAGNOSTIC_SYSTEM.md` for complete documentation.

