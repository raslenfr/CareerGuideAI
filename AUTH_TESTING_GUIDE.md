# Authentication Testing Guide

## Setup Verification

### 1. Check Requirements
Make sure all dependencies are installed:
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
cd Backend
python app.py
```

You should see:
```
Database tables created successfully.
Blueprints registered successfully.
Starting Flask development server...
```

### 3. Verify Database File
Check that the SQLite database was created:
- Location: `Backend/instance/course_recommendation.db`
- If it doesn't exist, the server will create it on first run

## Testing Authentication

### Option 1: Using the Test Script
```bash
cd Backend
python test_auth.py
```

This will automatically test:
- Backend connectivity
- User signup
- User login (correct password)
- User login (wrong password)

### Option 2: Manual Testing with curl

**Test Signup:**
```bash
curl -X POST http://127.0.0.1:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"mypassword123"}'
```

Expected response:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-01T12:00:00"
  },
  "message": "Account created successfully"
}
```

**Test Login:**
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"mypassword123"}'
```

Expected response:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-01T12:00:00"
  },
  "message": "Login successful"
}
```

### Option 3: Test via Frontend

1. Start Backend (port 5000):
```bash
cd Backend
python app.py
```

2. Start Frontend (port 5173):
```bash
cd Frontend
npm run dev
```

3. Open browser to http://localhost:5173
4. Click "Sign Up" and create an account
5. Try logging in with your new credentials

## View Database Contents

### Using DB Browser for SQLite (Recommended)

1. Download: https://sqlitebrowser.org/
2. Open `Backend/instance/course_recommendation.db`
3. Browse Data → Select "users" table
4. You'll see all registered users with:
   - id
   - email
   - password_hash (encrypted)
   - name
   - created_at

### Using Python
```python
import sqlite3

conn = sqlite3.connect('instance/course_recommendation.db')
cursor = conn.cursor()

# View all users
cursor.execute("SELECT id, email, name, created_at FROM users")
for row in cursor.fetchall():
    print(row)

conn.close()
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'flask_sqlalchemy'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"
**Solution:** Port 5000 is taken. Kill the process or change port in app.py

### Issue: "CORS error" in browser
**Solution:** Make sure Flask-CORS is installed and CORS is enabled in app.py (already configured)

### Issue: Cannot connect to backend from frontend
**Solution:** 
1. Check backend is running on port 5000
2. Check vite.config.js has proxy configured
3. Try accessing http://127.0.0.1:5000/ directly in browser

### Issue: Login/Signup buttons don't work
**Solution:** 
1. Open browser console (F12)
2. Check Network tab for API calls
3. Look for errors in Console tab
4. Verify backend logs for errors

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL
);
```

### Chat History Table
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    reply TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Saved Courses Table
```sql
CREATE TABLE saved_courses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    course_title VARCHAR(255) NOT NULL,
    provider VARCHAR(100),
    description TEXT,
    url VARCHAR(500),
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Security Notes

- ✅ Passwords are hashed using bcrypt (never stored in plain text)
- ✅ Email addresses are stored in lowercase for consistency
- ✅ User input is validated before database operations
- ✅ SQL injection is prevented by SQLAlchemy ORM
- ⚠️ For production: Add rate limiting, JWT tokens, and email verification

