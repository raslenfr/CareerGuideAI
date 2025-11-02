# Frontend-Integrated AI Testing System

## 🎉 Overview

The AI testing system has been completely transformed from a backend-only CLI tool to a **frontend-integrated, real-time testing system** with automatic AI detection and manual control.

## ✨ Key Features

### ✅ **NO TIME LIMITS**
- Tests run indefinitely until you manually stop them
- No automatic timeouts or forced endings
- Test at your own pace

### ✅ **FRONTEND-INTEGRATED**
- Test Mode toggle in the header (visible on all pages)
- Real-time recording of AI interactions
- Visual status indicator showing current AI and interaction count
- Start/Stop controls always accessible

### ✅ **AUTOMATIC AI DETECTION**
- System automatically detects which AI you're testing based on the current page:
  - `/chatbot` → **Chatbot AI**
  - `/career-suggester` → **Career Suggester AI**
  - `/course-recommender` → **Course Recommender AI**
- No need to manually select AI type

### ✅ **FLEXIBLE TESTING**
- Test one AI at a time or switch between multiple AIs
- No enforced order or sequence
- Navigate freely between pages during testing
- Each AI interaction is logged separately with full context

### ✅ **MANUAL CONTROL**
- **Start Recording** button - begins logging all AI interactions
- **Stop Recording & Generate Report** button - stops logging and creates comprehensive report
- Full control over when to start/stop testing

---

## 🚀 How to Use

### **Step 1: Start the Backend Server**

```bash
cd Backend
python app.py
```

**Expected Output:**
```
✅ Flask server running on http://localhost:5000
✅ Database initialized
✅ LLM service ready
✅ All blueprints registered successfully
```

---

### **Step 2: Start the Frontend**

```bash
cd Frontend
npm run dev
```

**Expected Output:**
```
VITE v6.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

---

### **Step 3: Log In to the Application**

1. Open your browser to `http://localhost:5173`
2. Sign up or log in with your credentials
3. You'll see the dashboard

---

### **Step 4: Enable Test Mode**

In the header (top of the page), you'll see:
- **"Test: OFF"** button (gray)

Click it to enable test mode:
- Button turns green: **"Test: ON"**
- Test status indicator appears in the bottom-right corner

---

### **Step 5: Start Recording**

Once test mode is enabled, you'll see:
- **"Start"** button (green, with play icon)

Click **"Start"** to begin recording:
- Button changes to **"Stop (0)"** (red, with square icon)
- Status indicator shows: **"🔴 Recording [AI Name] (0)"**

---

### **Step 6: Test Your AI**

Navigate to any AI page and interact with it normally:

#### **Testing Chatbot AI:**
1. Go to `/chatbot` page
2. Status indicator updates: **"🔴 Recording Chatbot AI (0)"**
3. Send messages to the chatbot
4. Each interaction is automatically logged
5. Counter increments: **"Stop (1)"**, **"Stop (2)"**, etc.

#### **Testing Career Suggester AI:**
1. Go to `/career-suggester` page
2. Status indicator updates: **"🔴 Recording Career Suggester AI (X)"**
3. Answer the career assessment questions
4. Each answer is logged
5. Final suggestions are logged with full context

#### **Testing Course Recommender AI:**
1. Go to `/course-recommender` page
2. Status indicator updates: **"🔴 Recording Course Recommender AI (X)"**
3. Search for courses
4. Submit survey answers
5. Recommendations are logged with response time

#### **Testing Multiple AIs:**
- You can freely switch between pages
- Each AI interaction is automatically logged with the correct AI type
- No order enforced - test in any sequence you want

---

### **Step 7: Stop Recording & Generate Report**

When you're done testing, click the **"Stop (X)"** button in the header:

**What Happens:**
1. Recording stops immediately
2. System generates a comprehensive diagnostic report
3. Report is saved to `Backend/logs/ai_diagnostic_frontend_recording_YYYY-MM-DD_HH-MM-SS.json`
4. Toast notification shows:
   - **Status:** ✅ PASS / ⚠️ WARNING / ❌ FAIL
   - **Score:** XX/100
   - **Interactions:** Total number logged

---

## 📊 Report Structure

The generated report includes:

```json
{
  "test_id": "frontend_recording_abc12345",
  "session_id": "full-uuid-here",
  "timestamp": "2025-10-27T18:30:00.000000",
  "test_name": "Frontend AI Test Recording",
  "test_type": "frontend_integrated",
  "status": "PASS",
  "overall_score": 92.5,
  "duration_seconds": 245.67,
  "summary": {
    "started_at": "2025-10-27T18:25:00.000000",
    "stopped_at": "2025-10-27T18:30:00.000000",
    "total_interactions": 15,
    "ai_types_tested": ["chatbot", "career_suggester"],
    "user_id": 2
  },
  "ai_reports": {
    "chatbot": {
      "ai_type": "chatbot",
      "score": 95.0,
      "total_interactions": 10,
      "avg_response_time_ms": 3200,
      "quality_scores": [100, 90, 90, 95, ...],
      "issues": [],
      "status": "PASS"
    },
    "career_suggester": {
      "ai_type": "career_suggester",
      "score": 90.0,
      "total_interactions": 5,
      "avg_response_time_ms": 2800,
      "quality_scores": [90, 90, 90, 90, 90],
      "issues": [],
      "status": "PASS"
    }
  },
  "metadata": {
    "test_mode": "frontend_recording",
    "manual_control": true
  }
}
```

