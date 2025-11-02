# Chat History Feature - ChatGPT Style Implementation

## Overview

This feature adds ChatGPT-style conversation management to the AI Career Chatbot, allowing users to:
- Save conversations automatically to the database
- View a list of all previous conversations
- Load and continue previous conversations
- Create new chats
- Delete old conversations

## Database Changes

### Updated ChatHistory Model

```python
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    conversation_id = db.Column(db.String(36), nullable=False, index=True)  # NEW: UUID for grouping
    chat_title = db.Column(db.String(255), nullable=True)  # NEW: Auto-generated title
    message = db.Column(db.Text, nullable=False)
    reply = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

**Key Changes:**
- `conversation_id`: Groups multiple messages into a single conversation
- `chat_title`: Auto-generated from the first user message

## Backend API Endpoints

### 1. POST /api/chatbot/message (Updated)
**Purpose:** Send a message and automatically save to database

**Request:**
```json
{
  "message": "What career should I pursue?",
  "history": [...],
  "user_id": 1,
  "conversation_id": "uuid-string"  // optional, created if new
}
```

**Response:**
```json
{
  "success": true,
  "reply": "Based on your background...",
  "history_update": [...],
  "conversation_id": "uuid-string"
}
```

### 2. GET /api/chatbot/conversations
**Purpose:** Get list of all conversations for a user

**Request:** `GET /api/chatbot/conversations?user_id=1`

**Response:**
```json
{
  "success": true,
  "conversations": [
    {
      "conversation_id": "uuid-123",
      "title": "Career advice for software engineering...",
      "created_at": "2025-10-26T12:00:00",
      "message_count": 5,
      "preview": "What career should I pursue after..."
    }
  ]
}
```

### 3. GET /api/chatbot/conversations/<conversation_id>
**Purpose:** Get full history of a specific conversation

**Request:** `GET /api/chatbot/conversations/uuid-123?user_id=1`

**Response:**
```json
{
  "success": true,
  "conversation": {
    "conversation_id": "uuid-123",
    "title": "Career advice for software engineering...",
    "created_at": "2025-10-26T12:00:00",
    "history": [
      {"role": "user", "content": "What career..."},
      {"role": "assistant", "content": "Based on..."}
    ],
    "message_count": 5
  }
}
```

### 4. DELETE /api/chatbot/conversations/<conversation_id>
**Purpose:** Delete a conversation

**Request:** `DELETE /api/chatbot/conversations/uuid-123?user_id=1`

**Response:**
```json
{
  "success": true,
  "message": "Deleted 5 messages"
}
```

## Frontend Components

### 1. ChatSidebar Component (NEW)
**File:** `src/components/chatbot/ChatSidebar.jsx`

**Features:**
- Displays list of saved conversations
- Shows conversation title, date, and message count
- Allows clicking to load a conversation
- "New Chat" button to start fresh
- Delete button for each conversation
- Collapsible sidebar

**Props:**
```javascript
<ChatSidebar
  userId={user.id}
  currentConversationId={conversationId}
  onSelectConversation={(id) => {...}}
  onNewChat={() => {...}}
  isCollapsed={false}
  onToggleCollapse={() => {...}}
/>
```

### 2. Updated ChatWindow Component
**File:** `src/components/chatbot/ChatWindow.jsx`

**New Props:**
- `userId`: Current user ID for saving messages
- `conversationId`: Current conversation ID
- `onConversationIdChange`: Callback when conversation ID changes
- `messages`: Initial messages (for loading conversations)
- `onMessagesChange`: Callback when messages change

### 3. Updated Chatbot Page
**File:** `src/pages/Chatbot.jsx`

**Changes:**
- Integrated ChatSidebar component
- Manages conversation state
- Handles loading/creating/deleting conversations
- Passes user ID to ChatWindow for saving

## Frontend API Functions

**File:** `src/services/api.js`

```javascript
// Updated to include userId and conversationId
sendChatMessage(message, history, userId, conversationId)

// Get all conversations for a user
getChatConversations(userId)

// Get specific conversation
getChatConversation(conversationId, userId)

