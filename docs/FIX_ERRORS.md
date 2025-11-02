# Fix Errors - Complete Guide

## Issues Found

1. ✅ Fixed: Infinite loop in handleSampleQuestionClick (Chatbot.jsx)
2. ⚠️ Need to fix: Database schema needs migration
3. ✅ Fixed: Missing dependency array in useImperativeHandle (ChatSidebar.jsx)

## Step 1: Stop Backend Server

**IMPORTANT:** The database file is locked. You need to stop the backend first!

Press `Ctrl+C` in the terminal where `python app.py` is running.

## Step 2: Recreate Database with New Schema

After stopping the backend, run:

```bash
cd Backend
python app.py
```

The backend will automatically recreate the database with the updated schema (including `conversation_id` and `chat_title` columns).

## Step 3: Verify Frontend Fixes

The following fixes have been applied:

**File: src/pages/Chatbot.jsx**
- Removed the recursive useEffect that was causing infinite loop
- Function now properly delegates to window.handleSuggestedPrompt

**File: src/components/chatbot/ChatSidebar.jsx**
- Added dependency array to useImperativeHandle to prevent infinite re-renders

## Step 4: Restart Frontend (if needed)

```bash
cd Frontend
npm run dev
```

## What Was Fixed

### 1. Infinite Loop in Chatbot.jsx

**Before (Broken):**
```javascript
const handleSampleQuestionClick = (question) => {
  if (window.handleSuggestedPrompt) {
    window.handleSuggestedPrompt(question)  // Calls handleSampleQuestionClick
  }
}

useEffect(() => {
  window.handleSuggestedPrompt = handleSampleQuestionClick  // Recursion!
  return () => {
    delete window.handleSuggestedPrompt
  }
}, [])
```

**After (Fixed):**
```javascript
const handleSampleQuestionClick = (question) => {
  if (window.handleSuggestedPrompt) {
    window.handleSuggestedPrompt(question)
  }
}
// Removed the useEffect that was causing recursion
```

### 2. Sidebar useImperativeHandle Fix

**Before:**
```javascript
useImperativeHandle(ref, () => ({
  loadConversations,
}))
```

**After:**
```javascript
useImperativeHandle(ref, () => ({
  loadConversations,
}), [])  // Added dependency array
```

### 3. Database Schema Migration

The database needs the new columns. Options:

**Option A: Delete and Recreate (Recommended for Development)**
1. Stop backend (Ctrl+C)
2. Delete: `Backend/instance/course_recommendation.db`
3. Restart: `python app.py`
4. Database will be recreated with new schema

**Option B: Run Migration Script**
1. Stop backend
2. Run: `python migrate_database.py`
3. Restart backend

## Testing After Fixes

1. **Start Backend:**
```bash
cd Backend
python app.py
```

2. **Start Frontend:**
```bash
cd Frontend
npm run dev
```

3. **Test Save Chat:**
   - Login
   - Go to Chatbot
   - Send a message
   - Click "Save Chat" button
   - Should see "Chat saved successfully!"
   - Conversation should appear in sidebar

4. **Check Console:**
   - No more 500 errors
   - No more stack overflow errors
   - Sidebar should load conversations

## If Errors Persist

### 500 Error on /conversations

**Check backend terminal for error message.**

Common issues:
1. Database columns don't exist
   - **Fix:** Delete database and restart backend
   
2. Import errors in Python
   - **Fix:** Check that extensions.py exists
   - **Fix:** Check that models import from extensions

3. SQLAlchemy session errors
   - **Fix:** Check database is properly initialized

### Maximum Call Stack

**Should be fixed now.** If still happening:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5)
3. Check if useEffect dependencies are correct

### Vite Reload Errors

**Should be fixed now.** If still happening:
1. Stop frontend
2. Delete `node_modules` and `package-lock.json`
3. Run `npm install` again

## Database Schema

**Expected columns in chat_history table:**
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER FOREIGN KEY)
- conversation_id (VARCHAR(36)) ← NEW
- chat_title (VARCHAR(255)) ← NEW
- message (TEXT)
- reply (TEXT)
- created_at (DATETIME)

**To verify schema:**
```bash
cd Backend/instance
sqlite3 course_recommendation.db
.tables
.schema chat_history
```

## Summary of Changes

**Files Modified:**
1. `src/pages/Chatbot.jsx` - Fixed infinite loop
2. `src/components/chatbot/ChatSidebar.jsx` - Fixed useImperativeHandle
3. `../Backend/migrate_database.py` - NEW: Migration script

**Action Required:**
1. Stop backend server
2. Delete database OR run migration
3. Restart backend
4. Test save functionality

Everything should work after restarting the backend with the updated schema!

