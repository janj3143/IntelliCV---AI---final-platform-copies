"""
🎯 UMarketU Suite - Complete Career Marketing Platform
======================================================
Unified suite for discovering roles, analyzing fit, tailoring resumes, planning interviews,
and tracking applications with partner-aware life logistics.

Based on Product/Tech Spec [2025-10-25-01]
Consolidates pages: 12, 20, 21, 24, 25, 27
Backend services: Resume Upload (09), Career Intelligence (11)
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import tempfile
import sys

# Setup paths
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Import portal bridge for cross-portal communication
try:
    from shared_backend.services.portal_bridge import IntelligenceService
    intelligence_service = IntelligenceService()
    PORTAL_BRIDGE_AVAILABLE = True
except ImportError as e:
    PORTAL_BRIDGE_AVAILABLE = False
    intelligence_service = None

# Page configuration
st.set_page_config(
    page_title="🎯 UMarketU Suite | IntelliCV-AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to access UMarketU Suite")
    if st.button("🏠 Return to Home"):
        st.switch_page("main.py")
    st.stop()

# Tier check for premium features
user_tier = st.session_state.get('subscription_tier', 'free')
PREMIUM_TIERS = ['monthly_pro', 'annual_pro', 'enterprise_pro']

# Initialize session state for UMarketU workflow
if 'umarketu_state' not in st.session_state:
    st.session_state.umarketu_state = {
        'current_step': 'discovery',  # discovery, fit, tune, track, coach, partner
        'search_results': [],
        'selected_job': None,
        'jd_data': None,
        'fit_analysis': None,
        'peer_overlay': None,
        'tuned_resume': None,
        'applications': [],
        'interview_prep': None,
        'partner_profile': None
    }

# =============================================================================
# HELPER FUNCTIONS - EXA COMPANY INSIGHTS
# =============================================================================

def get_company_insights(company_name: str, domain: str = None) -> dict:
    """
    Get Exa-enriched company insights for job postings.
    
    Args:
        company_name: Company name from job posting
        domain: Company domain (optional, will be extracted if not provided)
    
    Returns:
        Dictionary with company insights or empty dict if not available
    """
    if not EXA_AVAILABLE:
        return {}
    
    # Extract domain from company name if not provided
    if not domain:
        # Simple heuristic: lowercase company name + .com
        domain = company_name.lower().replace(' ', '').replace(',', '').replace('.', '') + '.com'
    
    try:
        # Get enrichment summary from database
        summary = get_enrichment_summary(domain)
        
        if not summary:
            return {}
        
        # Get careers pages
        careers_pages = get_company_sources(domain, content_type='careers', limit=3)
        
        # Get product pages
        product_pages = get_company_sources(domain, content_type='products', limit=3)
        
        return {
            'domain': domain,
            'has_data': True,
            'total_pages': summary.get('total_pages_found', 0),
            'careers_pages': careers_pages,
            'product_pages': product_pages,
            'last_updated': summary.get('completed_at'),
            'enriched': True
        }
    
    except Exception as e:
        # Silently fail - don't break job cards if Exa data unavailable
        return {}

def render_company_insights_card(insights: dict):
    """
    Render a company insights card with Exa data.
    
    Args:
        insights: Company insights dictionary from get_company_insights()
    """
    if not insights or not insights.get('has_data'):
        return
    
    with st.expander("🌐 Company Intel (Exa)", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Careers Pages**")
            careers = insights.get('careers_pages', [])
            if careers:
                for page in careers[:2]:  # Show top 2
                    st.markdown(f"- [{page.get('title', 'View Page')}]({page.get('url')})")
            else:
                st.info("No careers pages found yet")
        
        with col2:
            st.markdown("**🚀 Products**")
            products = insights.get('product_pages', [])
            if products:
                for page in products[:2]:  # Show top 2
                    st.markdown(f"- [{page.get('title', 'View Page')}]({page.get('url')})")
            else:
                st.info("No product pages found yet")
        
        st.caption(f"💡 Enriched from {insights.get('total_pages', 0)} pages • Last updated: {insights.get('last_updated', 'N/A')}")

# Title and introduction
st.title("🎯 UMarketU Suite")
st.markdown("""
### Your Complete Career Marketing Platform
**Vision**: Market yourself end-to-end from job discovery to offer acceptance.