// Delete a conversation
deleteChatConversation(conversationId, userId)
```

## How It Works

### Conversation Flow

1. **Starting a New Chat:**
   - User clicks "New Chat" button
   - `conversationId` is set to `null`
   - User sends first message
   - Backend generates new UUID for `conversation_id`
   - Backend auto-generates title from first message
   - Message saved to database with new conversation_id
   - Frontend receives conversation_id and stores it

2. **Continuing a Conversation:**
   - User sends another message
   - Frontend includes existing `conversation_id`
   - Backend saves message with same `conversation_id`
   - All messages grouped together

3. **Loading Previous Conversation:**
   - User clicks conversation in sidebar
   - Frontend calls `getChatConversation(id, userId)`
   - Backend returns all messages in that conversation
   - Frontend displays messages in ChatWindow
   - User can continue chatting with same conversation_id

4. **Deleting a Conversation:**
   - User clicks delete button
   - Confirms deletion
   - Frontend calls `deleteChatConversation(id, userId)`
   - Backend deletes all messages with that conversation_id
   - Sidebar refreshes to remove deleted conversation

## UI Features

### ChatGPT-Style Design

**Left Sidebar:**
- List of conversations (newest first)
- Each item shows:
  - Message icon
  - Conversation title
  - Date (Today, Yesterday, X days ago)
  - Message count
  - Delete button (on hover)
- "+ New Chat" button at top
- Collapsible with toggle button

**Main Chat Area:**
- Full chat interface
- Messages automatically save
- Continues previous conversations seamlessly

**Right Sidebar (Optional):**
- Sample questions
- Tips
- Information

### Visual Indicators
- Active conversation highlighted in sidebar
- Loading states for fetching conversations
- Empty state when no conversations exist
- Confirmation dialog before deleting

## Database Migration

**IMPORTANT:** The ChatHistory table schema has changed!

### Migration Steps:

1. **Option A: Drop and recreate (development only)**
```bash
# Stop backend
# Delete the database file
rm Backend/instance/course_recommendation.db
# Restart backend - tables will be recreated
python app.py
```

2. **Option B: Manual migration (if you have data to keep)**
```sql
ALTER TABLE chat_history ADD COLUMN conversation_id VARCHAR(36);
ALTER TABLE chat_history ADD COLUMN chat_title VARCHAR(255);
CREATE INDEX idx_conversation_id ON chat_history(conversation_id);
```

## Testing the Feature

### Step 1: Restart Backend
```bash
cd Backend
# Delete old database to apply schema changes (dev only)
rm instance/course_recommendation.db
python app.py
```

### Step 2: Login and Navigate to Chatbot
1. Go to http://localhost:5173/login
2. Login with your credentials
3. Navigate to the Chatbot page

### Step 3: Test New Conversation
1. You should see an empty sidebar (no conversations yet)
2. Send a message: "What career should I pursue?"
3. Wait for AI response
4. Send another message: "Tell me more about data science"
5. Conversation is automatically saved

### Step 4: Test Loading Conversation
1. Click "+ New Chat" button
2. Start a different conversation
3. Look at sidebar - you should see 2 conversations
4. Click on the first conversation
5. Messages should load back into chat window

### Step 5: Test Deleting Conversation
1. Hover over a conversation in sidebar
2. Click the trash icon
3. Confirm deletion
4. Conversation should be removed from sidebar

### Step 6: Verify Database
Open database with DB Browser for SQLite:
1. Go to `Backend/instance/course_recommendation.db`
2. Browse `chat_history` table
3. You should see:
   - Multiple messages with same `conversation_id`
   - `chat_title` on first message
   - All linked to your `user_id`

## Troubleshooting

### Sidebar Not Showing
- Make sure you're logged in
- Check browser console for errors
- Verify backend is running

### Conversations Not Saving
- Check that `user.id` is being passed to ChatWindow
- Look at backend logs for errors
- Verify database file exists

### "Column not found" Error
- Delete database file and restart backend
- Or run SQL migration manually

### Conversations Not Loading
- Check browser Network tab
- Verify API endpoint is being called
- Check backend logs for errors

## Security Considerations

- All endpoints require `user_id` parameter
- Conversations are user-scoped (users can only see their own)
- No conversation sharing between users
- Delete operations verify user ownership

## Future Enhancements

Possible improvements:
- [ ] Rename conversation titles
- [ ] Search conversations
- [ ] Export conversation as PDF/text
- [ ] Share conversations
- [ ] Conversation folders/categories
- [ ] Star/favorite conversations
- [ ] Better title generation using LLM
- [ ] Conversation analytics
- [ ] Auto-delete old conversations

## Files Modified

**Backend:**
- `models.py` - Updated ChatHistory model
- `blueprints/chatbot_bp.py` - Added new endpoints

**Frontend:**
- `services/api.js` - Added conversation API functions
- `components/chatbot/ChatSidebar.jsx` - NEW sidebar component
- `components/chatbot/ChatSidebar.css` - NEW sidebar styles
- `components/chatbot/ChatWindow.jsx` - Updated to accept props
- `pages/Chatbot.jsx` - Integrated sidebar
- `pages/Chatbot.css` - Updated layout styles

## Summary

You now have a complete ChatGPT-style conversation history system! Users can:
✅ Have multiple conversations saved automatically
✅ Switch between conversations easily
✅ Continue previous conversations
✅ Create new chats
✅ Delete old conversations
✅ See conversation titles and metadata

The system is fully functional and ready to use!

