# 🛡️ Admin Fraud Detection - User Guide

## 🎯 Quick Start

### Step 1: Access the Fraud Detection Dashboard
1. **Login** as admin (e.g., `put your email here`)
2. You'll be redirected to **Admin Dashboard** (`/admin/dashboard`)
3. In the left sidebar, click **"Fraud Detection"** (⚠️ icon)

---

## 📊 Understanding the Dashboard

### Top Section: Statistics Cards

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  Pending Review     │  │  Total Suspicious   │  │  Reviewed           │  │  Flagged Rate       │
│        1            │  │         1           │  │        0            │  │      10.0%          │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

- **Pending Review**: Users flagged but not yet reviewed by admin
- **Total Suspicious**: All users ever flagged as suspicious
- **Reviewed**: Users that have been reviewed (verified/blocked/cleared)
- **Flagged Rate**: Percentage of total users flagged as suspicious

---

### Filter Tabs

```
[ Pending ]  [ Reviewed ]  [ All ]
```

- **Pending**: Show only users awaiting review (default view)
- **Reviewed**: Show users already processed by admins
- **All**: Show all suspicious users regardless of status

---

### User Queue Table

```
┌──────────────────┬───────┬────────────┬──────────────────────┬──────────────┬────────┬────────────┐
│ User Info        │ Role  │ Risk       │ Reason               │ Signed Up    │ Status │ Action     │
├──────────────────┼───────┼────────────┼──────────────────────┼──────────────┼────────┼────────────┤
│ Test User        │ 🎓    │ CRITICAL   │ auto-block-          │ Oct 28, 2025 │ Pending│ View &     │
│ testuser999      │ Student│ 98.69%    │ recommended          │              │        │ Review     │
│ suspicious@...   │       │            │                      │              │        │            │
└──────────────────┴───────┴────────────┴──────────────────────┴──────────────┴────────┴────────────┘
```

#### Risk Badge Colors
- 🟢 **Low** (< 40%): Green - Likely legitimate
- 🟡 **High** (40-80%): Yellow - Needs review
- 🔴 **Critical** (> 80%): Red - High fraud risk