---

## 🎯 Testing Scenarios

### **Scenario 1: Quick Chatbot Test**
1. Enable Test Mode
2. Click "Start"
3. Go to `/chatbot`
4. Send 5 messages
5. Click "Stop"
6. Check report in `Backend/logs/`

**Time:** ~2-3 minutes

---

### **Scenario 2: Comprehensive Multi-AI Test**
1. Enable Test Mode
2. Click "Start"
3. Go to `/chatbot` → Send 3 messages
4. Go to `/career-suggester` → Complete assessment
5. Go to `/course-recommender` → Search for courses
6. Click "Stop"
7. Check comprehensive report covering all 3 AIs

**Time:** ~10-15 minutes

---

### **Scenario 3: Long-Form Career Suggester Test**
1. Enable Test Mode
2. Click "Start"
3. Go to `/career-suggester`
4. Answer all 11 questions thoughtfully
5. Review suggestions
6. Click "Stop"
7. Check detailed report with all Q&A pairs and suggestions

**Time:** ~5-10 minutes

---

## 🔍 Quality Scoring

### **Chatbot Quality Analysis:**
- **100 points** - High-quality, relevant career advice
- **-30 points** - Response too short (< 20 chars)
- **-40 points** - No career-related keywords
- **-20 points** - Low relevance to user question

### **Career Suggester Quality Analysis:**
- **100 points** - Valid suggestions with detailed answers
- **-50 points** - No suggestions returned
- **-30 points** - Missing or incomplete answers

### **Course Recommender Quality Analysis:**
- **100 points** - Relevant courses with proper data
- **-50 points** - No courses returned
- **-20 points** - Insufficient course count (< 3)

---

## 🛠️ API Endpoints

### **Start Recording**
```
POST /api/tests/start-recording
Content-Type: application/json

{
  "user_id": 2  // Optional
}

Response:
{
  "success": true,
  "session_id": "uuid-here",
  "message": "Test recording started",
  "started_at": "2025-10-27T18:25:00.000000"
}
```

### **Log Interaction**
```
POST /api/tests/log-interaction
Content-Type: application/json

{
  "session_id": "uuid-here",
  "ai_type": "chatbot",  // or "career_suggester" or "course_recommender"
  "interaction": {
    "user_message": "What skills are important for data science?",
    "ai_response": "Data science requires...",
    "response_time_ms": 3200,
    "conversation_id": "optional-conv-id"
  }
}

Response:
{
  "success": true,
  "message": "Interaction logged",
  "interaction_id": "uuid-here",
  "total_interactions": 5
}
```

### **Stop Recording**
```
POST /api/tests/stop-recording
Content-Type: application/json

{
  "session_id": "uuid-here"
}

Response:
{
  "success": true,
  "message": "Test recording stopped",
  "report": { /* full comprehensive report */ }
}
```

### **Get Session Status**
```
GET /api/tests/session-status/{session_id}

Response:
{
  "success": true,
  "session_id": "uuid-here",
  "started_at": "2025-10-27T18:25:00.000000",
  "total_interactions": 15,
  "ai_types_tested": ["chatbot", "career_suggester"],
  "interactions_by_type": {
    "chatbot": 10,
    "career_suggester": 5
  }
}
```

---

## 📝 Summary

### **What You Get:**
✅ Real-time frontend-integrated testing  
✅ Automatic AI detection based on page  
✅ No time limits - test at your own pace  
✅ Manual start/stop control  
✅ Comprehensive diagnostic reports  
✅ Quality scoring for each AI  
✅ Visual status indicators  
✅ Saved JSON reports for analysis  

### **What Changed:**
- ✅ Tests now run from the frontend (no CLI needed)
- ✅ Automatic AI type detection (no manual selection)
- ✅ No time limits (indefinite recording)
- ✅ Manual control (start/stop buttons)
- ✅ Real-time visual feedback
- ✅ Multi-AI testing in single session

### **Old System vs New System:**

| Feature | Old System (CLI) | New System (Frontend) |
|---------|-----------------|----------------------|
| **Interface** | Terminal commands | Web UI with buttons |
| **AI Detection** | Manual `--test` flag | Automatic based on page |
| **Time Limit** | Fixed test scenarios | Unlimited |
| **Start/Stop** | Automatic | Manual control |
| **Testing Multiple AIs** | Separate runs | Single session |
| **Real-time Feedback** | Console only | Visual indicators |
| **Report Format** | Same JSON | Same JSON + summary |

---

## 🎉 You're All Set!

Your AI testing system is now **production-ready** with:
- ✅ Frontend integration complete
- ✅ Automatic AI detection working
- ✅ Manual control implemented
- ✅ No time limits enforced
- ✅ Comprehensive reporting active

**Start testing and enjoy the new workflow!** 🚀

