# IntelliCV Platform - API Quick Reference Card

## 🔴 CRITICAL (Must Have for Production)

| API | Purpose | Where to Get | Cost/Month |
|-----|---------|--------------|------------|
| **OpenAI GPT-4** | Core AI features | https://platform.openai.com | $200-500 |
| **Stripe** | Payments & subscriptions | https://dashboard.stripe.com | 2.9% + $0.30 per transaction |

## 🟠 HIGH PRIORITY (Important Features)

| API | Purpose | Where to Get | Cost/Month |
|-----|---------|--------------|------------|
| **Claude (Anthropic)** | AI redundancy | https://console.anthropic.com | $100-300 |
| **LinkedIn** | Profile import, jobs | https://developer.linkedin.com | Partnership |
| **AWS S3** | File storage | https://aws.amazon.com/s3 | $20-50 |
| **SendGrid** | Email notifications | https://sendgrid.com | $15-90 |

## 🟡 MEDIUM PRIORITY (Enhanced Features)

| API | Purpose | Where to Get | Cost/Month |
|-----|---------|--------------|------------|
| **Google AI** | Alternative AI | https://ai.google.dev | Free tier available |
| **Indeed** | Job listings | https://www.indeed.com/publisher | Partnership |
| **Glassdoor** | Company data | https://www.glassdoor.com/developer | Partnership |
| **Azure Blob** | Cloud storage backup | https://azure.microsoft.com | Variable |

## 🟢 OPTIONAL (Nice to Have)

| API | Purpose | Where to Get | Cost/Month |
|-----|---------|--------------|------------|
| **Perplexity** | Enhanced search | https://www.perplexity.ai | Variable |
| **Hugging Face** | ML models | https://huggingface.co | Free |
| **Exa AI** 🆕 | Semantic search | https://exa.ai | $0-200 |
| **SerpAPI** | Google scraping | https://serpapi.com | $0-100 |
| **Tavily** | AI search | https://tavily.com | $0-100 |
| **Twilio** | SMS/2FA | https://www.twilio.com | Variable |
| **Postman** | API testing | https://www.postman.com | $0-12 |

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Get CRITICAL Keys
1. Sign up for OpenAI: https://platform.openai.com → Get API key
2. Sign up for Stripe: https://dashboard.stripe.com → Get secret key

### Step 2: Configure in Admin Portal
1. Open: `http://localhost:8501`
2. Go to: Page 13 → API Integration
3. Click: "🔑 API Key Manager" tab
4. Paste keys → Save → Test

### Step 3: Set Environment Variables (Production)
```bash
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_live_...
```

---

## 📊 Minimum Costs

| Scenario | Monthly Cost |
|----------|--------------|
| **Development** | $50-100 (OpenAI only) |
| **MVP Launch** | $300-500 (OpenAI + Stripe + SendGrid) |
| **Full Production** | $400-1,200 (All features) |

---

## 🔄 Maintenance Schedule

- **Weekly:** Check usage stats (Page 13 dashboard)
- **Monthly:** Review costs and limits
- **Quarterly:** Rotate CRITICAL keys
- **Annually:** Security audit

---

## 🆘 Need Help?

- **Documentation:** `/SANDBOX/API_KEY_MANAGEMENT_GUIDE.md`
- **Admin UI:** Page 13: API Integration
- **Config Files:** `utils/config.py`, `sandbox_config.py`

---

## 🎯 Production Checklist

Before going live:
- [ ] OpenAI API key configured
- [ ] Stripe API key configured (live mode)
- [ ] SendGrid API key configured
- [ ] AWS S3 or Azure storage configured
- [ ] Environment variables set (not hardcoded)
- [ ] All CRITICAL APIs tested
- [ ] Rate limiting implemented
- [ ] Cost alerts configured
- [ ] Backup providers identified

---

**Last Updated:** October 28, 2025
