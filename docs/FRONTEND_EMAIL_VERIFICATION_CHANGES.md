# Frontend Email Verification Changes Guide

**Date**: October 28, 2025  
**Purpose**: Restore email verification requirement and update signup flow

---

## 🎯 Overview

These changes restore mandatory email verification for new signups and update the user flow to redirect to login instead of auto-login after signup.

---

## ✅ Backend Changes (COMPLETED)

The following backend changes have been implemented:

### 1. Signup Endpoint (`/api/auth/signup`)
- ✅ Generates 6-digit verification code
- ✅ Saves code to `user.verification_code`
- ✅ Saves timestamp to `user.verification_sent_at`
- ✅ Sends verification email
- ✅ Returns success without JWT token
- ✅ Response includes message: "Account created! Verification code sent to your email. Please verify before logging in."

### 2. Login Endpoint (`/api/auth/login`)
- ✅ Checks if `user.is_verified === false`
- ✅ Returns 403 error if not verified
- ✅ Error response includes `requires_verification: true` flag
- ✅ Allows login only for verified users

### 3. Verify Email Endpoint (`/api/auth/verify-email`)
- ✅ Verifies the code
- ✅ Marks user as verified
- ✅ Returns message: "Email verified successfully! You can now login."
- ✅ Includes `redirect_to_login: true` flag

---

## 📝 Frontend Changes Required

### File 1: `careersuggestion_Frontend/src/pages/Signup.jsx`

**Location**: Find the signup form component  
**Changes**:

```jsx
// In handleSubmit function, after successful signup:

const handleSubmit = async (e) => {
  e.preventDefault();
  
  try {
    const response = await signupUser({
      name,
      email,
      password,
      username, // optional
      role // 'student' or 'admin'
    });
    
    if (response.success) {
      // DON'T call login() from AuthContext
      // DON'T store token or user in localStorage
      
      // Show success message
      alert(response.message || "Account created! Please check your email to verify your account, then login.");
      
      // Redirect to login page
      navigate('/login');
    }
  } catch (error) {
    // Handle error
    setError(error.message || "Signup failed");
  }
};
```

**Key Points**:
- ❌ Remove: `login(response.access_token, response.user)`
- ❌ Remove: Auto-redirect to dashboard
- ✅ Add: `navigate('/login')`
- ✅ Add: Success message display

---

### File 2: `careersuggestion_Frontend/src/pages/Login.jsx`

**Location**: Find the login form component  
**Changes**:

```jsx
// In handleSubmit function:

const handleSubmit = async (e) => {
  e.preventDefault();
  setError('');
  
  try {
    const response = await loginUser({ email, password, role }); // role is optional
    
    if (response.success) {
      // Login successful and user is verified
      login(response.access_token, response.user);
      
      // Redirect based on role
      if (response.user.role === 'admin') {
        navigate('/admin/dashboard');
      } else {
        navigate('/dashboard');
      }
    }
  } catch (error) {
    // Check if error is due to unverified email
    if (error.requires_verification) {
      // Store user email for verification page
      localStorage.setItem('pending_verification_email', error.user?.email || email);
      
      // Show message
      setError(error.message || "Please verify your email before logging in");
      
      // Redirect to verify-email page after 2 seconds
      setTimeout(() => {
        navigate('/verify-email');
      }, 2000);
    } else {
      // Other login errors
      setError(error.message || "Login failed");
    }
  }
};
```

**Key Points**:
- ✅ Check for `error.requires_verification` flag
- ✅ Redirect unverified users to `/verify-email`
- ✅ Show appropriate error messages
- ✅ Keep role-based dashboard routing

---

### File 3: `careersuggestion_Frontend/src/pages/VerifyEmail.jsx`

**Location**: Find the email verification page  
**Changes**:

```jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { sendVerificationCode, verifyEmail } from '../services/api';

const VerifyEmail = () => {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [codeSent, setCodeSent] = useState(false);
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  // Auto-send verification code on mount if user is logged in and not verified
  useEffect(() => {
    if (isAuthenticated && user && !user.is_verified) {
      handleSendCode();
    } else if (!isAuthenticated) {
      // User not logged in, they might be coming from failed login
      // Allow manual code entry for pending verification
      const pendingEmail = localStorage.getItem('pending_verification_email');
      if (!pendingEmail) {
        // No pending verification, redirect to login
        navigate('/login');
      }
    }
  }, [isAuthenticated, user]);

  const handleSendCode = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await sendVerificationCode();
      if (response.success) {
        setSuccess('Verification code sent to your email!');
        setCodeSent(true);
      }
    } catch (err) {
      setError(err.message || 'Failed to send verification code');
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    if (!code || code.length !== 6) {
      setError('Please enter the 6-digit code');
      setLoading(false);
      return;
    }
    
    try {
      const response = await verifyEmail({ code });
      
      if (response.success) {
        setSuccess('Email verified successfully! Redirecting to login...');
        
        // Clear pending verification email
        localStorage.removeItem('pending_verification_email');
        
        // Redirect to login after 2 seconds
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      }
    } catch (err) {
      setError(err.message || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="verify-email-container">
      <div className="verify-email-card">
        <h2>Verify Your Email</h2>
        
        {!isAuthenticated && (
          <p className="info-text">
            Please check your email for the verification code.
          </p>
        )}
        
        {user && !user.is_verified && (
          <>
            <p className="email-display">Email: {user.email}</p>
            
            {!codeSent && (
              <button onClick={handleSendCode} disabled={loading}>
                {loading ? 'Sending...' : 'Send Verification Code'}
              </button>
            )}
          </>
        )}
        
        {(codeSent || !isAuthenticated) && (
          <form onSubmit={handleVerify}>
            <div className="input-group">
              <label>Verification Code</label>
              <input
                type="text"
                maxLength="6"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Enter 6-digit code"
                required
              />
            </div>
            
            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">{success}</p>}
            
            <button type="submit" disabled={loading || !code || code.length !== 6}>
              {loading ? 'Verifying...' : 'Verify Email'}
            </button>
          </form>
        )}
        
        {codeSent && (
          <p className="resend-text">
            Didn't receive the code?{' '}
            <button onClick={handleSendCode} className="link-button" disabled={loading}>
              Resend Code
            </button>
          </p>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail;
```

