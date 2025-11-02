# AI Diagnostic Testing System

## Overview

Comprehensive diagnostic testing framework for AI features in the Career Guidance application. Provides detailed, step-by-step analysis of AI behavior with extensive reporting and logging.

---

## Features

✅ **Detailed Test Reports** - Step-by-step analysis of what the AI did  
✅ **Quality Assessment** - Evaluate response relevance, completeness, and accuracy  
✅ **Performance Metrics** - Response times, API calls, token usage  
✅ **Issue Detection** - Identify errors, warnings, and inconsistencies  
✅ **Recommendations** - Actionable suggestions for improvement  
✅ **JSON Logging** - All reports saved as structured JSON files  
✅ **CLI Interface** - Easy command-line test execution  
✅ **Web API** - View reports via HTTP endpoints  
✅ **Statistics** - Aggregate metrics across all tests  

---

## Components

### 1. Diagnostic Framework (`tests/diagnostic_framework.py`)

Base classes for building AI diagnostic tests:

- **`TestStatus`** - Enumeration for test results (PASS, FAIL, WARNING, ERROR, SKIPPED)
- **`TestStep`** - Represents a single test step with timing and metadata
- **`DiagnosticReport`** - Comprehensive report with summary, steps, analysis, issues, and recommendations
- **`AITestCase`** - Base class for creating test cases
- **`TestRunner`** - Executes tests and generates reports

### 2. Test Suites

#### Career Suggester Test (`tests/test_career_suggester.py`)
Tests the 11-question career path suggestion system:
- Validates all 11 questions are asked
- Checks each answer is processed correctly
- Verifies career suggestions are generated
- Analyzes suggestion quality and relevance
- Validates suggestions match user profile

#### Chatbot Test (`tests/test_chatbot.py`)
Tests the conversational career guidance AI:
- Sends multiple test messages
- Analyzes response quality and relevance
- Checks career-topic focus
- Measures response time
- Validates conversation coherence

#### Course Recommender Test (`tests/test_course_recommender.py`)
Tests the course recommendation system:
- Multiple search scenarios
- Validates course results
- Checks relevance to keywords
- Verifies required fields (title, provider, URL)
- Measures recommendation quality

### 3. Test Runner (`run_ai_tests.py`)

CLI tool for executing tests:

```bash
# Run all tests
python run_ai_tests.py

# Run specific test
python run_ai_tests.py --test career_suggester

# Verbose output
python run_ai_tests.py --verbose

# Custom output directory
python run_ai_tests.py --output results/

# Custom API URL
python run_ai_tests.py --url http://localhost:8000
```

### 4. Report Viewer (`tests/report_viewer.py`)

Utility for viewing and analyzing saved reports:

```bash
# List all reports
python tests/report_viewer.py --list

# View specific report
python tests/report_viewer.py --view career_suggester_2025-01-27_14-30-15

# Show statistics
python tests/report_viewer.py --stats

# Filter by type
python tests/report_viewer.py --list --type chatbot

# Filter by status
python tests/report_viewer.py --list --status FAIL
```

### 5. Web API (`blueprints/test_reports_bp.py`)

HTTP endpoints for viewing reports:

- **`GET /api/tests/reports`** - List all reports (with filtering)
- **`GET /api/tests/reports/<test_id>`** - Get specific report
- **`GET /api/tests/statistics`** - Get aggregate statistics
- **`GET /api/tests/health`** - Health check

---

## Report Structure

Each diagnostic report includes:

