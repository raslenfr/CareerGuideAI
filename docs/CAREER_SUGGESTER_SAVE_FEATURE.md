# Career Suggester Save Feature Documentation

## Overview
This document describes the save functionality implemented for the Career Suggester component, similar to the chat save feature.

## Features Implemented

### 1. Database Model
**File**: `Backend/models.py`

Created `CareerSuggestion` model with the following fields:
- `id`: Primary key
- `user_id`: Foreign key to User model
- `session_id`: UUID for unique session identification
- `session_title`: Auto-generated title from user's answers
- `answers`: JSON string of all Q&A pairs
- `suggestions`: JSON string of career suggestions
- `created_at`: Timestamp

### 2. Backend API Endpoints
**File**: `Backend/blueprints/suggester_bp.py`

#### POST `/api/suggester/save-session`
Saves a completed suggestion session to the database.

**Request Body**:
```json
{
  "user_id": 1,
  "answers": {
    "What subjects did you enjoy...": "I enjoyed mathematics and computer science...",
    ...
  },
  "suggestions": {
    "summary": "Based on your answers...",
    "suggestions": [
      {"career": "Software Engineer", "reason": "Your skills match..."},
      ...
    ]
  },
  "session_id": "uuid-string" (optional)
}
```

**Response**:
```json
{
  "success": true,
  "message": "Session saved successfully",
  "session_id": "generated-uuid",
  "session_title": "Generated Title"
}
```

#### GET `/api/suggester/sessions?user_id={userId}`
Retrieves all saved sessions for a user.

**Response**:
```json
{
  "success": true,
  "sessions": [
    {
      "id": 1,
      "session_id": "uuid",
      "session_title": "12th - technical role",
      "created_at": "2025-10-27T12:00:00"
    },
    ...
  ]
}
```

#### GET `/api/suggester/sessions/{session_id}?user_id={userId}`
Retrieves a specific session with full details.

**Response**:
```json
{
  "success": true,
  "session": {
    "id": 1,
    "session_id": "uuid",
    "session_title": "12th - technical role",
    "answers": {...},
    "suggestions": {...},
    "created_at": "2025-10-27T12:00:00"
  }
}
```

#### DELETE `/api/suggester/sessions/{session_id}?user_id={userId}`
Deletes a saved session.

**Response**:
```json
{
  "success": true,
  "message": "Session deleted successfully"
}
```

### 3. Frontend Components

#### SuggesterSidebar Component
**File**: `src/components/suggester/SuggesterSidebar.jsx`

Features:
- Displays list of saved sessions
- "New Session" button to start fresh
- Session deletion with confirmation
- Click to load previous sessions
- Collapsible sidebar
- Date formatting ("Today", "Yesterday", "X days ago")

#### Updated CareerSuggester Page
**File**: `src/pages/CareerSuggester.jsx`

New Features:
1. **Save Button in Header**
   - Only visible when results are available
   - Shows "Save Session" / "Saving..." / "Saved" states
   - Disabled when already saved or no results

2. **Auto-Save on Navigation**
   - Automatically saves session when user navigates away
   - Silent save (no toast notification)
   - Only saves if results exist and not already saved

3. **Session Management**
   - Load previous sessions from sidebar
   - Start new session
   - Track save state

4. **State Management**
   - `currentSessionId`: Tracks active session
   - `isSaved`: Prevents duplicate saves
   - `isSaving`: Shows loading state
   - `hasUnsavedResultsRef`: Tracks unsaved changes for auto-save

### 4. API Service Functions
**File**: `src/services/api.js`

New Functions:
```javascript
// Save a suggestion session
saveSuggesterSession(userId, answers, suggestions, sessionId?)

// Get all sessions for a user
getSuggesterSessions(userId)

// Get specific session details
getSuggesterSession(sessionId, userId)

// Delete a session
deleteSuggesterSession(sessionId, userId)
```

### 5. Styling
**File**: `src/pages/CareerSuggester.css`

Added styles for:
- Page header with icon and save button
- Save button states (normal, disabled, saved)
- Suggester container with sidebar layout
- Responsive design for mobile devices

**File**: `src/components/suggester/SuggesterSidebar.css`

Complete styling for:
- Sidebar container and header
- Session list items
- Active session highlighting
- Delete button on hover
- Loading and empty states
- Collapsed sidebar state

## Session Title Generation

The system automatically generates meaningful titles based on user answers:

1. **Priority 1**: Education level + Career preference
   - Example: "12th - technical role"

2. **Priority 2**: First answer (truncated to 50 chars)
   - Example: "I enjoy mathematics and computer science..."

3. **Fallback**: "Career Suggestion Session"

## User Flow

