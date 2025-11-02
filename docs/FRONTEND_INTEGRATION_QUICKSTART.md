# Frontend Integration Quick Start

## 🚀 Quick Start Guide

This guide will help you test the newly integrated JWT authentication system.

---

## Prerequisites

1. **Backend Running:** Flask server on port 5000
2. **Frontend Running:** Vite dev server on port 5173
3. **SMTP Configured:** Email verification requires SMTP credentials

---

## Step 1: Configure SMTP (Optional but Recommended)

Create or update `.env` file in `careersuggestion_Backend`:

```bash
# Required for email verification
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password

# Required for AI features
GROQ_API_KEY=your-groq-api-key

# Optional (defaults provided)
JWT_SECRET_KEY=your-super-secret-jwt-key
```

### **Gmail App Password Setup:**
1. Go to Google Account Settings
2. Enable 2-Factor Authentication
3. Generate App Password: https://myaccount.google.com/apppasswords
4. Use generated password in `.env`

---

## Step 2: Start Backend

```bash
cd careersuggestion_Backend
python app.py
```

**Expected Output:**
```
✅ Database initialized successfully.
✅ LLM Service initialized successfully.
✅ All blueprints registered successfully (including admin panel).
 * Running on http://127.0.0.1:5000
```

**Test Backend:**
```bash
curl http://localhost:5000/
```

Should return JSON with version 2.0.0 and JWT authentication info.

---

## Step 3: Start Frontend

```bash
cd careersuggestion_Frontend
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Open in Browser:**
http://localhost:5173/

---

## Step 4: Test Signup Flow

### **A. Create New Account**

1. Click "Sign Up" on homepage
2. Fill in form:
   - **Name:** John Doe
   - **Email:** john@example.com
   - **Username:** johndoe (optional, auto-generated if empty)
   - **Password:** password123
   - **Confirm Password:** password123
3. Click "Create Account"

### **B. Expected Result:**

✅ Success toast: "Account created successfully! Please verify your email."
✅ Redirect to `/verify-email`
✅ JWT token stored in localStorage
✅ Verification code sent to email (if SMTP configured)

### **C. Verify Email (If SMTP Configured):**

1. Check email inbox for 6-digit code
2. Enter code in verification page
3. Click "Verify Email"
4. Success! Redirect to dashboard

### **D. Skip Verification (For Testing):**

If SMTP not configured, manually verify in database:

**Option 1 - Python Script:**
```python
# In careersuggestion_Backend directory
from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(email='john@example.com').first()
    user.is_verified = True
    db.session.commit()
    print(f"✅ {user.email} verified!")
```

**Option 2 - SQLite Command:**
```bash
cd careersuggestion_Backend/instance
sqlite3 course_recommendation.db
```
```sql
UPDATE users SET is_verified = 1 WHERE email = 'john@example.com';
SELECT email, is_verified FROM users WHERE email = 'john@example.com';
.exit
```

Then refresh `/dashboard` in browser.

---

## Step 5: Test Login Flow

### **A. Logout First:**
Click user menu → Logout

### **B. Login:**
1. Click "Sign In"
2. Enter:
   - **Email:** john@example.com (or johndoe username works too!)
   - **Password:** password123
3. Click "Sign In"

### **C. Expected Result:**

✅ Success toast: "Login successful!"
✅ JWT token stored in localStorage
✅ If verified → Redirect to `/dashboard`
✅ If not verified → Redirect to `/verify-email`

---

## Step 6: Test Protected Features

### **A. Chatbot:**
1. Navigate to "AI Chatbot"
2. Send message: "What career paths are available in software engineering?"
3. Should work with JWT authentication

**Check Developer Console:**
```
Network tab → chatbot/message → Headers → Authorization: Bearer <token>
```

### **B. Career Suggester:**
1. Navigate to "Career Suggester"
2. Answer questions
3. Save session (requires JWT)

### **C. Course Recommender:**
1. Navigate to "Course Recommender"
2. Search for courses
3. Get AI recommendations

---

## Step 7: Test Token Expiry

### **A. Simulate Expired Token:**

**In Browser Console:**
```javascript
// Clear token
localStorage.removeItem('jwt_token')
// Try making API call
```

### **B. Expected Result:**

✅ 401 response from backend
✅ Auto-logout triggered
✅ Redirect to `/login`
✅ Toast: "Session expired. Please login again."

---

## Step 8: Test Admin Features (Optional)

### **A. Create Admin User:**

By default, first user (ID=1) is admin after migration. Or manually set:

```python
from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(email='john@example.com').first()
    user.role = 'admin'
    db.session.commit()
    print(f"✅ {user.email} is now admin!")