```json
{
  "test_id": "career_suggester_2025-01-27_14-30-15",
  "timestamp": "2025-01-27T14:30:15",
  "test_name": "Career Suggester AI Test",
  "test_type": "career_suggester",
  "status": "PASS",
  "score": 95,
  "duration_seconds": 3.45,
  
  "summary": {
    "total_questions": 11,
    "questions_asked": 11,
    "answers_provided": 11,
    "suggestions_generated": 3,
    "errors": 0,
    "warnings": 1
  },
  
  "test_steps": [
    {
      "step": 1,
      "action": "Initialize Career Suggester",
      "expected": "Receive first question",
      "actual": "Received question: What subjects...",
      "status": "PASS",
      "timestamp": "2025-01-27T14:30:15.123",
      "duration_ms": 234,
      "error": null,
      "metadata": {}
    }
  ],
  
  "ai_analysis": {
    "all_questions_completed": true,
    "suggestion_quality": "high",
    "reasoning_logical": true,
    "response_time_avg_ms": 456
  },
  
  "issues": [
    {
      "severity": "WARNING",
      "description": "Response time high for question 7",
      "details": "Took 1200ms (expected < 1000ms)",
      "timestamp": "2025-01-27T14:30:18"
    }
  ],
  
  "recommendations": [
    "Optimize response generation for question 7",
    "Consider caching common responses"
  ],
  
  "metadata": {
    "api_calls": 12,
    "tokens_used": 0,
    "errors_count": 0,
    "warnings_count": 1
  }
}
```

---

## Usage Examples

### Running Tests

#### 1. Run All Tests (Recommended for CI/CD)
```bash
cd Backend
python run_ai_tests.py
```

Output:
```
======================================================================
  AI DIAGNOSTIC TEST SUITE
  Comprehensive AI Behavior Analysis
======================================================================

Running: Career Suggester AI Test
======================================================================

🧪 Testing Career Suggester AI...
✅ Status: PASS
📊 Score: 95.0/100
⏱️  Duration: 3.45s
📈 Steps: 13 executed

📄 Report saved to: logs/ai_diagnostic_career_suggester_2025-01-27_14-30-15.json

Running: Career Chatbot AI Test
======================================================================
...

######################################################################
  FINAL SUMMARY
######################################################################

Total Tests: 3
✅ Passed: 2
❌ Failed: 1
⚠️  Warnings: 0
📊 Average Score: 85.3/100
⏱️  Total Duration: 8.75s

📁 All reports saved to: logs/
######################################################################
```

#### 2. Run Specific Test with Verbose Output
```bash
python run_ai_tests.py --test chatbot --verbose
```

#### 3. Save to Custom Directory
```bash
python run_ai_tests.py --output test_results/
```

### Viewing Reports

#### 1. List Recent Reports
```bash
python tests/report_viewer.py --list --limit 10
```

#### 2. View Specific Report
```bash
python tests/report_viewer.py --view career_suggester_2025-01-27_14-30-15
```

#### 3. Show Statistics
```bash
python tests/report_viewer.py --stats
```

Output:
```
======================================================================
  Test Statistics
======================================================================

📊 Total Tests: 15
✅ Passed: 12
❌ Failed: 2
⚠️  Warnings: 1
📈 Pass Rate: 80.0%
📊 Average Score: 82.5/100
⏱️  Average Duration: 4.2s
🕐 Latest Test: 2025-01-27T14:30:15

======================================================================
```

### Web API Usage

#### 1. List All Reports
```bash
curl http://localhost:5000/api/tests/reports
```

Response:
```json
{
  "success": true,
  "reports": [
    {
      "test_id": "career_suggester_2025-01-27_14-30-15",
      "test_name": "Career Suggester AI Test",
      "status": "PASS",
      "score": 95,
      "timestamp": "2025-01-27T14:30:15"
    }
  ],
  "total": 1
}
```

#### 2. Get Specific Report
```bash
curl http://localhost:5000/api/tests/reports/career_suggester_2025-01-27_14-30-15
```

#### 3. Get Statistics
```bash
curl http://localhost:5000/api/tests/statistics
```

#### 4. Filter Reports
```bash
# By test type
curl http://localhost:5000/api/tests/reports?type=chatbot

# By status
curl http://localhost:5000/api/tests/reports?status=FAIL

# Limit results
curl http://localhost:5000/api/tests/reports?limit=10
```

---

## Test Scenarios

### Career Suggester Test Scenarios

**Input Profile**: Tech-focused user with CS degree
- Education: Bachelor's in Computer Science
- Skills: Python, problem-solving, analytical thinking
- Interests: Technical challenges, algorithms, data
- Career preference: Technical role with research

**Expected Outcomes**:
- All 11 questions asked in sequence
- Career suggestions include tech roles (Software Engineer, Data Scientist, etc.)
- Suggestions have detailed reasons
- Total time < 10 seconds

