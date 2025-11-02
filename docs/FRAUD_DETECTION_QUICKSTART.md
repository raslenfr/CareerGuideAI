# Fraud Detection - Quick Start Guide

## ✅ Installation Complete!

Your ML fraud detection model has been integrated. Here's how to use it:

---

## 🚀 Run the Application

### Backend:
```bash
cd C:\Users\MSI\Desktop\course-recommendation-main\careersuggestion_Backend
.\.venv\Scripts\python.exe app.py
```

✅ **Look for these logs:**
```
INFO - Fraud detection model loaded from ml_models/signup_risk_model.joblib
INFO - Fraud thresholds loaded: REVIEW=0.4, BLOCK=0.8
INFO - Feature names loaded: 10 features
```

### Frontend:
```bash
cd C:\Users\MSI\Desktop\course-recommendation-main\careersuggestion_Frontend
npm run dev
```

---

## 🧪 Quick Test

### 1. Create a **Legitimate Signup:**
- Name: `John Smith`
- Email: `john.smith@gmail.com`
- Username: `johnsmith`
- Password: `password123`

**Expected:** ✅ Low risk score (< 0.4), `is_suspicious = False`

---

### 2. Create a **Suspicious Signup:**
- Name: `Test Admin`
- Email: `test123@yopmail.com`
- Username: `testadmin`
- Password: `password123`

**Expected:** ⚠️ High risk score (≥ 0.4), `is_suspicious = True`

**Why flagged?**
- Disposable email (`yopmail.com`)
- Blacklisted words (`test`, `admin`)
- High digits in email

---

## 👨‍💼 Admin Review

### 1. **Login as Admin:**
- Email: `put your email here`
- Role: Select "Admin Account"
- Password: Your password

### 2. **Navigate to Fraud Detection:**
Click **"Fraud Detection"** in the admin sidebar (⚠️ icon)

### 3. **Review Suspicious Users:**
- View pending queue
- Check risk scores
- Click "View & Review" button
- Add notes and choose action:
  - ✅ **Verify** - Mark as legitimate
  - 🚫 **Block** - Disable account
  - 🔄 **Clear** - Remove flag

---

## 📊 Fraud Statistics

**URL:** http://127.0.0.1:5000/api/admin/fraud/stats

Shows:
- Total suspicious signups
- Pending reviews
- Reviewed count
- Average risk score
- Breakdown by role and reason

---

## ⚙️ Adjust Sensitivity

Edit `.env` to change thresholds:

```env
# More strict (flag more users):
FRAUD_THRESHOLD_REVIEW=0.3

# Less strict (flag fewer users):
FRAUD_THRESHOLD_REVIEW=0.5
```

---

## 🎯 What Gets Flagged?

### **Red Flags (High Risk):**
- ✘ Disposable email domains (yopmail, tempmail, etc.)
- ✘ Blacklisted words (test, admin, root, hack, etc.)
- ✘ Random character patterns
- ✘ High digits in email
- ✘ Non-Latin characters

### **Green Flags (Low Risk):**
- ✓ Known email providers (Gmail, Yahoo, Outlook)
- ✓ Real-looking names
- ✓ Normal username patterns
- ✓ Email/username similarity

---

## 📍 API Endpoints

### **Admin Only:**
- `GET /api/admin/fraud/queue` - List suspicious signups
- `GET /api/admin/fraud/stats` - Statistics
- `POST /api/admin/fraud/review/<user_id>` - Review user

### **Automatic (on signup):**
- Fraud detection runs on `POST /api/auth/signup`

---

## ✨ Key Features

✅ **Automatic:** Runs on every signup
✅ **Non-blocking:** Never prevents signups
✅ **ML-powered:** Uses your trained model
✅ **Admin review:** Human in the loop
✅ **Audit trail:** All actions logged
✅ **Real-time stats:** Monitor fraud trends

---

## 🔧 Configuration Files

- **Model:** `ml_models/signup_risk_model.joblib`
- **Thresholds:** `ml_models/signup_risk_thresholds.json`
- **Features:** `ml_models/feature_names.json`
- **Config:** `.env` (FRAUD_* variables)

---

## 📈 Monitor Performance

Check stats regularly:
1. Login as admin
2. Go to **Fraud Detection**
3. Review **Statistics** cards:
   - Pending Review
   - Total Suspicious
   - Flagged Rate

Adjust thresholds if:
- Too many false positives → Increase `FRAUD_THRESHOLD_REVIEW`
- Missing obvious spam → Decrease `FRAUD_THRESHOLD_REVIEW`

---

## 🎉 You're All Set!

Your fraud detection system is live and protecting your platform!

**Need help?** Check `FRAUD_DETECTION_INTEGRATION_SUMMARY.md` for detailed documentation.

