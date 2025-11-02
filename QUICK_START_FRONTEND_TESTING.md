# Quick Start: Frontend-Integrated AI Testing

## 🚀 5-Minute Setup

### 1. Start Backend
```bash
cd Backend
python app.py
```

### 2. Start Frontend
```bash
cd Frontend
npm run dev
```

### 3. Log In
- Open `http://localhost:5173`
- Sign up or log in

---

## 🎯 How to Test (3 Easy Steps)

### **Step 1: Enable Test Mode**
- Look at the top header
- Click **"Test: OFF"** button
- It turns green: **"Test: ON"**

### **Step 2: Start Recording**
- Click the green **"Start"** button
- Status indicator appears in bottom-right corner
- Shows: **"🔴 Recording [AI Name] (0)"**

### **Step 3: Test & Stop**
- Navigate to any AI page:
  - `/chatbot` - Chat with AI
  - `/career-suggester` - Complete assessment
  - `/course-recommender` - Search courses
- Interact normally
- When done, click red **"Stop (X)"** button
- Report saved to `Backend/logs/`

---

## 📍 Where Things Are

### **Frontend Controls (Header):**
```
┌─────────────────────────────────────────────────┐
│  Logo    [Test: ON] [Start]  [User Menu]       │
└─────────────────────────────────────────────────┘
```

### **Status Indicator (Bottom-Right):**
```
┌────────────────────────────────────────┐
│ 🔴 Recording Chatbot AI (5)            │
└────────────────────────────────────────┘
```

---

## 💡 Key Features

| Feature | How It Works |
|---------|--------------|
| **No Time Limits** | Test runs until you click "Stop" |
| **Auto AI Detection** | System knows which AI you're testing based on page |
| **Multi-AI Testing** | Switch between pages, all logged in one session |
| **Manual Control** | You decide when to start and stop |

---

## 📊 Example Test Flow

```
1. Click "Test: ON"              → Test mode enabled
2. Click "Start"                 → Recording begins (0 interactions)
3. Go to /chatbot                → Detected: Chatbot AI
4. Send 3 messages               → Counter: (1), (2), (3)
5. Go to /career-suggester       → Detected: Career Suggester AI
6. Answer questions              → Counter: (4), (5), (6)...
7. Click "Stop (11)"             → Recording stops
8. See toast: "✅ Test Complete! Score: 92.5/100 | Interactions: 11"
9. Check: Backend/logs/ai_diagnostic_frontend_recording_*.json
```

---

## 🎉 That's It!

You're now testing AI systems in real-time with:
- ✅ Unlimited testing time
- ✅ Automatic detection
- ✅ Manual control
- ✅ Comprehensive reports

**Happy Testing!** 🧪