**Workflow**: Search → Analyze Fit → Tailor Resume → Apply & Track → Interview Prep → Partner Optimization
""")

# Token cost display
st.info("💎 **Token Costs**: Discovery (5 tokens) | Fit Analysis (8 tokens) | Resume Tuning (12 tokens) | Interview Coach (15 tokens) | Partner Mode (20 tokens)")

# KPI metrics at top
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🎯 Match Rate", "78%", "12%", help="Quality of job matches found")
with col2:
    st.metric("📧 Interview Rate", "24%", "8%", help="Applications resulting in interviews")
with col3:
    st.metric("🏆 Offer Rate", "15%", "5%", help="Interviews resulting in offers")
with col4:
    st.metric("⏱️ Time to Apply", "18m", "-12m", help="Average time from search to application")
with col5:
    st.metric("⭐ Quality Score", "8.2/10", "0.8", help="Application quality rating")

st.markdown("---")

# Navigation tabs for suite sections
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Job Discovery", 
    "📊 Fit Analysis", 
    "📝 Resume Tuning", 
    "📋 Application Tracker", 
    "🎤 Interview Coach",
    "👥 Partner Mode"
])

# ===========================
# TAB 1: JOB DISCOVERY
# ===========================
with tab1:
    st.header("🔍 Job Discovery & Search")
    st.markdown("**US1**: Search across Google/LinkedIn/company career pages with your skills & location radius")
    
    # Search filters
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_skills = st.multiselect(
            "🎯 Your Core Skills",
            ["Python", "Machine Learning", "Data Science", "SQL", "Cloud Computing", 
             "Project Management", "Agile", "Leadership", "Communication"],
            default=["Python", "Machine Learning"],
            help="Select or type your key skills"
        )
        
        job_titles = st.text_input(
            "💼 Target Job Titles",
            value="Machine Learning Engineer, Data Scientist",
            help="Comma-separated list of job titles"
        )
    
    with col2:
        location = st.text_input("📍 Location", value="London, UK")
        radius_km = st.slider("📏 Search Radius (km)", 0, 100, 25, 5)
        
        remote_ok = st.checkbox("🏠 Include Remote Jobs", value=True)
        
        salary_min = st.number_input("💰 Min Salary (£)", 0, 200000, 50000, 5000)
    
    # Advanced filters (collapsible)
    with st.expander("🔧 Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            experience_level = st.select_slider(
                "📊 Experience Level",
                options=["Entry", "Mid", "Senior", "Lead", "Executive"],
                value="Mid"
            )
            company_size = st.multiselect(
                "🏢 Company Size",
                ["Startup (<50)", "Small (50-200)", "Medium (200-1000)", "Large (1000+)"],
                default=["Medium (200-1000)", "Large (1000+)"]
            )
        with col2:
            job_type = st.multiselect(
                "📄 Job Type",
                ["Full-time", "Part-time", "Contract", "Freelance"],
                default=["Full-time"]
            )
            posted_within = st.selectbox(
                "📅 Posted Within",
                ["24 hours", "7 days", "30 days", "Any time"],
                index=1
            )
    
    # Search button
    if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
        with st.spinner("🔄 Searching across multiple platforms..."):
            # Get market intelligence from admin backend via portal_bridge
            if PORTAL_BRIDGE_AVAILABLE and intelligence_service and user_tier in PREMIUM_TIERS:
                try:
                    # Extract primary industry from skills
                    primary_skill = search_skills[0] if search_skills else "Technology"
                    
                    # Get real market intelligence
                    market_intel = intelligence_service.get_market_intel(
                        industry=primary_skill,
                        role=job_titles.split(',')[0].strip() if job_titles else None,
                        location=location
                    )
                    
                    # Use market intelligence to enhance search results
                    st.session_state.umarketu_state['market_intelligence'] = market_intel
                    st.success(f"✅ Retrieved market intelligence: {market_intel.get('demand_level', 'N/A')} demand")
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not fetch market intelligence: {str(e)}")
                    market_intel = None
            else:
                market_intel = None
            
            # Simulate search (would call backend API: POST /search/jobs)
            # In production, this would integrate with job boards APIs
            search_results = [
                {
                    'id': 'job_001',
                    'title': 'Senior Machine Learning Engineer',
                    'company': 'TechCorp AI',
                    'location': 'London, UK',
                    'salary': '£70,000 - £95,000',
                    'source': 'LinkedIn',
                    'posted': '2 days ago',
                    'remote': 'Hybrid',
                    'url': 'https://example.com/job1',
                    'quick_fit': 85
                },
                {
                    'id': 'job_002',
                    'title': 'Data Science Lead',
                    'company': 'FinTech Innovations',
                    'location': 'London, UK',
                    'salary': '£80,000 - £110,000',
                    'source': 'Company Site',
                    'posted': '5 days ago',
                    'remote': 'Remote',
                    'url': 'https://example.com/job2',
                    'quick_fit': 78
                },
                {
                    'id': 'job_003',
                    'title': 'ML Engineer - NLP',
                    'company': 'DeepLearn Labs',
                    'location': 'Cambridge, UK',
                    'salary': '£65,000 - £85,000',
                    'source': 'Google Jobs',
                    'posted': '1 week ago',
                    'remote': 'On-site',
                    'url': 'https://example.com/job3',
                    'quick_fit': 92
                }
            ]
            
            # Enhance with market intelligence if available
            if market_intel:
                for job in search_results:
                    job['market_demand'] = market_intel.get('demand_level', 'Unknown')
                    job['salary_benchmark'] = market_intel.get('salary_range', 'N/A')
            
            st.session_state.umarketu_state['search_results'] = search_results
            st.success(f"✅ Found {len(search_results)} matching jobs!")
            
            if not PORTAL_BRIDGE_AVAILABLE and user_tier in PREMIUM_TIERS:
                st.info("ℹ️ Portal bridge unavailable - using cached job data")
    
    # Display search results
    if st.session_state.umarketu_state['search_results']:
        st.markdown("### 📋 Search Results")
        
        # Sort options
        sort_by = st.selectbox("Sort by", ["Quick Fit Score ⬇️", "Salary ⬇️", "Posted Date ⬇️"], index=0)
        
        for job in st.session_state.umarketu_state['search_results']:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {job['title']}")
                    st.markdown(f"**{job['company']}** | 📍 {job['location']} | {job['remote']}")
                    st.markdown(f"💰 {job['salary']} | 📅 Posted {job['posted']} | Source: {job['source']}")
                
                with col2:
                    # Quick fit indicator
                    fit_color = "green" if job['quick_fit'] >= 80 else "orange" if job['quick_fit'] >= 60 else "red"
                    st.markdown(f"### :{fit_color}[{job['quick_fit']}%]")
                    st.caption("Quick Fit")
                
                with col3:
                    if st.button("📊 Analyze Fit", key=f"analyze_{job['id']}", use_container_width=True):
                        st.session_state.umarketu_state['selected_job'] = job
                        st.session_state.umarketu_state['current_step'] = 'fit'
                        st.rerun()
                    
                    if st.button("🔗 View Job", key=f"view_{job['id']}", use_container_width=True):
                        st.markdown(f"[Open in new tab]({job['url']})")
                
                # EXA COMPANY INSIGHTS - NEW!
                if EXA_AVAILABLE:
                    insights = get_company_insights(job['company'], job.get('domain'))
                    if insights.get('has_data'):
                        render_company_insights_card(insights)
                
                st.markdown("---")

# ===========================
# TAB 2: FIT ANALYSIS
# ===========================
with tab2:
    st.header("📊 Fit Analysis - Touch Points & Block Points")
    st.markdown("**US3**: Calculate Touch-Points (positives) and Block-Points (gaps), output % fit, suggest actions")
    
    selected_job = st.session_state.umarketu_state.get('selected_job')
    
    if not selected_job:
        st.info("👈 Select a job from the Discovery tab to analyze fit")
    else:
        st.success(f"**Analyzing**: {selected_job['title']} at {selected_job['company']}")
        
        # JD ingestion (US2)
        with st.expander("📄 Job Description Details", expanded=False):
            st.markdown("**Auto-captured from job posting**")
            
            # Simulated JD text
            jd_text = f"""
            **{selected_job['title']}** at {selected_job['company']}
            
            We're looking for an experienced ML Engineer to join our AI team...
            
            **Requirements:**
            - 5+ years Python development
            - Deep learning frameworks (TensorFlow, PyTorch)
            - Cloud platforms (AWS, GCP)
            - Strong communication skills
            - Experience with NLP a plus
            
            **Nice to have:**
            - PhD in relevant field
            - Published research
            - Team leadership experience
            """
            st.text_area("JD Text", jd_text, height=200)
        
        # Fit analysis engine
        if st.button("🔍 Calculate Fit Score", type="primary"):
            with st.spinner("🧠 Analyzing with AI..."):
                # Simulate AI analysis (would call: POST /match/fit {resume_id, jd_id})
                st.session_state.umarketu_state['fit_analysis'] = {
                    'fit_score': 78,
                    'touch_points': [
                        {'skill': 'Python', 'weight': 10, 'evidence': '8 years experience', 'recency_boost': 1.3, 'score': 13.0},
                        {'skill': 'Machine Learning', 'weight': 10, 'evidence': 'Led 5 ML projects', 'recency_boost': 1.3, 'score': 13.0},
                        {'skill': 'TensorFlow', 'weight': 8, 'evidence': 'Used in last 3 projects', 'recency_boost': 1.3, 'score': 10.4},
                        {'skill': 'SQL', 'weight': 6, 'evidence': 'Daily use for 5 years', 'recency_boost': 1.3, 'score': 7.8},
                        {'skill': 'Communication', 'weight': 7, 'evidence': 'Presented at 3 conferences', 'recency_boost': 1.1, 'score': 7.7},
                    ],
                    'block_points': [
                        {'requirement': 'Cloud Computing (AWS/GCP)', 'criticality': 8, 'mitigation': 'Complete AWS ML Specialty course (2-week crash course)'},
                        {'requirement': 'NLP Experience', 'criticality': 5, 'mitigation': 'Highlight transferable skills from text analysis project'},
                        {'requirement': 'PhD', 'criticality': 3, 'mitigation': 'Emphasize practical experience and impact'},
                    ]
                }
                st.success("✅ Analysis complete!")
        
        # Display fit analysis
        if st.session_state.umarketu_state.get('fit_analysis'):
            analysis = st.session_state.umarketu_state['fit_analysis']
            
            # Overall score
            st.markdown("### 🎯 Overall Fit Score")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                fit_score = analysis['fit_score']
                color = "green" if fit_score >= 75 else "orange" if fit_score >= 60 else "red"
                st.markdown(f"# :{color}[{fit_score}%]")
                st.caption("Match Score")
            with col2:
                st.metric("Touch Points", len(analysis['touch_points']), help="Strengths matching requirements")
            with col3:
                st.metric("Block Points", len(analysis['block_points']), help="Gaps to address")
            with col4:
                likelihood = "Strong Bet" if fit_score >= 75 else "Competitive" if fit_score >= 60 else "Stretch"
                st.markdown(f"### {likelihood}")
                st.caption("Likelihood Band")
            
            # Touch Points (strengths)
            st.markdown("### ✅ Touch Points - Your Strengths")
            tp_data = []
            for tp in analysis['touch_points']:
                tp_data.append({
                    'Skill': tp['skill'],
                    'Weight': tp['weight'],
                    'Evidence': tp['evidence'],
                    'Recency Boost': f"{tp['recency_boost']}x",
                    'Score': f"{tp['score']:.1f}"
                })
            st.dataframe(pd.DataFrame(tp_data), use_container_width=True)
            
            # Block Points (gaps)
            st.markdown("### ⚠️ Block Points - Gaps to Address")
            for bp in analysis['block_points']:
                severity = "🔴" if bp['criticality'] >= 7 else "🟡" if bp['criticality'] >= 4 else "🟢"
                st.markdown(f"{severity} **{bp['requirement']}** (Criticality: {bp['criticality']}/10)")
                st.info(f"💡 **Mitigation**: {bp['mitigation']}")
            
            # Quadrant visualization
            st.markdown("### 📈 Value vs Readiness Quadrant")
            
            fig = go.Figure()
            
            # Add quadrant background
            fig.add_shape(type="rect", x0=0, y0=0, x1=50, y1=50, fillcolor="lightcoral", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=50, y0=0, x1=100, y1=50, fillcolor="lightyellow", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=0, y0=50, x1=50, y1=100, fillcolor="lightyellow", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=50, y0=50, x1=100, y1=100, fillcolor="lightgreen", opacity=0.2, line_width=0)
            
            # Add current position
            readiness = 75  # Based on touch points
            value = 82      # Based on potential impact
            fig.add_trace(go.Scatter(
                x=[readiness],
                y=[value],
                mode='markers+text',
                marker=dict(size=20, color='blue'),
                text=['YOU'],
                textposition='top center',
                name='Your Position'
            ))
            
            fig.update_layout(
                title="Your Position in Value-Readiness Space",
                xaxis_title="Readiness (Skills & Recency) →",
                yaxis_title="Value to Employer →",
                xaxis=dict(range=[0, 100]),
                yaxis=dict(range=[0, 100]),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # US4: Peer Overlay
            st.markdown("### 👥 Peer Comparison Overlay")
            if st.button("📊 Show Peer Benchmarking"):
                with st.spinner("🔄 Simulating peer cohort..."):
                    # Would call: POST /peer/overlay {resume_id, jd_id, assumptions{}}
                    st.session_state.umarketu_state['peer_overlay'] = {
                        'percentile': 72,
                        'rank': 'Top 28%',
                        'cohort_size': 150,
                        'avg_fit': 65,
                        'top_10_fit': 88
                    }
            
            if st.session_state.umarketu_state.get('peer_overlay'):
                overlay = st.session_state.umarketu_state['peer_overlay']
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Your Rank", overlay['rank'])
                with col2:
                    st.metric("Percentile", f"{overlay['percentile']}th")
                with col3:
                    st.metric("Cohort Average", f"{overlay['avg_fit']}%")
                with col4:
                    st.metric("Top 10% Threshold", f"{overlay['top_10_fit']}%")
                
                st.success(f"✅ You rank in the **{overlay['rank']}** among {overlay['cohort_size']} similar candidates")

# ===========================
# TAB 3: RESUME TUNING
# ===========================
with tab3:
    st.header("📝 Resume Auto-Tuning")
    st.markdown("**US5**: Generate role-specific resume variant, highlighting strengths and closing gaps with evidence")
    
    if not st.session_state.umarketu_state.get('selected_job'):
        st.info("👈 Select a job and analyze fit first")
    elif not st.session_state.umarketu_state.get('fit_analysis'):
        st.info("👆 Run fit analysis first to get tuning recommendations")
    else:
        job = st.session_state.umarketu_state['selected_job']
        fit = st.session_state.umarketu_state['fit_analysis']
        
        st.success(f"**Tuning resume for**: {job['title']} at {job['company']}")
        
        # Tuning options
        col1, col2 = st.columns(2)
        with col1:
            headline_style = st.selectbox(
                "📰 Headline Style",
                ["Achievement-focused", "Skill-focused", "Impact-focused", "Hybrid"],
                index=0
            )
            
            bullet_format = st.selectbox(
                "📋 Bullet Format",
                ["STAR (Situation-Task-Action-Result)", "CAR (Context-Action-Result)", "PAR (Problem-Action-Result)"],
                index=0
            )
        
        with col2:
            skills_placement = st.selectbox(
                "🎯 Skills Section",
                ["Top (before experience)", "Bottom (after experience)", "Integrated in bullets"],
                index=0
            )
            
            gap_strategy = st.multiselect(
                "🔧 Gap Mitigation Strategy",
                ["Include micro-courses", "Add portfolio links", "Highlight transferable skills", "Add case notes"],
                default=["Highlight transferable skills"]
            )
        
        # Generate tuned resume
        if st.button("✨ Generate Tailored Resume", type="primary"):
            with st.spinner("🎨 Auto-tuning your resume..."):
                # Would call: POST /resume/tune {resume_id, jd_id, options{}}
                st.session_state.umarketu_state['tuned_resume'] = {
                    'version_id': 'v2025_001',
                    'headline': f"Senior ML Engineer | 8 Years Python & Deep Learning | Delivered 5 Production ML Systems",
                    'summary': "Results-driven ML Engineer with proven track record...",
                    'changes': 15,
                    'created_at': datetime.now().isoformat()
                }
                st.success("✅ Resume variant generated!")
        
        # Display tuned resume
        if st.session_state.umarketu_state.get('tuned_resume'):
            tuned = st.session_state.umarketu_state['tuned_resume']
            
            st.markdown("### 📄 Tailored Resume Preview")
            
            # Show changes summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Changes Made", tuned['changes'])
            with col2:
                st.metric("Version ID", tuned['version_id'])
            with col3:
                st.metric("ATS Score", "94%", "12%")
            
            # Diff viewer (simplified)
            with st.expander("🔍 View Changes", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ❌ Original")
                    st.code("""
