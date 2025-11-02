# Quick Setup Guide - Career Suggester Save Feature

## Step 1: Create Database Tables

The backend will automatically create the `career_suggestions` table when you start the server. However, if you want to manually create it first:

```bash
cd Backend
python -c "from app import app, db; from models import CareerSuggestion; app.app_context().push(); db.create_all(); print('✅ Database tables created!')"
```

## Step 2: Start the Backend Server

```bash
cd Backend
python app.py
```

You should see:
```
INFO:app:Database tables created successfully.
INFO:app:✅ All blueprints registered successfully.
* Running on http://127.0.0.1:5000
```

## Step 3: Start the Frontend

In a new terminal:

```bash
cd Frontend
npm run dev
```

## Step 4: Test the Feature

1. **Open your browser**: Navigate to `http://localhost:5173`

2. **Log in or Sign up**: You must be logged in to save sessions

3. **Go to Career Suggester**: Click "Career Suggester" in the navigation

4. **Complete the Assessment**:
   - Answer all 11 questions
   - Click "Next" after each question
   - Wait for career suggestions to appear

5. **Save Your Session**:
   - Click the "Save Session" button in the top-right
   - You'll see a success toast notification
   - The button will change to "Saved" with a checkmark
   - Your session will appear in the left sidebar

6. **Test Auto-Save**:
   - Complete a new assessment (click "New Session" first)
   - View the results
   - Navigate to another page (Dashboard, Home, etc.)
   - Come back to Career Suggester
   - Your session should be in the sidebar (auto-saved!)

7. **Load a Previous Session**:
   - Click on any session in the sidebar
   - The results will be displayed
   - The "Saved" button will be shown

8. **Delete a Session**:
   - Hover over a session in the sidebar
   - Click the trash icon that appears
   - Confirm the deletion
   - Session is removed

## Step 5: Verify in Database

Check that sessions are being saved:

```bash
cd Backend
python -c "from app import app, db; from models import CareerSuggestion; app.app_context().push(); sessions = CareerSuggestion.query.all(); print(f'✅ Found {len(sessions)} saved sessions'); for s in sessions: print(f'  - {s.session_title}')"
```

## Common Issues

### Issue: "Failed to save session" error
**Solution**: 
- Make sure backend is running
- Check browser console for detailed errors
- Verify you're logged in

### Issue: Sidebar not showing sessions
**Solution**:
- Check Network tab in DevTools
- Verify `/api/suggester/sessions` endpoint returns data
- Check user_id is being sent correctly

### Issue: Auto-save not working
**Solution**:
- Ensure you complete all questions and see results
- Don't click "Start Over" before navigating away
- Check browser console for any JavaScript errors

## Architecture Overview

```
Frontend                          Backend
┌─────────────────┐              ┌──────────────────┐
│ CareerSuggester │              │ suggester_bp.py  │
│   Component     │─────────────▶│   /save-session  │
│                 │              │   /sessions      │
│                 │              │   /sessions/:id  │
└─────────────────┘              └──────────────────┘
        │                                 │
        │                                 │
        ▼                                 ▼
┌─────────────────┐              ┌──────────────────┐
│ SuggesterSidebar│              │    models.py     │
│   Component     │              │ CareerSuggestion │
└─────────────────┘              └──────────────────┘
        │                                 │
        │                                 │
        ▼                                 ▼
┌─────────────────┐              ┌──────────────────┐
│   api.js        │              │  SQLite Database │
│ Service Layer   │              │ career_suggestions│
└─────────────────┘              └──────────────────┘
```

## What Was Implemented

✅ **Backend**:
- `CareerSuggestion` database model
- 4 new API endpoints (save, list, get, delete)
- Auto-title generation from user answers
- Full error handling and validation

✅ **Frontend**:
- Save button in page header
- Auto-save on navigation away
- Sidebar component for session history
- Load previous sessions
- Delete sessions with confirmation
- Responsive design for all screen sizes

✅ **Features**:
- Manual save with toast notifications
- Silent auto-save on navigation
- Duplicate prevention (can't save twice)
- Session title auto-generation
- Date formatting ("Today", "Yesterday", etc.)
- Loading states and error handling

## Next Steps

Now that the save feature is working, you can:

1. **Test it thoroughly**: Complete multiple assessments and save them
2. **Customize titles**: Add a feature to let users edit session titles
3. **Export sessions**: Add PDF export functionality
4. **Share sessions**: Allow users to share results with others
5. **Analytics**: Track which careers are suggested most often

Enjoy your new Career Suggester save feature! 🚀

