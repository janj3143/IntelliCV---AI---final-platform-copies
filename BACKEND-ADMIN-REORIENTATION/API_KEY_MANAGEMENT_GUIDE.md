# IntelliCV Platform - API Key Management Guide

**Date:** October 28, 2025  
**Location:** Admin Portal > Page 13: API Integration  
**Purpose:** Comprehensive guide for managing all platform API keys

---

## Overview

The IntelliCV platform integrates with 17+ external APIs across multiple categories. This guide provides a complete reference for all required API keys, their purposes, validity periods, and configuration instructions.

---

## API Categories

### 1. AI/LLM Services (Critical & High Priority)

#### OpenAI GPT-4 ⚠️ CRITICAL
- **Provider:** OpenAI
- **Purpose:** Resume analysis, chatbot responses, career intelligence generation
- **Rate Limit:** 10,000 requests/day (varies by plan)
- **Validity Period:** No expiration (billing-based)
- **Documentation:** https://platform.openai.com/docs/api-reference
- **Environment Variable:** `OPENAI_API_KEY`
- **Configuration File:** `utils/config.py` (line 70)
- **Priority:** CRITICAL - Core functionality depends on this

#### Claude API (Anthropic) ⚠️ HIGH
- **Provider:** Anthropic
- **Purpose:** Alternative AI processing, coaching hub interactions
- **Rate Limit:** 5,000 requests/day (varies by plan)
- **Validity Period:** No expiration (billing-based)
- **Documentation:** https://docs.anthropic.com/claude/reference
- **Environment Variable:** `ANTHROPIC_API_KEY`
- **Configuration File:** `utils/config.py` (line 71)
- **Priority:** HIGH - Important for redundancy and specialized tasks

#### Google AI (Gemini) 🟡 MEDIUM
- **Provider:** Google
- **Purpose:** Error fix suggestions, alternative AI processing
- **Rate Limit:** 1,500 requests/day (free tier)
- **Validity Period:** No expiration (billing-based)
- **Documentation:** https://ai.google.dev/docs
- **Environment Variable:** `GOOGLE_API_KEY`
- **Configuration File:** `utils/config.py` (line 72)
- **Priority:** MEDIUM - Used for specialized features

#### Perplexity AI 🟢 OPTIONAL
- **Provider:** Perplexity
- **Purpose:** Code fix suggestions, enhanced search capabilities
- **Rate Limit:** Varies by plan
- **Validity Period:** No expiration (billing-based)
- **Documentation:** https://docs.perplexity.ai
- **Priority:** OPTIONAL - Enhanced debugging features

#### Hugging Face 🟢 OPTIONAL
- **Provider:** Hugging Face
- **Purpose:** Transformer models, semantic analysis
- **Rate Limit:** Unlimited (for self-hosted models)
- **Validity Period:** No expiration
- **Documentation:** https://huggingface.co/docs/api-inference
- **Priority:** OPTIONAL - Advanced AI features

---

### 2. Job Boards & Professional Networks (High & Medium Priority)

#### LinkedIn API ⚠️ HIGH
- **Provider:** LinkedIn (Microsoft)
- **Purpose:** Profile import, job search integration, industry data classification
- **Rate Limit:** Varies by endpoint and agreement
- **Validity Period:** 90 days (renewable via OAuth)
- **Documentation:** https://docs.microsoft.com/linkedin
- **Configuration File:** `sandbox_config.py` (line 1192)
- **Features Used:**
  - Profile import for resume auto-population
  - Industry classification (422-line integration)
  - Job posting integration
- **Priority:** HIGH - Major user-facing feature

#### Indeed API 🟡 MEDIUM
- **Provider:** Indeed
- **Purpose:** Job listings aggregation, market intelligence data
- **Rate Limit:** Varies by partnership agreement
- **Validity Period:** Annual renewal
- **Documentation:** https://www.indeed.com/publisher
- **Configuration File:** `sandbox_config.py` (line 1193)
- **Priority:** MEDIUM - Job search enhancement

