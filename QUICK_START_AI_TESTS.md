# Quick Start - AI Diagnostic Tests

## Prerequisites

```bash
# 1. Ensure Flask server is running
cd Backend
python app.py

# Server should be running on http://localhost:5000
```

## Run Tests (New Terminal)

```bash
# 2. Run all AI diagnostic tests
cd Backend
python run_ai_tests.py
```

## Expected Output

```
======================================================================
  AI DIAGNOSTIC TEST SUITE
  Total Tests: 3
======================================================================

Running: Career Suggester AI Test
======================================================================
✅ Status: PASS
📊 Score: 95.0/100
⏱️  Duration: 3.45s

Running: Career Chatbot AI Test
======================================================================
✅ Status: PASS
📊 Score: 88.5/100
⏱️  Duration: 2.1s

Running: Course Recommender AI Test
======================================================================
✅ Status: PASS
📊 Score: 92.0/100
⏱️  Duration: 1.8s

######################################################################
  FINAL SUMMARY
######################################################################
Total Tests: 3
✅ Passed: 3
❌ Failed: 0
⚠️  Warnings: 0
📊 Average Score: 91.8/100
⏱️  Total Duration: 7.35s
📁 All reports saved to: logs/
######################################################################
```

## View Reports

```bash
# List all test reports
python tests/report_viewer.py --list

# View specific report details
python tests/report_viewer.py --view career_suggester_2025-01-27_14-30-15

# Show test statistics
python tests/report_viewer.py --stats
```

## Check Reports via Web API

```bash
# Get all reports
curl http://localhost:5000/api/tests/reports

# Get statistics
curl http://localhost:5000/api/tests/statistics

# Get specific report
curl http://localhost:5000/api/tests/reports/<test_id>
```

## Command Options

```bash
# Verbose output (shows all test steps)
python run_ai_tests.py --verbose

# Run specific test only
python run_ai_tests.py --test chatbot

# Save to custom directory
python run_ai_tests.py --output results/

# Custom API URL
python run_ai_tests.py --url http://localhost:8000
```

## Report Location

All reports are saved as JSON files in:
```
Backend/logs/ai_diagnostic_*.json
```

## Understanding Results

- **PASS** ✅ = All checks passed
- **WARNING** ⚠️ = Minor issues found
- **FAIL** ❌ = Critical problems detected
- **Score 90-100** = Excellent
- **Score 70-89** = Good
- **Score 50-69** = Needs improvement
- **Score 0-49** = Major issues

## Troubleshooting

**Connection Error?**
→ Make sure Flask server is running: `python app.py`

**Import Error?**
→ Install dependencies: `pip install -r requirements.txt`

**No Reports?**
→ Run tests first: `python run_ai_tests.py`

## Full Documentation

See `Backend/AI_DIAGNOSTIC_SYSTEM.md` for complete documentation.

