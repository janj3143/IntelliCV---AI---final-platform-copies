# 🚀 IntelliCV Platform - AI-Powered Career Intelligence System

**Version:** 3.0 (Production-Ready)  
**Status:** ✅ All Critical Features Complete  
**Last Updated:** October 28, 2025

---

## 📋 Overview

**IntelliCV** is a comprehensive AI-powered career intelligence platform that transforms how professionals manage their careers and how companies find talent. Built with cutting-edge AI technology, real-time analytics, and enterprise-grade security.

### **Key Features:**

- 🤖 **AI Content Generation** - Professional summaries, STAR bullets, cover letters, job descriptions
- 📄 **Intelligent Resume Parsing** - Extract structured data from 200+ resume formats
- 🧠 **70 Intelligence Types** - Comprehensive career analysis and insights
- 🔒 **Enterprise Security** - Email verification + Two-Factor Authentication (TOTP)
- 💳 **Dual Payment Processing** - Stripe + PayPal subscriptions
- 📊 **Real-time Analytics** - Live dashboard with actual data (35,735+ companies)
- 📑 **Professional PDF Export** - Branded, formatted documents
- 🎯 **Smart Job Matching** - AI-powered candidate-job matching

---

## 🏗 Architecture

### **Platform Components:**

```
IntelliCV/
├── Full system/               # Production platform
│   ├── admin_portal/         # Admin dashboard (14 pages)
│   │   ├── services/         # Backend services
│   │   └── pages/            # Streamlit UI pages
│   └── user_portal_final/    # User portal (10 pages)
│       ├── services/         # User services
│       └── pages/            # Streamlit UI pages
├── BACKEND-ADMIN-REORIENTATION/  # Backend processing
├── ai_data_final/            # Central data hub
│   └── dashboard_data.json   # Real-time metrics
└── Markdowns/                # Complete documentation
```

### **Technology Stack:**

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.29.0+, Plotly |
| **Backend** | Python 3.10+, JSON file-based storage |
| **AI/ML** | OpenAI GPT-4, Anthropic Claude, Google Gemini |
| **Security** | pyotp (TOTP 2FA), SMTP Email Verification |
| **Payments** | Stripe, PayPal |
| **APIs** | 17 external integrations |

---

## ✨ Features

### **🔐 Security (Production-Ready)**

#### **Email Verification** (600+ lines)
- UUID token generation with 48h expiry
- SMTP integration (Gmail/SendGrid/AWS SES)
- HTML + plain text templates
- URL-based verification flow
- Resend functionality

#### **Two-Factor Authentication** (700+ lines)
- TOTP algorithm (RFC 6238)
- QR code generation for authenticator apps
- Compatible with Google/Microsoft Authenticator, Authy
- 10 recovery codes per user (single-use)
- Enable/disable with verification

### **📊 Analytics (Production-Ready)**

#### **Real-time Analytics Service** (400+ lines)
- **NO MOCK DATA** - 100% real data integration
- Reads from ai_data_final folder:
  - 200+ parsed resumes
  - 35,735 enriched company records
  - 43 enriched candidate profiles
- Live metrics: users, growth, AI usage, data quality
- 60-second caching for performance

### **💰 Payment Processing (Production-Ready)**

#### **Stripe Integration**
- Credit/Debit card processing
- Subscription management
- Webhook handling

#### **PayPal Service** (600+ lines)
- Subscription creation and management
- Webhook signature verification
- Plan management (Pro/Expert Monthly/Annual)
- Refund processing
- Sandbox/Production modes

### **📑 PDF Export (Production-Ready)**

#### **PDF Export Service** (500+ lines)
- Professional formatting with branding
- Multiple content types:
  - Professional summaries
  - Bullet points (STAR format)
  - Cover letters
  - Job descriptions
- Formatting preservation (bold, italic, bullets)
- Batch export capability

### **🤖 AI Content Generation**

- Professional summaries
- STAR format achievement bullets
- Cover letters
- Job descriptions
- ATS optimization
- Content enhancement

### **🎯 Job Matching**

- AI-powered candidate scoring
- Skill matching algorithms
- Location-based filtering
- Salary range matching
- Company culture fit analysis

### **🧠 Intelligence Hub**

**70 Intelligence Types Including:**
- Career path analysis
- Skills gap analysis
- Job market trends
- Salary benchmarking
- Company culture insights
- Industry trends
- Networking opportunities
- Interview preparation

---

## 📊 Platform Stats

| Metric | Value |
|--------|-------|
| **Total Code** | 53,400+ lines |
| **Production Services** | 15+ services |
| **UI Pages** | 24 pages (14 admin + 10 user) |
| **API Integrations** | 17 external APIs |
| **Parsed Resumes** | 200+ |
| **Enriched Companies** | 35,735 |
| **Intelligence Types** | 70 |
| **Development Time** | 13 months |

---

## 🚀 Quick Start