#### Glassdoor API 🟡 MEDIUM
- **Provider:** Glassdoor
- **Purpose:** Company reviews, salary data, employer insights
- **Rate Limit:** Varies by partnership agreement
- **Validity Period:** Annual renewal
- **Documentation:** https://www.glassdoor.com/developer
- **Configuration File:** `sandbox_config.py` (line 1194)
- **Priority:** MEDIUM - Career intelligence features

---

### 3. Payment & Subscription Services (Critical)

#### Stripe API ⚠️ CRITICAL
- **Provider:** Stripe
- **Purpose:** Subscription management, payment processing, plan upgrades
- **Rate Limit:** Unlimited (with built-in rate limiting)
- **Validity Period:** Secret keys rotatable anytime
- **Documentation:** https://stripe.com/docs/api
- **Configuration File:** `user_portal_admin_integration.py` (line 550)
- **Security Note:** 
  - Use publishable key for client-side
  - Use secret key for server-side (NEVER expose)
  - Rotate keys every 90 days minimum
- **Priority:** CRITICAL - Revenue and access control

---

### 4. Cloud Storage & Infrastructure (High Priority)

#### AWS S3 ⚠️ HIGH
- **Provider:** Amazon Web Services
- **Purpose:** Resume file storage, document backups, data archival
- **Rate Limit:** Unlimited (billing-based)
- **Validity Period:** Access keys should be rotated every 90 days
- **Documentation:** https://docs.aws.amazon.com/s3
- **Requirements File:** `requirements_sandbox.txt` (line 250) - boto3>=1.29.0
- **Security Best Practices:**
  - Use IAM roles when possible
  - Implement bucket policies
  - Enable versioning for critical data
  - Use server-side encryption
- **Priority:** HIGH - Data persistence

#### Azure Blob Storage 🟢 OPTIONAL
- **Provider:** Microsoft Azure
- **Purpose:** Alternative cloud storage option
- **Rate Limit:** Unlimited (billing-based)
- **Validity Period:** Rotate access keys regularly
- **Documentation:** https://docs.microsoft.com/azure/storage
- **Requirements File:** `requirements_sandbox.txt` (line 151)
- **Priority:** OPTIONAL - Redundancy option

---

### 5. Communication Services (High Priority)

#### SendGrid Email API ⚠️ HIGH
- **Provider:** SendGrid (Twilio)
- **Purpose:** Transactional emails, user notifications, system alerts
- **Rate Limit:** 
  - Free tier: 100 emails/day
  - Paid plans: Unlimited
- **Validity Period:** API keys are rotatable, no expiration
- **Documentation:** https://docs.sendgrid.com
- **Requirements File:** `requirements_sandbox.txt` (line 98)
- **Common Use Cases:**
  - Welcome emails
  - Password resets
  - Resume analysis notifications
  - Subscription confirmations
- **Priority:** HIGH - User communication

#### Twilio SMS API 🟢 OPTIONAL
- **Provider:** Twilio
- **Purpose:** SMS notifications, two-factor authentication (2FA)
- **Rate Limit:** Varies by plan
- **Validity Period:** No expiration
- **Documentation:** https://www.twilio.com/docs
- **Mentioned In:** `USER_EXPERIENCE_REDESIGN_SUMMARY.md` (line 388)
- **Priority:** OPTIONAL - Enhanced security features

---

### 6. Search & Data APIs (Optional)

#### Exa AI 🟢 NEW - OPTIONAL
- **Provider:** Exa
- **Purpose:** Enhanced semantic search, web data enrichment
- **Rate Limit:** 1,000 searches/month (free tier)
- **Validity Period:** No expiration (billing-based)
- **Documentation:** https://docs.exa.ai
- **Status:** NEW addition to platform
- **Use Cases:**
  - Enhanced job search
  - Company research
  - Industry trend analysis
- **Priority:** OPTIONAL - Advanced features

#### SerpAPI 🟢 OPTIONAL
- **Provider:** SerpAPI
- **Purpose:** Google search results scraping, job listing aggregation
- **Rate Limit:** 
  - Free: 100 searches/month
  - Paid plans: Higher limits