### Chatbot Test Scenarios

**Test Messages**:
1. "Hello, I need career advice"
2. "What skills are important for data science?"
3. "How can I transition from marketing to data analytics?"
4. "What certifications for cloud computing?"
5. "Career opportunities in AI"

**Expected Outcomes**:
- All messages receive responses
- Responses are career-focused
- Average response time < 3 seconds
- Responses are complete and relevant

### Course Recommender Test Scenarios

**Test Queries**:
1. "Python programming" + Tunisia
2. "Data science machine learning" + Tunisia
3. "Web development React" + Tunisia

**Expected Outcomes**:
- At least 3 courses per query
- Courses have title, provider, URL
- Courses match keywords
- Response time < 3 seconds

---

## Interpreting Results

### Test Status

- **PASS** ✅ - All checks passed, no issues
- **WARNING** ⚠️ - Passed but with minor issues
- **FAIL** ❌ - Critical issues found
- **ERROR** ❌ - Test execution failed

### Scores

- **90-100** - Excellent performance
- **70-89** - Good, minor improvements needed
- **50-69** - Fair, several issues to address
- **0-49** - Poor, major problems detected

### Common Issues

**Career Suggester**:
- Missing questions in sequence
- Suggestions not matching profile
- Short/generic reasons
- Incorrect suggestion count

**Chatbot**:
- Off-topic responses
- Incomplete answers
- Slow response time
- Non-career-related content

**Course Recommender**:
- No courses found
- Missing required fields
- Irrelevant courses
- Wrong location

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: AI Diagnostic Tests

on: [push, pull_request]

jobs:
  ai-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          cd Backend
          pip install -r requirements.txt
      
      - name: Start Flask server
        run: |
          cd Backend
          python app.py &
          sleep 10
      
      - name: Run AI diagnostic tests
        run: |
          cd Backend
          python run_ai_tests.py --output test_results/
      
      - name: Upload test reports
        uses: actions/upload-artifact@v2
        with:
          name: ai-test-reports
          path: Backend/test_results/
```

---

## Troubleshooting

### Test Connection Errors

**Problem**: `Connection refused` or `Network error`

**Solution**:
```bash
# Ensure Flask server is running
cd Backend
python app.py

# In another terminal, run tests
python run_ai_tests.py
```

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Run from Backend directory
cd Backend
python run_ai_tests.py
```

### No Reports Found

**Problem**: Report viewer shows "No reports found"

**Solution**:
```bash
# Check logs directory exists
ls -la logs/

# Run tests first to generate reports
python run_ai_tests.py

# View reports
python tests/report_viewer.py --list
```

---

## File Structure

```
Backend/
├── run_ai_tests.py          # Main test runner CLI
├── logs/                     # Test reports saved here
│   └── ai_diagnostic_*.json
├── tests/
│   ├── __init__.py
│   ├── diagnostic_framework.py    # Base framework
│   ├── test_career_suggester.py   # Career suggester tests
│   ├── test_chatbot.py            # Chatbot tests
│   ├── test_course_recommender.py # Course recommender tests
│   └── report_viewer.py           # Report viewing utility
└── blueprints/
    └── test_reports_bp.py         # Web API for reports
```

---

## Best Practices

1. **Run tests regularly** - Daily or before deployments
2. **Review reports** - Check for patterns in failures
3. **Track scores** - Monitor trends over time
4. **Fix warnings** - Don't ignore minor issues
5. **Update tests** - As AI features evolve
6. **Archive reports** - Keep historical data
7. **Automate** - Integrate with CI/CD pipeline

---

## Future Enhancements

- [ ] Performance benchmarking over time
- [ ] Automated regression detection
- [ ] Email notifications for failures
- [ ] Web dashboard for visualization
- [ ] Compare reports side-by-side
- [ ] Export reports as PDF
- [ ] Test scheduling/cron jobs
- [ ] Load testing capabilities

---

## Support

For issues or questions:
1. Check logs in `Backend/logs/`
2. Review test reports for details
3. Check Flask server logs
4. Verify API endpoints are accessible

---

**Version**: 1.0.0  
**Last Updated**: January 27, 2025  
**Status**: Production Ready ✅

