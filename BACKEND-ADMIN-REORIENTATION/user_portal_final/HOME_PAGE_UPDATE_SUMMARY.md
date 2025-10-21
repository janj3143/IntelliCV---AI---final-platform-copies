# Home Page Update Summary
**Date:** October 21, 2025  
**File:** `pages/00_Home.py`

## ✅ Updates Completed

### 1. Logo Sizing - UPDATED ✅
- **Changed:** Logo now displays at **60% width** on home page (was 90%)
- **Implementation:** `style="width: 60%; max-height: 400px;"`
- **Note:** Other pages will maintain 30% logo width as specified

### 2. Pricing Structure - COMPLETELY REVISED ✅
Updated from 3 tiers to **4 comprehensive pricing tiers**:

#### 🆓 **Free Plan** (Token-Based)
- Upload CV (data collection priority!)
- Profile access
- Limited Chatbot
- Basic AI from Career Intelligence Suite
- Truncated career options
- **Button:** Redirects to `pages/02_Payment.py`

#### ⭐ **Monthly Plan - $9.99/month**
- All Free features
- Increased AI options
- More career intelligence
- ❌ No Career Coach
- ❌ No Interview Coach
- ❌ No Multi-CV autogenerate & send
- **Button:** Redirects to `pages/02_Payment.py`

#### 🏆 **Annual Plan - $149.99/year** (Featured)
- All Monthly features
- ✅ Career Coach
- ✅ Interview Coach
- ✅ Multi-CV autogenerate & send functionality
- ✅ Full Career Intelligence Suite
- ❌ No Mentorship Support
- **Button:** Redirects to `pages/02_Payment.py`

#### 👑 **Super-User Plan - $299/year**
- Everything in Annual Plan
- ✅ **1-on-1 Mentorship Access** (KEY DIFFERENTIATOR)
- ✅ Connect with industry mentors
- ✅ Personalized career guidance
- 💡 **Mentor Revenue Share Model:**
  - Mentors incentivized to participate
  - Mentors receive cut of mentorship annual fee
  - Mentors can charge for services (20% platform fee to IntelliCV-AI)
  - All mentor arrangements must be approved through platform
- **Button:** Redirects to `pages/02_Payment.py`

### 3. Registration Flow - UPDATED ✅
- All pricing plan buttons now redirect to **`pages/02_Payment.py`**
- Matches your specification: "new registrations directed to payment page"
- Session state tracks selected plan: `st.session_state['selected_plan']`

### 4. Footer Enhancement - ADDED ✅
- Added payment integration note:
  - "Payment powered by Stripe, Google Pay, and more"
  - "Admin portal integration"
- Confirms connection to admin_portal payment complexity

### 5. Documentation - UPDATED ✅
- Updated module docstring to reflect:
  - Entry point status (00_Home.py)
  - Logo sizing (60% home, 30% other pages)
  - Four-tier pricing structure
  - Mentorship revenue share model
  - Payment system integrations

## 🎯 Key Features Implemented

### Entry Point Architecture
- **00_Home.py** = Primary entry point to system
- **Logo:** 60% width (static display)
- **Content:** Welcome, USPs, Login/Registration, Pricing
- **Flow:** User selects plan → Redirects to Payment (02_Payment.py)

### Login/Registration Integration
- ✅ Login form with demo credentials
- ✅ Registration button redirects to payment
- ✅ Session management for authenticated users
- ✅ Quick action buttons for logged-in users

### Payment Integration Notes
- 🔗 Links to **admin_portal** payment systems
- 💳 Stripe integration (primary)
- 📱 Google Pay support (as specified)
- 🎯 Admin portal handles payment complexity
- 🖥️ User sees clean, standard payment interface

## 📋 What Users See (Home Page Experience)

1. **Welcome Header** - "Welcome to IntelliCV-AI"
2. **Large Logo** - 60% width, prominent display
3. **Key USPs** - 6 core benefits in clean bullets
4. **Login/Registration Card** - Right-side panel
5. **Four Pricing Tiers** - Side-by-side comparison
6. **Footer** - Security, availability, support info

## 🔄 User Journey Flow

```
00_Home.py (Entry Point)
    ↓
[User selects plan]
    ↓
02_Payment.py (Payment processing)
    ↓
[Payment completed]
    ↓
03_Profile_Setup.py ("Profile and tell us about you")
    ↓
[Profile completed or skipped]
    ↓
05_Resume_Upload.py (Upload CV or update existing)
```