- **Validity Period:** No expiration
- **Documentation:** https://serpapi.com/docs
- **Priority:** OPTIONAL - Search enhancement

#### Tavily Search API 🟢 OPTIONAL
- **Provider:** Tavily
- **Purpose:** AI-optimized search results
- **Rate Limit:** 1,000 searches/month (free tier)
- **Validity Period:** No expiration (billing-based)
- **Documentation:** https://docs.tavily.com
- **Priority:** OPTIONAL - AI-enhanced search

---

### 7. Development & Testing (Optional)

#### Postman API 🟢 OPTIONAL
- **Provider:** Postman
- **Purpose:** API testing, collection management, automated testing
- **Rate Limit:** Varies by plan (personal/team)
- **Validity Period:** User-based, no expiration
- **Documentation:** https://learning.postman.com/docs/api
- **Priority:** OPTIONAL - Development workflow

---

## Configuration Instructions

### Step 1: Access Admin Portal
1. Navigate to Admin Portal: `http://localhost:8501` (or your deployment URL)
2. Login with admin credentials
3. Go to **Page 13: API Integration**

### Step 2: Configure API Keys

#### Method A: Via Admin Portal UI (Recommended for Testing)
1. Click on **"🔑 API Key Manager"** tab
2. Expand the API service you want to configure
3. Paste your API key in the password field
4. Click **"💾 Save"** button
5. Click **"🧪 Test"** to verify connection
6. Restart application for changes to take effect

#### Method B: Via Environment Variables (Recommended for Production)
```bash
# Create .env file in project root
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-api-key
STRIPE_SECRET_KEY=sk_live_your-stripe-secret-key
SENDGRID_API_KEY=SG.your-sendgrid-key
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# Add other keys as needed
```

#### Method C: Via Configuration Files
Edit the relevant configuration file:
- **User Portal:** `IntelliCV/SANDBOX/Full system/user_portal_final/utils/config.py`
- **Admin Portal:** `IntelliCV/SANDBOX/Full system/admin_portal/utilities/settings.py`

### Step 3: Verify Configuration
1. Return to API Integration page
2. Check status indicators:
   - ✅ Green = Active and working
   - 🟡 Yellow = Configured but not tested
   - ⚠️ Red = Not configured or error
3. Review usage statistics
4. Test critical APIs first (OpenAI, Stripe)

---

## Security Best Practices

### API Key Storage
- ✅ **DO:** Store in environment variables
- ✅ **DO:** Use secret management services (AWS Secrets Manager, Azure Key Vault)
- ✅ **DO:** Rotate keys every 90 days minimum
- ✅ **DO:** Use separate keys for dev/staging/production
- ❌ **DON'T:** Commit keys to version control
- ❌ **DON'T:** Share keys via email or Slack
- ❌ **DON'T:** Hardcode keys in source files

### Key Rotation Schedule
- **Critical APIs (OpenAI, Stripe, AWS):** Every 90 days
- **High Priority APIs (LinkedIn, SendGrid):** Every 180 days
- **Optional APIs:** Annually or as needed
- **After Security Incident:** IMMEDIATELY

### Access Control
- Limit API key access to essential team members
- Use role-based access control (RBAC)
- Implement audit logging for all key usage
- Monitor for unusual activity patterns

### Rate Limiting
- Implement application-level rate limiting
- Monitor usage to stay within provider limits
- Set up alerts for approaching limits
- Have backup providers for critical services

---

## Troubleshooting

### Common Issues

#### "API Key Invalid" Error
1. Verify key is correctly copied (no extra spaces)
2. Check if key has expired or been revoked
3. Verify key has required permissions/scopes
4. Confirm you're using correct environment (test vs. production)

#### "Rate Limit Exceeded" Error
1. Check current usage in API Integration dashboard
2. Review rate limit for your plan tier
3. Consider upgrading to higher tier
4. Implement request queuing/throttling