### **Prerequisites:**

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### **Installation:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/janj3143/IntelliCV---AI---final-platform-copies.git
   cd IntelliCV---AI---final-platform-copies
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r Full\ system/user_portal_final/requirements.txt
   pip install -r Full\ system/user_portal_final/requirements-security.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy template and edit with your API keys
   cp Full\ system/user_portal_final/.env.email.template .env
   ```

   Required environment variables:
   ```env
   # AI Providers
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...
   
   # Email Service
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=noreply@intellicv.ai
   
   # Payment Providers
   STRIPE_SECRET_KEY=sk_test_...
   PAYPAL_CLIENT_ID=...
   PAYPAL_CLIENT_SECRET=...
   ```

5. **Run the application:**

   **User Portal:**
   ```bash
   cd Full\ system/user_portal_final
   streamlit run app.py --server.port 8501
   ```

   **Admin Portal:**
   ```bash
   cd Full\ system/admin_portal
   streamlit run main.py --server.port 8502
   ```

6. **Access the platform:**
   - User Portal: http://localhost:8501
   - Admin Portal: http://localhost:8502

---

## 💳 Pricing Tiers

| Plan | Price | Features |
|------|-------|----------|
| **Free** | £0 | Basic resume upload, limited AI credits |
| **Pro Monthly** | £59.99/mo | Full AI features, analytics, job matching |
| **Expert Monthly** | £99.99/mo | Priority support, advanced features |
| **Pro Annual** | £599.99/yr | Save 17%, all Pro features |
| **Expert Annual** | £999.99/yr | Save 17%, all Expert features |

---

## 🔌 API Integrations

**Integrated External APIs (17 total):**

1. **AI Providers:** OpenAI, Anthropic, Google Gemini
2. **Communication:** SendGrid, Twilio (optional)
3. **Payments:** Stripe, PayPal
4. **Job Boards:** LinkedIn, Indeed, Glassdoor
5. **Search:** Exa AI (deep web search)
6. **Services:** Google Maps, Calendly, Zoom, AWS S3
7. **Development:** GitHub, Slack

---

## 📚 Documentation

### **Master Guides:**

- **[MASTER_PROJECT_OVERVIEW.md](MASTER_PROJECT_OVERVIEW.md)** - Complete project documentation
- **[MASTER_TIMELINE.md](MASTER_TIMELINE.md)** - 13-month development timeline
- **[API_KEY_MANAGEMENT_GUIDE.md](API_KEY_MANAGEMENT_GUIDE.md)** - API setup guide
- **[PRIORITY_IMPLEMENTATION_COMPLETE.md](PRIORITY_IMPLEMENTATION_COMPLETE.md)** - All 5 priorities
- **[REAL_DATA_INTEGRATION_COMPLETE.md](REAL_DATA_INTEGRATION_COMPLETE.md)** - Real data architecture
- **[GITHUB_UPLOAD_CHECKLIST.md](GITHUB_UPLOAD_CHECKLIST.md)** - Deployment checklist

### **Organized Documentation:**

See `/Markdowns/` folder for categorized documentation:
- `/admin/` - Admin portal documentation
- `/backend/` - Backend service guides
- `/user/` - User portal documentation
- `/development/` - Development guides
- `/integration/` - Integration documentation

---

## 🛠 Development

### **Project Structure:**

```
Full system/
├── admin_portal/
│   ├── main.py                    # Admin entry point
│   ├── services/
│   │   ├── analytics_service.py   # Real-time analytics
│   │   └── pdf_export_service.py  # PDF generation
│   └── pages/                     # 14 admin pages
│
└── user_portal_final/
    ├── app.py                     # User entry point
    ├── services/
    │   ├── email_verification_service.py
    │   ├── two_factor_auth_service.py
    │   └── paypal_service.py
    └── pages/                     # 10 user pages
```

### **Key Services:**

| Service | Lines | Description |
|---------|-------|-------------|
| `email_verification_service.py` | 600+ | Email verification with SMTP |
| `two_factor_auth_service.py` | 700+ | TOTP 2FA with QR codes |
| `analytics_service.py` | 400+ | Real-time analytics (NO MOCK DATA) |
| `paypal_service.py` | 600+ | PayPal subscriptions & webhooks |
| `pdf_export_service.py` | 500+ | Professional PDF generation |

---

## 🧪 Testing

### **Security Testing:**

```bash
# Test email verification
cd Full\ system/user_portal_final
python -c "from services.email_verification_service import get_email_verification_service; print(get_email_verification_service().get_verification_stats())"

# Test 2FA
python -c "from services.two_factor_auth_service import get_2fa_service; service = get_2fa_service(); print(service.generate_secret('test@example.com'))"
```

### **Analytics Testing:**

```bash
# Test real data analytics
cd Full\ system/admin_portal
python -c "from services.analytics_service import get_analytics_service; service = get_analytics_service(); print(service.get_user_metrics())"
```

---

## 🤝 Contributing

This is a private production platform. For issues or questions, please contact the development team.

---

## 📄 License

Copyright © 2024-2025 IntelliCV Platform. All rights reserved.

---

## 🎯 Roadmap

### **Completed (v3.0):**
- ✅ Email verification system
- ✅ Two-factor authentication
- ✅ Real-time analytics with actual data
- ✅ PayPal payment integration
- ✅ PDF export functionality
- ✅ AI content generation
- ✅ Resume parsing
- ✅ Job matching
- ✅ 70 intelligence types

### **Planned (v3.1+):**
- [ ] Mobile app development
- [ ] Database migration (PostgreSQL)
- [ ] Advanced reporting
- [ ] Enterprise features
- [ ] API marketplace
- [ ] Multi-language support

---

## 📞 Support

**Documentation:** See `/Markdowns/` folder  
**Issues:** GitHub Issues (for collaborators)  
**Email:** support@intellicv.ai  

---

## 🎉 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [OpenAI](https://openai.com/) - AI content generation
- [Anthropic](https://anthropic.com/) - Alternative AI provider
- [Stripe](https://stripe.com/) - Payment processing
- [PayPal](https://paypal.com/) - Payment processing
- [ReportLab](https://reportlab.com/) - PDF generation

---

**Last Updated:** October 28, 2025  
**Version:** 3.0  
**Status:** ✅ Production-Ready

**⭐ Star this repository if you find it useful!**