**Key Points**:
- ❌ Remove: "Verify Your Email (Optional)" title
- ❌ Remove: "Skip this" link
- ✅ Add: Title "Verify Your Email" (required)
- ✅ Add: Auto-send code on mount if authenticated
- ✅ Add: Redirect to `/login` after successful verification
- ✅ Add: Handle non-authenticated state (pending verification from failed login)

---

### File 4: `careersuggestion_Frontend/src/context/AuthContext.jsx`

**Location**: Find the `register` function  
**Changes**:

```jsx
const register = async (userData) => {
  try {
    const response = await signupUser(userData);
    
    if (response.success) {
      // DON'T auto-login after signup
      // DON'T store token or user in localStorage
      
      // Just return success
      return {
        success: true,
        message: response.message
      };
    }
  } catch (error) {
    throw error;
  }
};
```

**Key Points**:
- ❌ Remove: `setUser(response.user)`
- ❌ Remove: `localStorage.setItem('user', JSON.stringify(response.user))`
- ❌ Remove: `localStorage.setItem('jwt_token', response.access_token)`
- ✅ Keep: Return success status for signup form to handle redirect

---

### File 5: `careersuggestion_Frontend/src/services/api.js`

**Location**: Update the `loginUser` function  
**Changes**:

```jsx
export const loginUser = async (credentials) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials)
    });

    const data = await response.json();

    if (response.status === 403 && data.requires_verification) {
      // User needs to verify email
      throw {
        requires_verification: true,
        message: data.error,
        user: data.user
      };
    }

    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }

    return data;
  } catch (error) {
    throw error;
  }
};

export const signupUser = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Signup failed');
    }

    return data;
  } catch (error) {
    throw error;
  }
};
```

**Key Points**:
- ✅ Add: Special handling for 403 status with `requires_verification` flag
- ✅ Add: Throw custom error object with verification flag
- ✅ Update: Remove token from signup response handling

---

## 🔄 Updated User Flow

### NEW Flow (After Changes):

```
1. User visits /signup
   ↓
2. Fills form (name, email, password, role)
   ↓
3. Submits → Backend creates user (is_verified=false)
   ↓
4. Backend sends verification email with 6-digit code
   ↓
5. Frontend shows: "Account created! Check your email"
   ↓
6. Frontend redirects to /login
   ↓
7. User tries to login
   ↓
8. Backend checks is_verified → false
   ↓
9. Backend returns 403: "Please verify email"
   ↓
10. Frontend redirects to /verify-email
    ↓
11. User enters 6-digit code
    ↓
12. Backend marks is_verified=true
    ↓
13. Frontend shows: "Email verified! You can now login"
    ↓
14. Frontend redirects to /login
    ↓
15. User logs in again
    ↓
16. Backend checks is_verified → true ✅
    ↓
17. Login successful → Redirect to dashboard
```

---

## 🧪 Testing Checklist

### Test 1: New Signup Flow
- [ ] Signup with new account
- [ ] Verify "Account created" message appears
- [ ] Verify email is sent with 6-digit code
- [ ] Verify redirect to /login
- [ ] Verify NO auto-login occurs

### Test 2: Unverified Login Attempt
- [ ] Try to login before verifying email
- [ ] Verify error message: "Please verify your email before logging in"
- [ ] Verify redirect to /verify-email page

### Test 3: Email Verification
- [ ] Visit /verify-email
- [ ] Enter 6-digit code from email
- [ ] Verify success message appears
- [ ] Verify redirect to /login

### Test 4: Verified Login
- [ ] Login after email verification
- [ ] Verify successful login
- [ ] Verify redirect to correct dashboard (admin/student)

### Test 5: Existing Users
- [ ] Existing verified users can login normally
- [ ] No disruption to current user accounts

---

## ⚠️ Important Notes

1. **Fraud Detection**: All fraud detection logic remains intact during signup
2. **Role Selection**: Signup still allows choosing between Student and Admin roles
3. **JWT Tokens**: Still generated on login (not on signup)
4. **Dashboard Routing**: Admin → `/admin/dashboard`, Student → `/dashboard`
5. **Existing Users**: Already verified users (is_verified=true) can login immediately

---

## 🛠️ Implementation Steps

1. **Open Frontend Project**:
   ```bash
   cd ../careersuggestion_Frontend
   ```

2. **Update Files in Order**:
   - [ ] Update `src/context/AuthContext.jsx`
   - [ ] Update `src/services/api.js`
   - [ ] Update `src/pages/Signup.jsx`
   - [ ] Update `src/pages/Login.jsx`
   - [ ] Update `src/pages/VerifyEmail.jsx`

3. **Test Each Step**:
   - Test signup flow
   - Test login with unverified account
   - Test email verification
   - Test login with verified account

4. **Verify Integration**:
   - Backend is already updated ✅
   - Frontend changes will complete the flow

---

## 📞 Support

If you encounter issues:
1. Check browser console for errors
2. Check backend logs for API errors
3. Verify `.env` has SMTP credentials set (for email sending)
4. Test with a real email address to receive verification codes

---

**Backend Status**: ✅ **COMPLETE**  
**Frontend Status**: ⏳ **AWAITING IMPLEMENTATION**

Apply these changes to complete the email verification requirement!

