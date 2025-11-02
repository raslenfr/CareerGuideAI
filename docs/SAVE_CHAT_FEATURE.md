# Save Chat Feature - Manual & Auto-Save Implementation

## Overview

This feature adds two ways to save conversations:
1. **Manual Save Button** - User explicitly clicks "Save Chat" button
2. **Auto-Save on Navigation** - Automatically saves when user navigates away

## Key Features

✅ **Manual Save Button**
- Located in page header next to chat title
- Shows different states: Save/Saving/Saved
- Disabled when no messages or already saved
- Displays checkmark icon when saved
- Immediately adds to sidebar after saving

✅ **Auto-Save on Navigation**
- Triggers when user navigates away from chatbot page
- Only saves if there are unsaved changes
- Silent save (no toast notification)
- Prevents data loss

✅ **Smart State Management**
- Tracks saved/unsaved status
- Prevents duplicate saves
- Marks loaded conversations as already saved
- Clears unsaved flag after successful save

## Backend Implementation

### New Endpoint: POST /api/chatbot/save-conversation

**Purpose:** Save an entire conversation to the database at once

**Request:**
```json
{
  "user_id": 1,
  "messages": [
    {"role": "user", "content": "What career should I pursue?"},
    {"role": "assistant", "content": "Based on your background..."},
    {"role": "user", "content": "Tell me more about data science"},
    {"role": "assistant", "content": "Data science involves..."}
  ],
  "conversation_id": "optional-uuid"
}
```

**Response (Success):**
```json
{
  "success": true,
  "conversation_id": "uuid-123",
  "title": "What career should I pursue?...",
  "message_count": 2,
  "message": "Conversation saved successfully"
}
```

**Response (Already Saved):**
```json
{
  "success": false,
  "error": "Conversation already saved"
}
```

### Updated Endpoint: POST /api/chatbot/message

**New Parameter:** `auto_save` (boolean, default: false)

```json
{
  "message": "What career should I pursue?",
  "history": [...],
  "user_id": 1,
  "conversation_id": "uuid",
  "auto_save": false  // NEW: Only saves if true
}
```

**Behavior:**
- Messages are NO LONGER auto-saved by default
- Only saves if `auto_save: true` is explicitly passed
- This gives users control over what gets saved

## Frontend Implementation

### Save Button (Chatbot.jsx)

**Location:** Page header, right side next to title

**Button States:**

1. **Default (Unsaved)**
   ```
   [💾 Save Chat]
   - Blue background
   - Enabled when user has messages
   ```

2. **Saving**
   ```
   [⟳ Saving...]
   - Spinning save icon
   - Disabled during save
   ```

3. **Saved**
   ```
   [✓ Saved]
   - Green background
   - Disabled (already saved)
   ```

### Save Logic

**Function:** `saveChatToDatabase(isSilent)`

```javascript
const saveChatToDatabase = async (isSilent = false) => {
  // 1. Check user is authenticated
  // 2. Filter out welcome message
  // 3. Validate at least one message exchange exists
  // 4. Call save API
  // 5. Update state (conversation_id, isSaved)
  // 6. Refresh sidebar to show new conversation
  // 7. Show toast (if not silent)
}
```

**Parameters:**
- `isSilent` (boolean): If true, no toast notifications shown
  - Used for auto-save on navigation
  - Prevents popup when user is leaving page

### Auto-Save Implementation

**Trigger:** Component unmount / navigation away

```javascript
useEffect(() => {
  return () => {
    // Cleanup function runs when component unmounts
    if (hasUnsavedChangesRef.current && user?.id) {
      saveChatToDatabase(true) // Silent save
    }
  }
}, [])
```

**Tracking Unsaved Changes:**

```javascript
const hasUnsavedChangesRef = useRef(false)

useEffect(() => {
  const hasUserMessages = messages.some(msg => msg.role === "user")
  hasUnsavedChangesRef.current = hasUserMessages && !isSaved
}, [messages, isSaved])
```

### State Management

**States:**
- `isSaved` (boolean): Whether current conversation is saved
- `isSaving` (boolean): Loading state during save
- `hasUnsavedChangesRef` (ref): Tracks if there are unsaved changes

**State Transitions:**
```
New Chat → isSaved = false
Send Message → isSaved = false (mark as unsaved)
Save Chat → isSaved = true
Load Conversation → isSaved = true (already saved)
```

### Sidebar Integration

**Using forwardRef to expose methods:**

```javascript
// ChatSidebar.jsx
const ChatSidebar = forwardRef((props, ref) => {
  useImperativeHandle(ref, () => ({
    loadConversations  // Exposed to parent
  }))
})
```

**Parent calls to refresh sidebar:**

```javascript
// Chatbot.jsx
const sidebarRef = useRef(null)

const saveChatToDatabase = async () => {
  // ... save logic ...
  if (sidebarRef.current) {
    sidebarRef.current.loadConversations() // Refresh list
  }
}
```

## User Experience

### Manual Save Flow

1. User starts chatting
2. Button shows "Save Chat" (enabled)
3. User clicks "Save Chat"
4. Button changes to "Saving..." with spinning icon
5. Success toast: "Chat saved successfully!"
6. Button changes to "Saved" with checkmark (green)
7. Conversation appears in left sidebar
8. Button remains disabled (already saved)

### Auto-Save Flow