#### "Connection Timeout" Error
1. Verify internet connectivity
2. Check if API provider has outage (status page)
3. Review firewall/proxy settings
4. Increase timeout settings in configuration

### Getting Help
- **Documentation:** Check provider's official docs first
- **Community:** Stack Overflow, provider forums
- **Support:** Contact provider's support team
- **Internal:** Check `Error fixes word docs/` folder

---

## Monitoring & Maintenance

### Regular Tasks

#### Weekly
- [ ] Review API usage statistics
- [ ] Check for approaching rate limits
- [ ] Monitor error rates
- [ ] Verify all critical APIs are functional

#### Monthly
- [ ] Analyze cost trends
- [ ] Review unused API keys
- [ ] Update documentation
- [ ] Test backup/failover systems

#### Quarterly
- [ ] Rotate critical API keys
- [ ] Review and update rate limits
- [ ] Audit access permissions
- [ ] Update API integration dependencies

#### Annually
- [ ] Comprehensive security audit
- [ ] Renegotiate API contracts
- [ ] Evaluate alternative providers
- [ ] Update disaster recovery plans

---

## Cost Management

### Current Costs (Estimated Monthly)

| Service | Free Tier | Paid Tier | Current Usage | Priority |
|---------|-----------|-----------|---------------|----------|
| OpenAI GPT-4 | $0 (limited) | ~$200-500 | Variable | CRITICAL |
| Anthropic Claude | $0 (limited) | ~$100-300 | Variable | HIGH |
| Google Gemini | $0 (1500/day) | Pay-per-use | Low | MEDIUM |
| LinkedIn API | Partnership | Partnership | Medium | HIGH |
| Stripe | $0 | 2.9% + $0.30 | Per transaction | CRITICAL |
| SendGrid | $0 (100/day) | $15-$90 | Medium | HIGH |
| AWS S3 | $0 (5GB) | ~$20-50 | Variable | HIGH |
| Exa AI | $0 (1000/mo) | ~$50-200 | Not yet used | OPTIONAL |

**Total Estimated Monthly Cost:** $400-$1,200 (varies by usage)

### Cost Optimization Tips
1. Use free tiers during development
2. Implement caching to reduce API calls
3. Batch requests when possible
4. Monitor and alert on unusual usage spikes
5. Regularly review and remove unused integrations

---

## Compliance & Legal

### Data Privacy
- Ensure API providers are GDPR/CCPA compliant
- Review data retention policies
- Understand data residency requirements
- Implement data anonymization where needed

### Terms of Service
- Review and comply with each provider's TOS
- Understand usage restrictions
- Monitor for TOS changes
- Maintain compliance documentation

---

## Future Additions

### Planned Integrations
- [ ] ZipRecruiter API (Job Boards)
- [ ] Monster API (Job Boards)
- [ ] Slack API (Notifications)
- [ ] GitHub API (Developer profiles)
- [ ] Calendly API (Interview scheduling)

### Under Evaluation
- [ ] Anthropic's Extended Models
- [ ] Azure OpenAI Service
- [ ] CareerBuilder API
- [ ] Zoom API

---

## Quick Reference

### Critical Path (Minimum for Production)
1. ✅ OpenAI API (Resume analysis, AI features)
2. ✅ Stripe API (Payments, subscriptions)
3. ✅ SendGrid API (Email notifications)
4. ✅ AWS S3 or Azure Blob (File storage)

### Full Feature Set
All 17 APIs configured and tested

### Development/Testing
OpenAI + Stripe (test mode) + Local storage

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | Oct 28, 2025 | Initial comprehensive guide | IntelliCV Team |

---

## Additional Resources

- **Admin Portal:** Page 13 - API Integration
- **Configuration Files:** `utils/config.py`, `sandbox_config.py`
- **Requirements:** `requirements_sandbox.txt`
- **Documentation Folder:** `Error fixes word docs/`
- **Markdown Guides:** `Markdowns/` directory

---

**Last Updated:** October 28, 2025  
**Next Review:** January 28, 2026 (Quarterly)