```

### **B. Test Admin Endpoints:**

**Using curl:**
```bash
# Login first to get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Copy access_token from response, then:
TOKEN="<your-token-here>"

# Get all users
curl http://localhost:5000/api/admin/users \
  -H "Authorization: Bearer $TOKEN"

# Get stats
curl http://localhost:5000/api/admin/stats \
  -H "Authorization: Bearer $TOKEN"
```

**Using Browser (if logged in as admin):**
- Open Network tab
- Call admin endpoints from Console:
```javascript
fetch('/api/admin/users', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }
}).then(r => r.json()).then(console.log)
```

---

## Troubleshooting

### **Issue 1: "Network error" toast**
**Cause:** Backend not running
**Fix:** Start Flask server on port 5000

### **Issue 2: "Authorization header missing"**
**Cause:** Token not stored or expired
**Fix:** Login again to get fresh token

### **Issue 3: Email not sending**
**Cause:** SMTP credentials missing or incorrect
**Fix:** 
1. Check `.env` file has `SMTP_USERNAME` and `SMTP_PASSWORD`
2. For Gmail, use App Password (not regular password)
3. Enable "Less secure app access" (if using old method)

### **Issue 4: CORS errors**
**Cause:** Frontend proxy not configured
**Fix:** Check `vite.config.js` has:
```javascript
server: {
  proxy: {
    '/api': 'http://localhost:5000'
  }
}
```

### **Issue 5: 401 errors on every API call**
**Cause:** Invalid JWT secret mismatch
**Fix:** 
1. Check backend `.env` has `JWT_SECRET_KEY`
2. Restart backend after changing `.env`
3. Login again to get new token

### **Issue 6: Verification code expired**
**Cause:** Code valid for only 10 minutes
**Fix:** Click "Resend Code" button (60s cooldown)

---

## Quick Testing Commands

### **Check Backend Health:**
```bash
curl http://localhost:5000/
```

### **Test Signup (No Frontend):**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "username": "testuser"
  }'
```

### **Test Login (No Frontend):**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### **Test Protected Endpoint:**
```bash
TOKEN="<your-jwt-token>"

curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## Database Inspection

### **View Users:**
```bash
cd careersuggestion_Backend/instance
sqlite3 course_recommendation.db
```
```sql
SELECT id, email, username, role, is_verified, created_at FROM users;
.exit
```

### **View Admin Logs:**
```sql
SELECT admin_id, action, target_user_id, timestamp FROM admin_logs ORDER BY timestamp DESC LIMIT 10;
.exit
```

---

## Success Indicators

✅ **Backend:**
- No errors on startup
- JWT endpoints registered
- Admin panel registered

✅ **Frontend:**
- Signup creates user + returns JWT
- Login returns JWT + user
- Protected routes require login
- Token auto-refresh or logout on expiry
- Email verification flow works

✅ **Integration:**
- All API calls include `Authorization: Bearer <token>` header
- 401 responses trigger auto-logout
- User data + token persists across page refreshes
- Role-based navigation works

---

## Next Steps

1. ✅ Test signup flow
2. ✅ Test email verification (or skip in dev)
3. ✅ Test login flow
4. ✅ Test protected features (chatbot, suggester, recommender)
5. ✅ Test token expiry handling
6. ✅ Test admin endpoints (if admin user)
7. ✅ Test logout and re-login

**Happy Testing! 🎉**

If everything works, you now have a fully integrated JWT-authenticated career guidance platform with email verification, role-based access, and all AI features preserved!