Headline: Machine Learning Engineer

Summary: Experienced engineer with ML skills...

Experience:
- Worked with machine learning models
- Developed data pipelines
""")
                
                with col2:
                    st.markdown("#### ✅ Tailored")
                    st.code(f"""
Headline: {tuned['headline']}

Summary: {tuned['summary']}

Experience:
- Architected and deployed 5 production ML systems processing 1M+ daily transactions
- Built data pipelines reducing processing time by 40% using Apache Spark
- Led cloud migration (AWS) for ML infrastructure, cutting costs by $50k/year
""")
            
            # Export options
            st.markdown("### 💾 Export Resume")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📥 Download PDF", use_container_width=True):
                    st.info("🔄 Generating PDF...")
            with col2:
                if st.button("📥 Download DOCX", use_container_width=True):
                    st.info("🔄 Generating DOCX...")
            with col3:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.success("✅ Copied!")
            with col4:
                if st.button("🚀 Apply with This Resume", use_container_width=True):
                    st.session_state.umarketu_state['current_step'] = 'track'
                    st.rerun()

# ===========================
# TAB 4: APPLICATION TRACKER
# ===========================
with tab4:
    st.header("📋 Application Tracker")
    st.markdown("**US7**: Log every application with structured fields; link to resume version sent")
    
    # Quick stats
    total_apps = len(st.session_state.umarketu_state.get('applications', []))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Applications", total_apps)
    with col2:
        st.metric("In Progress", 5)
    with col3:
        st.metric("Interviews", 2)
    with col4:
        st.metric("Offers", 1)
    
    # Add new application
    with st.expander("➕ Add New Application", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            app_company = st.text_input("Company")
            app_title = st.text_input("Job Title")
            app_location = st.text_input("Location")
            app_salary = st.text_input("Salary Range")
        
        with col2:
            app_status = st.selectbox("Status", ["Applied", "Phone Screen", "Interview", "Offer", "Rejected", "Withdrawn"])
            app_applied_date = st.date_input("Applied Date", datetime.now())
            app_contact_name = st.text_input("Contact Name")
            app_contact_email = st.text_input("Contact Email")
        
        app_resume_version = st.selectbox("Resume Version Used", ["Master Resume", "v2025_001 (ML Engineer)", "v2025_002 (Data Scientist)"])
        app_notes = st.text_area("Notes", placeholder="Additional details, follow-up actions, etc.")
        
        if st.button("💾 Save Application", type="primary"):
            st.success("✅ Application logged!")
    
    # Applications table
    st.markdown("### 📊 Your Applications")
    
    # Demo applications data
    apps_data = [
        {
            'Company': 'TechCorp AI',
            'Title': 'Senior ML Engineer',
            'Location': 'London, UK',
            'Status': '🟢 Interview',
            'Applied': '2025-10-20',
            'Last Update': '2025-10-24',
            'Resume': 'v2025_001',
            'Fit': '85%',
            'Next Action': 'Final round 2025-10-28'
        },
        {
            'Company': 'FinTech Innovations',
            'Title': 'Data Science Lead',
            'Location': 'London, UK',
            'Status': '🟡 Phone Screen',
            'Applied': '2025-10-18',
            'Last Update': '2025-10-22',
            'Resume': 'v2025_002',
            'Fit': '78%',
            'Next Action': 'Call scheduled 2025-10-26'
        },
        {
            'Company': 'DeepLearn Labs',
            'Title': 'ML Engineer - NLP',
            'Location': 'Cambridge, UK',
            'Status': '🔵 Applied',
            'Applied': '2025-10-25',
            'Last Update': '2025-10-25',
            'Resume': 'v2025_001',
            'Fit': '92%',
            'Next Action': 'Wait for response'
        }
    ]
    
    df_apps = pd.DataFrame(apps_data)
    st.dataframe(df_apps, use_container_width=True, height=300)
    
    # Application timeline (for selected application)
    st.markdown("### 📅 Application Timeline")
    selected_app = st.selectbox("Select application to view timeline", [f"{a['Title']} at {a['Company']}" for a in apps_data])
    
    if selected_app:
        # Timeline events
        timeline_data = [
            {'Date': '2025-10-20', 'Event': 'Applied', 'Details': 'Resume submitted via LinkedIn'},
            {'Date': '2025-10-22', 'Event': 'Application Viewed', 'Details': 'Recruiter viewed profile'},
            {'Date': '2025-10-24', 'Event': 'Interview Scheduled', 'Details': 'Final round with engineering team'},
            {'Date': '2025-10-28', 'Event': 'Interview', 'Details': 'Technical + behavioral (scheduled)'}
        ]
        
        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, use_container_width=True)
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎤 Prepare Interview", use_container_width=True):
                st.session_state.umarketu_state['current_step'] = 'coach'
                st.rerun()
        with col2:
            if st.button("📧 Draft Follow-up", use_container_width=True):
                st.info("📝 Opening outreach assistant...")
        with col3:
            if st.button("📝 Update Status", use_container_width=True):
                st.info("✏️ Opening status editor...")

# ===========================
# TAB 5: INTERVIEW COACH
# ===========================
with tab5:
    st.header("🎤 Interview Coach")
    st.markdown("**US8**: Get tailored Q&A pack, company intel, timeline prep, behavior/mindset tips")
    
    # Select job or standalone
    coach_mode = st.radio(
        "Interview Mode",
        ["📋 Linked to Application", "🆕 Standalone Prep"],
        horizontal=True
    )
    
    if coach_mode == "📋 Linked to Application":
        linked_job = st.selectbox(
            "Select Application",
            ["Senior ML Engineer at TechCorp AI", "Data Science Lead at FinTech Innovations"]
        )
        st.success(f"✅ Loading interview prep for: **{linked_job}**")
        
        # Pull fit insights
        st.info("💡 Using fit analysis and resume variant to generate talking points")
    else:
        st.text_input("Company Name", placeholder="Enter company name")
        st.text_input("Role Title", placeholder="e.g., Senior ML Engineer")
    
    # Generate interview pack
    if st.button("🎯 Generate Interview Pack", type="primary"):
        with st.spinner("🧠 Preparing your interview pack..."):
            st.session_state.umarketu_state['interview_prep'] = {
                'company_intel': "TechCorp AI is a leading AI research company...",
                'qa_count': 28,
                'generated_at': datetime.now().isoformat()
            }
            st.success("✅ Interview pack ready!")
    
    # Display interview pack
    if st.session_state.umarketu_state.get('interview_prep'):
        prep = st.session_state.umarketu_state['interview_prep']
        
        # Interview pack sections
        subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
            "🏢 Company Intel",
            "❓ Q&A Pack",
            "🎭 Behavioral",
            "📅 Day-of Logistics",
            "✉️ Follow-up"
        ])
        
        with subtab1:
            st.markdown("### 🏢 Company Intelligence")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📰 Recent News")
                st.markdown("""
                - **Oct 2025**: Raised $50M Series B led by Sequoia
                - **Sep 2025**: Launched AI-powered analytics platform
                - **Aug 2025**: Acquired DataViz startup for $10M
                """)
                
                st.markdown("#### 🏆 Products & Services")
                st.markdown("""
                - **TechCorp ML Cloud**: Enterprise ML platform
                - **InsightAI**: Real-time analytics engine
                - **AutoML Suite**: Automated model training
                """)
            
            with col2:
                st.markdown("#### 👥 Team Structure")
                st.markdown("""
                - **Engineering**: 45 people, 5 teams
                - **ML Team**: 12 engineers, led by Dr. Sarah Chen
                - **Tech Stack**: Python, TensorFlow, Kubernetes, AWS
                """)
                
                st.markdown("#### 💡 Culture Notes")
                st.markdown("""
                - Fast-paced startup environment
                - Strong emphasis on R&D
                - Remote-friendly with quarterly offsites
                """)
        
        with subtab2:
            st.markdown("### ❓ Tailored Q&A Pack")
            st.markdown(f"**{prep['qa_count']} questions** prepared based on your profile and the role")
            
            # Sample questions
            qa_sections = {
                "Technical (10)": [
                    "Explain the difference between L1 and L2 regularization",
                    "How would you handle imbalanced datasets?",
                    "Walk me through deploying an ML model to production"
                ],
                "Behavioral (8)": [
                    "Tell me about a time you disagreed with your team on a technical decision",
                    "Describe a project that didn't go as planned. What did you learn?"
                ],
                "Company-Specific (6)": [
                    "Why TechCorp AI specifically?",
                    "What interests you about our AutoML Suite product?"
                ],
                "Your Background (4)": [
                    "I see you have 8 years of Python experience. What's your favorite feature in Python 3.11?",
                    "Tell me about your most impactful ML project"
                ]
            }
            
            for section, questions in qa_sections.items():
                with st.expander(f"📚 {section}", expanded=False):
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"**Q{i}**: {q}")
                        st.markdown("**Suggested Answer Framework**:")
                        st.info("🎯 Touch Point: Highlight your relevant experience...")
                        st.markdown("---")
        
        with subtab3:
            st.markdown("### 🎭 Behavioral Interview Prep")
            
            st.markdown("#### 🌟 STAR Method Framework")
            st.code("""