### Saving a Session
1. User completes all 11 questions
2. System displays career suggestions
3. "Save Session" button appears in header
4. User clicks "Save Session"
5. System saves to database with auto-generated title
6. Button changes to "Saved" with checkmark
7. Session appears in sidebar immediately

### Auto-Save on Navigation
1. User completes assessment and views results
2. User navigates to another page
3. System automatically saves session silently
4. No toast notification shown
5. Session available in sidebar on return

### Loading a Previous Session
1. User clicks session in sidebar
2. System fetches session data
3. Display results view with saved suggestions
4. User can review past suggestions
5. "Start Over" button creates new session

### Creating a New Session
1. User clicks "New Session" button
2. System resets all state
3. Fetches first question from backend
4. User begins new assessment
5. Previous session saved state preserved

## Database Schema

```sql
CREATE TABLE career_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(36) UNIQUE NOT NULL,
    session_title VARCHAR(255),
    answers TEXT NOT NULL,
    suggestions TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_user_id ON career_suggestions(user_id);
CREATE INDEX idx_session_id ON career_suggestions(session_id);
```

## Testing Guide

### 1. Backend Testing
Start the Flask server:
```bash
cd Backend
python app.py
```

The server will automatically create the `career_suggestions` table on startup.

### 2. Frontend Testing

#### Test Save Functionality:
1. Log in to the application
2. Navigate to Career Suggester (`/career-suggester`)
3. Complete all 11 questions
4. Click "Save Session" button
5. Verify toast notification shows success
6. Check sidebar shows new session

#### Test Auto-Save:
1. Complete assessment and view results
2. Navigate to Dashboard or Home
3. Return to Career Suggester
4. Check sidebar - session should be saved

#### Test Load Session:
1. Click on a session in sidebar
2. Verify results are displayed correctly
3. Check that "Saved" button is displayed
4. Try "Start Over" to begin new session

#### Test Delete Session:
1. Hover over a session in sidebar
2. Click trash icon
3. Confirm deletion
4. Verify session is removed

### 3. Database Verification

Check saved sessions:
```bash
cd Backend
python -c "from app import app, db; from models import CareerSuggestion; app.app_context().push(); sessions = CareerSuggestion.query.all(); print(f'Total sessions: {len(sessions)}'); [print(f'{s.session_title} - {s.created_at}') for s in sessions]"
```

## Error Handling

The implementation includes comprehensive error handling:

1. **Missing User**: Prompts to log in
2. **Network Errors**: Shows error toast with details
3. **Already Saved**: Shows info toast, prevents duplicate
4. **Invalid Data**: Backend validates all inputs
5. **Database Errors**: Rolls back transaction, shows error

## Mobile Responsiveness

The sidebar and save button are fully responsive:
- **Desktop**: Sidebar always visible, save button in header
- **Tablet**: Sidebar collapsible, optimized layout
- **Mobile**: Sidebar as overlay, save button full-width

## Differences from Chat Save Feature

1. **Granularity**: Saves complete sessions (not individual Q&A pairs)
2. **Title Generation**: Based on user answers, not first message
3. **Data Structure**: JSON objects for answers and suggestions
4. **No Real-time Updates**: Saves only on completion or navigation
5. **Single Save**: Each session saved once (vs chat with multiple messages)

## Future Enhancements

Potential improvements:
1. Edit session titles
2. Export sessions as PDF
3. Share sessions with others
4. Compare multiple sessions
5. Session categories/tags
6. Search functionality
7. Session notes/comments

## Troubleshooting

### Session Not Saving
- Check user is logged in
- Verify assessment is complete
- Check browser console for errors
- Ensure backend server is running

### Sidebar Not Loading
- Check network tab for API errors
- Verify user_id is being sent
- Check backend logs for errors

### Auto-Save Not Working
- Ensure results exist before navigation
- Check useEffect cleanup is running
- Verify hasUnsavedResultsRef is tracking correctly

## File Summary

### Backend Files
- `Backend/models.py`: CareerSuggestion model
- `Backend/blueprints/suggester_bp.py`: API endpoints
- `Backend/extensions.py`: Database configuration

### Frontend Files
- `src/pages/CareerSuggester.jsx`: Main component with save logic
- `src/pages/CareerSuggester.css`: Component styles
- `src/components/suggester/SuggesterSidebar.jsx`: Sidebar component
- `src/components/suggester/SuggesterSidebar.css`: Sidebar styles
- `src/services/api.js`: API service functions

## Conclusion

The Career Suggester save feature provides a complete session management system similar to ChatGPT's conversation management. Users can save, load, and manage their career assessment sessions with automatic title generation and seamless integration with the existing application.