## 🎨 Visual Layout

```
┌─────────────────────────────────────────────────┐
│         🚀 Welcome to IntelliCV-AI              │
│    Transform Your Career with Intelligent       │
│           Resume Technology                      │
├──────────┬──────────────────┬──────────────────┤
│   LOGO   │   6 KEY USPs     │  LOGIN/REGISTER  │
│  (60%)   │   • AI-Powered   │   [Login Form]   │
│          │   • Smart Match  │   [Register]     │
│          │   • Analytics    │                  │
├──────────┴──────────────────┴──────────────────┤
│              💰 CHOOSE YOUR PLAN                │
├───────────┬──────────┬──────────┬──────────────┤
│   FREE    │ $9.99/mo │$149.99/yr│  $299/year   │
│  Token    │ Enhanced │   Full   │  Premium +   │
│  Based    │ Options  │  Suite   │ Mentorship   │
├───────────┴──────────┴──────────┴──────────────┤
│              FOOTER & SECURITY                  │
└─────────────────────────────────────────────────┘
```

## 💡 Business Model Notes

### Mentorship Revenue Share (Super-User Tier)
1. **Platform Fee:** IntelliCV-AI takes 20% of all mentorship transactions
2. **Mentor Earnings:** Mentors receive cut of $299 annual fee + can charge additional services
3. **Approval Process:** All mentor arrangements must run through platform
4. **Incentive Model:** Encourages high-level users to become mentors
5. **Value Proposition:** Real career guidance from industry professionals

### Data Collection Strategy (Free Tier)
- Priority: Get users to **upload CV** (valuable data asset)
- Give enough value to entice registration (limited chatbot, basic AI)
- Create clear upgrade path to paid tiers

## 🔧 Technical Implementation

### Files Modified
- ✅ `pages/00_Home.py` - Complete pricing and layout overhaul

### Session State Variables
- `selected_plan` - Tracks user's pricing tier choice
- `authenticated_user` - Login status
- `user_role` - User/admin role
- `is_new_user` - Registration flow tracking

### Button Redirects
- All pricing buttons → `pages/02_Payment.py`
- Registration button → `pages/02_Payment.py`
- Login success → `pages/03_Profile_Setup.py`

## ✨ Next Steps (Not Yet Implemented)

### 1. Payment Page (02_Payment.py)
- Needs to handle 4 pricing tiers
- Integration with admin_portal payment systems
- Stripe + Google Pay + other payment methods
- Pass selected_plan from session state

### 2. Profile Page (03_Profile_Setup.py)
- Standard elements: Full name, DOB, current role, salary expectations
- Email, address, location flexibility (country/postcode options)
- Current company, aspirations, job requirements
- **Chatbot integration** for career guidance
- Logo at 30% width (reduced from home page)
- Allow skip to Resume Upload

### 3. Resume Upload Page (05_Resume_Upload.py)
- Check if new user or existing user
- Prompt: "Any changes in your resume?"
- Upload latest version functionality
- Already has AI parsing and keyword extraction

### 4. Logo Consistency
- Ensure 30% logo width on all non-home pages
- Static logo in background of all pages

## 📊 Pricing Tier Comparison Matrix

| Feature | Free | Monthly $9.99 | Annual $149.99 | Super $299 |
|---------|------|---------------|----------------|------------|
| CV Upload | ✅ | ✅ | ✅ | ✅ |
| Profile Access | ✅ | ✅ | ✅ | ✅ |
| Basic AI | Limited | ✅ | ✅ | ✅ |
| Chatbot | Limited | ✅ | ✅ | ✅ |
| Career Intelligence | Truncated | Enhanced | Full | Full |
| Career Coach | ❌ | ❌ | ✅ | ✅ |
| Interview Coach | ❌ | ❌ | ✅ | ✅ |
| Multi-CV Auto | ❌ | ❌ | ✅ | ✅ |
| **1-on-1 Mentorship** | ❌ | ❌ | ❌ | ✅ |

## 🎯 Success Metrics to Track

1. **Conversion Rates** by tier
2. **Free → Paid upgrade rate** (esp. after CV upload)
3. **Mentor participation** in Super-User tier
4. **Mentorship session completion** and satisfaction
5. **Payment method usage** (Stripe vs Google Pay, etc.)

---

## 🚀 Status: HOME PAGE COMPLETE
All specified elements have been implemented. Ready for testing and integration with payment/profile pages.