Situation: Set the context
Task: Describe the challenge
Action: Explain what YOU did
Result: Quantify the outcome
""")
            
            st.markdown("#### 💪 Your Evidence Talking Points")
            st.markdown("""
            Based on your resume and fit analysis:
            
            1. **Leadership**: Led team of 5 engineers on ML platform migration
            2. **Problem-Solving**: Reduced model latency by 60% through optimization
            3. **Impact**: Delivered $200k cost savings through cloud optimization
            4. **Innovation**: Pioneered use of transformer models for customer segmentation
            5. **Communication**: Presented ML findings to C-suite, securing $500k budget
            """)
            
            st.markdown("#### 🚫 Common Pitfalls to Avoid")
            st.warning("""
            - ❌ Rambling without structure (use STAR!)
            - ❌ Taking sole credit for team efforts (say "we" then "I")
            - ❌ Negative talk about previous employers
            - ❌ Vague answers without metrics
            """)
        
        with subtab4:
            st.markdown("### 📅 Day-of-Interview Logistics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ⏰ Timeline")
                st.markdown("""
                **T-24 hours**:
                - ✅ Review company intel
                - ✅ Practice top 10 questions
                - ✅ Prepare 3 questions to ask
                
                **T-2 hours**:
                - ✅ Test video setup (if remote)
                - ✅ Print resume copy
                - ✅ Eat light meal
                
                **T-15 minutes**:
                - ✅ Deep breathing exercises
                - ✅ Review key talking points
                - ✅ Smile!
                """)
            
            with col2:
                st.markdown("#### 🎒 Checklist")
                st.checkbox("Resume copies (3x)", value=False)
                st.checkbox("Notepad + pen", value=False)
                st.checkbox("Portfolio/project samples", value=False)
                st.checkbox("Questions to ask (prepared list)", value=False)
                st.checkbox("Contact details (recruiter/interviewer)", value=False)
                st.checkbox("Water bottle", value=False)
                
                st.markdown("#### 💡 Mindset Tips")
                st.success("""
                - 🧘 You're evaluating them too
                - 💪 Your achievements speak for themselves
                - 🎯 Focus on fit, not perfection
                - 😊 Authenticity > memorization
                """)
        
        with subtab5:
            st.markdown("### ✉️ Follow-up Email Drafts")
            
            # Generate follow-up emails
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📧 Thank You Email (24h after)")
                st.code("""