1. User starts chatting
2. User navigates to different page (e.g., clicks Dashboard)
3. Component detects unsaved changes
4. Silently saves conversation before unmounting
5. Conversation appears in sidebar next time user visits chatbot
6. No interruption to user's navigation

### Preventing Duplicate Saves

**Scenario 1: User clicks Save twice**
- First click: Saves successfully, sets `isSaved = true`
- Second click: Button is disabled, can't click

**Scenario 2: User saves then navigates away**
- Manual save: Sets `hasUnsavedChangesRef.current = false`
- Auto-save: Checks ref, sees no unsaved changes, skips save

**Scenario 3: Loading saved conversation**
- Loads messages from database
- Sets `isSaved = true` immediately
- Button shows "Saved", auto-save won't trigger

## Visual Design

### Save Button CSS

```css
.save-chat-btn {
  margin-left: auto;           /* Push to right */
  padding: 0.75rem 1.5rem;
  background: #4F46E5;         /* Blue */
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.save-chat-btn.saved {
  background: #10B981;         /* Green when saved */
}

.save-chat-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

### Button Icons

- **Save:** `<FiSave />` - Floppy disk icon
- **Saving:** `<FiSave className="spin" />` - Spinning save icon
- **Saved:** `<FiCheck />` - Checkmark icon

## Error Handling

### Validation Errors

**No messages to save:**
```
Toast Warning: "Need at least one message exchange to save"
```

**Not logged in:**
```
Toast Error: "You must be logged in to save conversations"
```

**Already saved:**
```
Toast Info: "This conversation is already saved"
Button: Disabled with checkmark
```

### Network Errors

**Failed to save:**
```
Toast Error: "Error saving conversation"
Console: Full error logged
State: isSaving = false (re-enable button)
```

## Database Structure

**Saved Conversations:**

```
chat_history table:
- id: 1, 2, 3, 4
- user_id: 1, 1, 1, 1
- conversation_id: "uuid-123", "uuid-123", "uuid-456", "uuid-456"
- chat_title: "What career...", null, "Python dev...", null
- message: "What career...", "Tell me more...", "Python dev...", "Machine learning..."
- reply: "Based on...", "Data science...", "Good choice...", "ML is great..."
- created_at: timestamps
```

**Key Points:**
- Multiple rows with same `conversation_id` = one conversation
- First row has `chat_title`, subsequent rows have `null`
- Title generated from first user message (truncated to 50 chars)

## Testing

### Manual Save Testing

1. **Start new chat:**
   - Send a message
   - Button should show "Save Chat" (blue, enabled)

2. **Click Save:**
   - Button shows "Saving..." briefly
   - Toast: "Chat saved successfully!"
   - Button shows "Saved" (green, disabled)
   - Conversation appears in sidebar

3. **Try to save again:**
   - Button stays disabled
   - Can't click it

4. **Check database:**
   - Open DB Browser
   - View `chat_history` table
   - Should see your messages with same `conversation_id`

### Auto-Save Testing

1. **Start new chat:**
   - Send a message
   - DON'T click Save button

2. **Navigate away:**
   - Click "Dashboard" in navigation
   - No toast (silent save)

3. **Return to Chatbot:**
   - Check left sidebar
   - Your conversation should be there

4. **Verify database:**
   - Messages saved with `conversation_id`

### Duplicate Save Prevention

1. **Save manually:**
   - Click "Save Chat"
   - Wait for success

2. **Navigate away:**
   - Go to Dashboard
   - Check backend logs: No duplicate save

3. **Load saved conversation:**
   - Click conversation in sidebar
   - Button should show "Saved" (disabled)

## Troubleshooting

### Button Not Appearing
- Check if user is logged in (`user` is defined)
- Verify imports: `FiSave`, `FiCheck` from react-icons

### Save Button Always Disabled
- Check `hasMessagesToSave` logic
- Ensure messages array has user messages
- Look for `isSaved` being incorrectly set to true

### Auto-Save Not Working
- Check `hasUnsavedChangesRef.current` value
- Verify cleanup function in useEffect
- Look for console errors

### Conversations Not Appearing in Sidebar
- Check if `sidebarRef.current` exists
- Verify `loadConversations()` is called
- Check network tab for API call

### Duplicate Saves in Database
- Check `hasUnsavedChangesRef` is being cleared
- Verify backend checks for existing conversation
- Look at `conversation_id` in database rows

## Files Modified

**Backend:**
- `blueprints/chatbot_bp.py` - Added save endpoint, disabled auto-save

**Frontend:**
- `services/api.js` - Added `saveConversation()` function
- `pages/Chatbot.jsx` - Added save button, auto-save logic
- `pages/Chatbot.css` - Added save button styles
- `components/chatbot/ChatSidebar.jsx` - Added forwardRef, exposed loadConversations

## Summary

This feature gives users complete control over their chat history:

✅ **Manual Control:** Users decide when to save via button
✅ **Auto-Protection:** Prevents data loss on navigation
✅ **Smart State:** Tracks saved/unsaved status accurately
✅ **Visual Feedback:** Clear button states and icons
✅ **No Duplicates:** Robust duplicate prevention
✅ **Seamless UX:** Integrates smoothly with existing UI

The implementation balances user control with automatic protection, ensuring conversations are saved when needed without being intrusive.