#### Reason Badges
- `auto-allow`: Passed fraud check (won't appear in queue)
- `auto-review-required`: Medium risk, manual review needed
- `auto-block-recommended`: High risk, should be blocked

---

## 🔍 Reviewing a Suspicious User

### Click "View & Review" Button

A modal opens with detailed information:

```
┌─────────────────────────────────────────────────────────────┐
│  Review Fraud Case: suspicious@tempmail.com                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Information:                                          │
│  • Email: suspicious@tempmail.com                           │
│  • Username: testuser999                                    │
│  • Full Name: Test User                                     │
│  • Role: Student                                            │
│  • Signed Up: Oct 28, 2025 11:03 AM                        │
│                                                             │
│  Fraud Detection:                                           │
│  • Risk Score: 98.69% [ CRITICAL ]                         │
│  • Reason: auto-block-recommended                           │
│  • Checked At: Oct 28, 2025 11:03 AM                       │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Admin Notes (optional):                               │ │
│  │ ┌───────────────────────────────────────────────────┐ │ │
│  │ │ This user signed up with a disposable email...    │ │ │
│  │ │                                                    │ │ │
│  │ └───────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Actions:                                                   │
│  [ Verify as Legitimate ]  [ Block Account ]  [ Clear Flag ]│
│                                                             │
│  [ Cancel ]                                   [ Submit ]    │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚖️ Admin Actions Explained

### 1. ✅ Verify as Legitimate
**When to use**: User appears safe after manual review

**What happens**:
- Sets `is_suspicious = False`
- Sets `fraud_reason = "admin-verified"`
- Records your admin ID and notes
- User removed from pending queue
- User can use platform normally

**Example**: User has legitimate email but unusual username pattern

---

### 2. 🚫 Block Account
**When to use**: User is confirmed fraudulent/malicious

**What happens**:
- Keeps `is_suspicious = True`
- Sets `permissions = "blocked"`
- Sets `fraud_reason = "admin-blocked"`
- Records your admin ID and notes
- User stays in queue (as reviewed)
- **User cannot login** (blocked status)

**Example**: Bot account, spam account, clearly fake profile

---

### 3. 🔄 Clear Flag
**When to use**: False positive, user is clearly safe

**What happens**:
- Sets `is_suspicious = False`
- Sets `fraud_reason = "admin-cleared"`
- Records your admin ID and notes
- User removed from pending queue
- User can use platform normally

**Example**: ML model incorrectly flagged a legitimate user

---

## 📋 Review Workflow Example

### Scenario: New suspicious signup detected

1. **Email**: `suspicious@tempmail.com`
2. **Risk**: 98.69% (CRITICAL)
3. **Reason**: auto-block-recommended

### Admin's Investigation:
```
✓ Check email domain → tempmail.com (disposable email service)
✓ Check username → testuser999 (generic pattern)
✓ Check signup IP → Same IP as 10 other recent signups
✓ Decision: BLOCK ACCOUNT
```

### Admin Actions:
1. Click **"View & Review"**
2. Add note: "Disposable email + suspicious pattern + bot-like behavior"
3. Select **"Block Account"**
4. Click **"Submit"**

### Result:
- User blocked from logging in
- Moved to "Reviewed" tab
- Admin action logged in `/admin/logs`
- Statistics updated

---

## 📊 Monitoring Tips

### Daily Checks
1. Check **Pending Review** count on dashboard
2. Review high-risk users (CRITICAL badge) first
3. Look for patterns (same IP, similar usernames, etc.)

### Weekly Analysis
1. Go to **Fraud Stats** card
2. Check flagged rate percentage
3. If > 20%, model might need retuning
4. If < 2%, thresholds might be too strict

### Red Flags to Watch For
- 🚩 Disposable email domains (`@tempmail.com`, `@10minutemail.com`)
- 🚩 Very short usernames (`aa`, `bb`, `test`)
- 🚩 Admin-like names (`admin`, `root`, `superadmin`)
- 🚩 Multiple signups from same IP
- 🚩 Non-Latin characters in username (unusual for your region)
- 🚩 Email and username completely unrelated

---

## 🎓 Real-World Examples

### Case 1: Legitimate User (False Positive)
```
Email: john.smith.jr@gmail.com
Username: jsmith_jr
Risk: 45% (HIGH)
Reason: auto-review-required

Admin Review: Real person, verified email, normal pattern
Action: ✅ Verify as Legitimate
```

### Case 2: Bot Account
```
Email: xyz123@mailinator.com
Username: user98765
Risk: 99.2% (CRITICAL)
Reason: auto-block-recommended

Admin Review: Disposable email, generic username, no real name
Action: 🚫 Block Account
```

### Case 3: Spam Account
```
Email: clickhere@freemoney.com
Username: admin2024
Risk: 87% (CRITICAL)
Reason: auto-block-recommended

Admin Review: Suspicious domain, admin-like username
Action: 🚫 Block Account
```

---

## 🔧 Advanced Features

### Bulk Review (Future Enhancement)
Currently: Review one user at a time  
Planned: Select multiple users and apply action

### Auto-Block (Future Enhancement)
Currently: All suspicious users need manual review  
Planned: Auto-block if risk > 95%

### Email Notifications (Future Enhancement)
Currently: No notifications  
Planned: Email admin when critical risk user signs up

---

## 📞 Troubleshooting

### "No suspicious users" showing?
- Fraud detection only works on **NEW signups**
- Existing users before integration won't be flagged
- Try creating a test account with `@tempmail.com` email

### Admin count showing 0?
- Hard refresh page (Ctrl+F5)
- Clear browser cache
- Re-login to get fresh data

### Fraud detection not working?
1. Check backend logs for errors
2. Verify `ml_models/signup_risk_model.joblib` exists
3. Ensure `pandas` is installed
4. Check `.env` has `FRAUD_MODEL_PATH` set

---

## 📈 Success Metrics

**After 1 Week**:
- Track how many users flagged
- Track admin review accuracy (re-check blocked users)
- Adjust thresholds if needed

**After 1 Month**:
- Calculate false positive rate
- Retrain model with new data
- Update blacklists/whitelists

---

## 🎯 Best Practices

1. ✅ **Review within 24 hours** of signup
2. ✅ **Always add notes** for future reference
3. ✅ **Check for patterns** across multiple users
4. ✅ **Log suspicious IPs** for future blocking
5. ✅ **Monitor flagged rate** weekly
6. ⚠️ **Don't auto-block** without review (false positives happen)
7. ⚠️ **Don't ignore CRITICAL flags** (high accuracy)

---

**Dashboard Access**: `/admin/fraud`  
**Backend Endpoints**: `/api/admin/fraud/*`  
**Model Location**: `ml_models/signup_risk_model.joblib`

---

🛡️ **Keep your platform safe!** 🛡️