Subject: Thank you - Senior ML Engineer Interview

Dear [Interviewer Name],

Thank you for taking the time to speak with me 
yesterday about the Senior ML Engineer role at 
TechCorp AI.

I was particularly excited to learn about your 
AutoML Suite roadmap and how the team is pushing 
the boundaries of automated model deployment.

My experience with [specific project discussed] 
aligns closely with your team's goals, and I'm 
confident I can contribute meaningfully from day one.

Please don't hesitate to reach out if you need 
any additional information.

Looking forward to next steps!

Best regards,
[Your Name]
""")
            
            with col2:
                st.markdown("#### 🔄 Polite Follow-up (1 week after)")
                st.code("""
Subject: Following up - Senior ML Engineer Role

Hi [Recruiter Name],

I wanted to follow up on my interview last week 
for the Senior ML Engineer position.

I remain very interested in the opportunity and 
would love to know if there are any updates on 
the timeline.

Please let me know if you need anything further 
from my side.

Thank you!

Best,
[Your Name]
""")
            
            if st.button("📋 Copy Email Template"):
                st.success("✅ Copied to clipboard!")

# ===========================
# TAB 6: PARTNER MODE
# ===========================
with tab6:
    st.header("👥 Partner Mode - Dual Career Optimizer")
    st.markdown("**US9**: Add partner profile and run dual-career search with travel constraints")
    
    # Tier gate for partner mode
    if user_tier not in ['annual_pro', 'enterprise_pro']:
        st.warning("🔒 **Partner Mode** is available for Annual Pro and Enterprise Pro tiers")
        if st.button("⬆️ Upgrade to Annual Pro"):
            st.switch_page("pages/06_Pricing.py")
        st.stop()
    
    # Partner profile setup
    st.markdown("### 👤 Partner Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Partner 1 (You)")
        p1_name = st.text_input("Name", value=st.session_state.get('user_email', 'User 1'), key="p1_name")
        p1_resume = st.file_uploader("Resume", type=['pdf', 'docx'], key="p1_resume")
        p1_roles = st.text_input("Target Roles", value="ML Engineer, Data Scientist", key="p1_roles")
        p1_min_salary = st.number_input("Min Salary (£)", 50000, 200000, 60000, key="p1_salary")
    
    with col2:
        st.markdown("#### Partner 2")
        p2_name = st.text_input("Name", value="Partner", key="p2_name")
        p2_resume = st.file_uploader("Resume", type=['pdf', 'docx'], key="p2_resume")
        p2_roles = st.text_input("Target Roles", value="UX Designer, Product Manager", key="p2_roles")
        p2_min_salary = st.number_input("Min Salary (£)", 50000, 200000, 55000, key="p2_salary")
    
    # Geographic constraints
    st.markdown("### 🗺️ Geographic & Lifestyle Constraints")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_commute_p1 = st.slider("P1 Max Commute (km)", 0, 100, 30, 5)
        max_commute_p2 = st.slider("P2 Max Commute (km)", 0, 100, 25, 5)
    
    with col2:
        remote_flex_p1 = st.select_slider("P1 Remote Flexibility", ["On-site only", "Hybrid", "Fully Remote"], value="Hybrid")
        remote_flex_p2 = st.select_slider("P2 Remote Flexibility", ["On-site only", "Hybrid", "Fully Remote"], value="Hybrid")
    
    with col3:
        relocation_willing = st.checkbox("Open to Relocation", value=True)
        if relocation_willing:
            relocation_budget = st.number_input("Relocation Budget (£)", 0, 50000, 10000, 1000)
    
    # Run dual-career optimizer
    if st.button("🔍 Find Optimal Cities & Jobs", type="primary", use_container_width=True):
        with st.spinner("🧠 Optimizing dual-career opportunities..."):
            # Would call: POST /partner/optimize {user_id, partner_id, params}
            st.success("✅ Found optimal dual-career opportunities!")
            
            # Results
            st.markdown("### 🎯 Top 5 Dual-Career Cities")
            
            dual_results = [
                {
                    'City': 'London, UK',
                    'P1 Jobs': 127,
                    'P2 Jobs': 89,
                    'Combined Score': 92,
                    'Avg Commute': '22 min',
                    'Combined Salary': '£125k - £165k',
                    'Cost of Living': 'High'
                },
                {
                    'City': 'Manchester, UK',
                    'P1 Jobs': 45,
                    'P2 Jobs': 38,
                    'Combined Score': 85,
                    'Avg Commute': '18 min',
                    'Combined Salary': '£95k - £130k',
                    'Cost of Living': 'Medium'
                },
                {
                    'City': 'Cambridge, UK',
                    'P1 Jobs': 38,
                    'P2 Jobs': 24,
                    'Combined Score': 78,
                    'Avg Commute': '15 min',
                    'Combined Salary': '£100k - £140k',
                    'Cost of Living': 'High'
                },
                {
                    'City': 'Edinburgh, UK',
                    'P1 Jobs': 32,
                    'P2 Jobs': 28,
                    'Combined Score': 76,
                    'Avg Commute': '20 min',
                    'Combined Salary': '£90k - £125k',
                    'Cost of Living': 'Medium'
                },
                {
                    'City': 'Bristol, UK',
                    'P1 Jobs': 29,
                    'P2 Jobs': 31,
                    'Combined Score': 74,
                    'Avg Commute': '19 min',
                    'Combined Salary': '£92k - £128k',
                    'Cost of Living': 'Medium'
                }
            ]
            
            df_dual = pd.DataFrame(dual_results)
            st.dataframe(df_dual, use_container_width=True)
            
            # Visualization: Dual dartboard
            st.markdown("### 🎯 Dual-Career Opportunity Dartboard")
            
            fig = go.Figure()
            
            for result in dual_results:
                fig.add_trace(go.Scatterpolar(
                    r=[result['P1 Jobs']/2, result['P2 Jobs']/2, result['Combined Score'], 
                       (150 - len(result['City']))*2, 100 - (50 if result['Cost of Living'] == 'High' else 25)],
                    theta=['P1 Opportunities', 'P2 Opportunities', 'Overall Fit', 'Lifestyle', 'Affordability'],
                    fill='toself',
                    name=result['City']
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title="Multi-Dimensional Dual-Career Analysis",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed city view
            selected_city = st.selectbox("🏙️ View Details for City", [r['City'] for r in dual_results])
            
            if selected_city:
                city_data = next(r for r in dual_results if r['City'] == selected_city)
                
                st.markdown(f"### 📍 {selected_city} - Detailed Breakdown")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"#### Partner 1 ({p1_name}) Opportunities")
                    st.metric("Job Matches", city_data['P1 Jobs'])
                    st.markdown("**Top 3 Jobs:**")
                    st.markdown("1. Senior ML Engineer at TechCorp - £70k-£95k")
                    st.markdown("2. Data Scientist at FinTech Co - £65k-£85k")
                    st.markdown("3. ML Lead at AI Startup - £75k-£100k")
                
                with col2:
                    st.markdown(f"#### Partner 2 ({p2_name}) Opportunities")
                    st.metric("Job Matches", city_data['P2 Jobs'])
                    st.markdown("**Top 3 Jobs:**")
                    st.markdown("1. Senior UX Designer at DesignCo - £55k-£75k")
                    st.markdown("2. Product Manager at SaaS Firm - £60k-£80k")
                    st.markdown("3. UX Lead at E-commerce - £58k-£78k")
                
                # Commute analysis
                st.markdown("#### 🚗 Commute Overlap Zones")
                st.info(f"""
                **Optimal Living Areas**: 
                - Central {selected_city.split(',')[0]} (avg 15-20 min commute for both)
                - North District (avg 18-25 min for P1, 20-28 min for P2)
                - East Quarter (avg 22-30 min for both)
                
                **Combined Cost of Living**: {city_data['Cost of Living']} 
                **Quality of Life Score**: 8.2/10
                """)

# Footer with next actions
st.markdown("---")
st.markdown("### 🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💾 Save Progress", use_container_width=True):
        st.success("✅ Progress saved!")

with col2:
    if st.button("📊 View Analytics", use_container_width=True):
        st.info("📈 Opening analytics dashboard...")

with col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.info("🔧 Opening settings...")

with col4:
    if st.button("❓ Help & Tutorials", use_container_width=True):
        st.info("📚 Opening help center...")

# Session state debug (for development)
if st.checkbox("🔧 Debug: Show Session State", value=False):
    st.json(st.session_state.umarketu_state)
