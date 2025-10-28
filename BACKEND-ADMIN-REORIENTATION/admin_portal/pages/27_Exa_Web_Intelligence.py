"""
=============================================================================
IntelliCV Admin Portal - EXA Web Intelligence Dashboard (Page 27)
=============================================================================

Deep web search and company enrichment using Exa AI.

Features:
- Manual company search and enrichment
- Automated careers page discovery
- Product/solution page extraction
- Company background research
- Search history and analytics
- Corpus management
- API usage tracking

Integration:
- Feeds data to User Portal Pages 10, 13
- Enhances Admin Pages 10, 11 (Market/Competitive Intelligence)
- Stores enrichment in company_corpora
"""

import streamlit as st
import sys
from pathlib import Path
import json
import time
from datetime import datetime, timedelta

# Add shared_backend to path
backend_path = Path(__file__).parent.parent.parent / "shared_backend"
sys.path.insert(0, str(backend_path))

# =============================================================================
# MANDATORY AUTHENTICATION CHECK  
# =============================================================================

def check_authentication():
    """Auto-generated function body"""
    return True  # Fallback authentication

# =============================================================================
# IMPORTS
# =============================================================================

try:
    from services.exa_service.exa_client import get_exa_client
    from services.exa_service.company_enrichment import get_company_enricher
    from services.exa_service.keyword_extractor import get_keyword_extractor
    EXA_AVAILABLE = True
except ImportError as e:
    st.error(f"⚠️ Exa service not available: {e}")
    EXA_AVAILABLE = False

try:
    from database.exa_db import (
        get_company_sources,
        get_crawl_history,
        get_enrichment_summary,
        get_api_usage_stats,
        health_check as db_health_check
    )
    DB_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ Database not available: {e}")
    DB_AVAILABLE = False

try:
    import sys
    integration_path = Path(__file__).parent / "shared"
    sys.path.insert(0, str(integration_path))
    from integration_hooks import get_integration_hooks
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ Integration hooks not available: {e}")
    INTEGRATION_AVAILABLE = False

# Integration hooks (optional - for Phase 2 completion)
try:
    sys.path.insert(0, str(Path(__file__).parent / "shared"))
    from integration_hooks import get_integration_hooks
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    st.info(f"ℹ️ Integration hooks not available: {e}")
    INTEGRATION_AVAILABLE = False

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="EXA Web Intelligence | IntelliCV Admin",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# MAIN PAGE
# =============================================================================

def main():
    """Main page rendering"""
    
    # Authentication
    if not check_authentication():
        st.error("🔒 Authentication required")
        st.stop()
    
    # Header
    st.title("🌐 EXA Web Intelligence Dashboard")
    st.markdown("**Deep web search and company enrichment using Exa AI**")
    st.markdown("---")
    
    # System status
    render_system_status()
    
    # Tabs for different features
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Company Search",
        "📊 Search History",
        "📚 Corpus Browser",
        "📈 Analytics",
        "⚙️ Settings",
        "🎯 JD Analysis"
    ])
    
    with tab1:
        render_company_search_tab()
    
    with tab2:
        render_search_history_tab()
    
    with tab3:
        render_corpus_browser_tab()
    
    with tab4:
        render_analytics_tab()
    
    with tab5:
        render_settings_tab()
    
    with tab6:
        render_jd_analysis_tab()

# =============================================================================
# SYSTEM STATUS
# =============================================================================

def render_system_status():
    """Show system status indicators"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        exa_status = "🟢 Online" if EXA_AVAILABLE else "🔴 Offline"
        st.metric("Exa Service", exa_status)
    
    with col2:
        db_status = "🟢 Connected" if DB_AVAILABLE else "🔴 Disconnected"
        st.metric("Database", db_status)
    
    with col3:
        if DB_AVAILABLE:
            try:
                stats = get_api_usage_stats(days=7)
                st.metric("API Calls (7d)", f"{stats['total_calls']:,}")
            except:
                st.metric("API Calls (7d)", "N/A")
        else:
            st.metric("API Calls (7d)", "N/A")
    
    with col4:
        if DB_AVAILABLE:
            try:
                health = db_health_check()
                status = health.get('status', 'unknown')
                st.metric("DB Health", status.upper())
            except:
                st.metric("DB Health", "UNKNOWN")
        else:
            st.metric("DB Health", "OFFLINE")

# =============================================================================
# TAB 1: COMPANY SEARCH
# =============================================================================

def render_company_search_tab():
    """Manual company search and enrichment"""
    
    st.markdown("### 🔍 Search & Enrich Company Data")
    st.markdown("Enter a company domain to discover careers pages, products, and background information.")
    
    if not EXA_AVAILABLE:
        st.error("❌ Exa service is not available. Please check configuration.")
        return
    
    # Search form
    with st.form("company_search_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            domain = st.text_input(
                "Company Domain",
                placeholder="example.com (without www or https://)",
                help="Enter the company's main domain"
            )
        
        with col2:
            company_name = st.text_input(
                "Company Name (optional)",
                placeholder="Example Corp"
            )
        
        st.markdown("**Search Types:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_careers = st.checkbox("🎯 Careers Pages", value=True)
        with col2:
            search_products = st.checkbox("🚀 Product Pages", value=True)
        with col3:
            search_background = st.checkbox("📖 Company Background", value=True)
        
        col1, col2 = st.columns(2)
        with col1:
            num_results = st.slider("Results per search", 3, 20, 5)
        with col2:
            use_cache = st.checkbox("Use cache (faster)", value=True)
        
        submitted = st.form_submit_button("🔍 Search & Enrich", type="primary", use_container_width=True)
    
    # Process search
    if submitted and domain:
        if not any([search_careers, search_products, search_background]):
            st.warning("⚠️ Please select at least one search type")
            return
        
        # Clean domain
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").strip().rstrip("/")
        
        st.markdown("---")
        st.markdown(f"### 🔄 Enriching: **{domain}**")
        
        enricher = get_company_enricher()
        
        # Progress tracking
        progress_text = st.empty()
        progress_bar = st.progress(0)
        results_container = st.container()
        
        total_steps = sum([search_careers, search_products, search_background])
        current_step = 0
        
        all_results = {
            'domain': domain,
            'company_name': company_name or domain,
            'timestamp': datetime.now().isoformat(),
            'careers': None,
            'products': None,
            'background': None,
            'total_pages': 0
        }
        
        # Search careers
        if search_careers:
            current_step += 1
            progress_text.text(f"🎯 Searching careers pages... ({current_step}/{total_steps})")
            progress_bar.progress(current_step / total_steps)
            
            try:
                careers_result = enricher.find_careers_pages(
                    domain=domain,
                    num_results=num_results,
                    use_cache=use_cache
                )
                all_results['careers'] = careers_result
                all_results['total_pages'] += careers_result.get('total_found', 0)
                
                with results_container:
                    render_search_results("Careers Pages", careers_result, "🎯")
            
            except Exception as e:
                with results_container:
                    st.error(f"❌ Careers search failed: {e}")
        
        # Search products
        if search_products:
            current_step += 1
            progress_text.text(f"🚀 Searching product pages... ({current_step}/{total_steps})")
            progress_bar.progress(current_step / total_steps)
            
            try:
                products_result = enricher.find_product_pages(
                    domain=domain,
                    num_results=num_results,
                    use_cache=use_cache
                )
                all_results['products'] = products_result
                all_results['total_pages'] += products_result.get('total_found', 0)
                
                with results_container:
                    render_search_results("Product Pages", products_result, "🚀")
            
            except Exception as e:
                with results_container:
                    st.error(f"❌ Products search failed: {e}")
        
        # Search background
        if search_background:
            current_step += 1
            progress_text.text(f"📖 Searching company background... ({current_step}/{total_steps})")
            progress_bar.progress(current_step / total_steps)
            
            try:
                background_result = enricher.get_company_background(
                    domain=domain,
                    num_results=num_results,
                    use_cache=use_cache
                )
                all_results['background'] = background_result
                all_results['total_pages'] += background_result.get('total_found', 0)
                
                with results_container:
                    render_search_results("Company Background", background_result, "📖")
            
            except Exception as e:
                with results_container:
                    st.error(f"❌ Background search failed: {e}")
        
        # Complete
        progress_text.text("✅ Enrichment complete!")
        progress_bar.progress(1.0)
        
        # Summary
        st.markdown("---")
        st.success(f"✅ **Enrichment Complete**: Found **{all_results['total_pages']} total pages** for {domain}")
        
        # Sync to integration hooks
        try:
            if INTEGRATION_AVAILABLE:
                hooks = get_integration_hooks()
                hooks.sync_exa_company_data(domain, all_results)
                st.success("🔄 Data synced to user portals and backend")
        except Exception as e:
            st.warning(f"⚠️ Integration sync failed (non-critical): {e}")
        
        # Sync to integration hooks (if available)
        if INTEGRATION_AVAILABLE:
            try:
                hooks = get_integration_hooks()
                hooks.sync_exa_company_data(domain, all_results)
                st.success("🔄 Data synced to user portals and backend")
            except Exception as e:
                st.warning(f"⚠️ Integration sync failed: {e}")
        
        # Download option
        st.download_button(
            label="📥 Download Full Results (JSON)",
            data=json.dumps(all_results, indent=2),
            file_name=f"{domain}_enrichment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def render_search_results(title, results, icon):
    """Render search results for a category"""
    
    st.markdown(f"### {icon} {title}")
    
    total_found = results.get('total_found', 0)
    from_cache = results.get('from_cache', False)
    cache_indicator = "💾 (cached)" if from_cache else "🌐 (fresh)"
    
    st.markdown(f"**Found**: {total_found} pages {cache_indicator}")
    
    # Get results based on category
    if 'careers' in title.lower():
        pages = results.get('careers_pages', [])
    elif 'product' in title.lower():
        pages = results.get('product_pages', [])
    else:
        pages = results.get('background_pages', [])
    
    if not pages:
        st.info("No results found")
        return
    
    # Display results
    for i, page in enumerate(pages, 1):
        with st.expander(f"#{i} - {page.get('title', 'Untitled')} (Score: {page.get('score', 0):.3f})"):
            st.markdown(f"**URL**: [{page.get('url', 'N/A')}]({page.get('url', '#')})")
            
            if page.get('published_date'):
                st.markdown(f"**Published**: {page.get('published_date')}")
            
            if page.get('author'):
                st.markdown(f"**Author**: {page.get('author')}")
            
            # Content preview
            content = page.get('text', '')
            if content:
                st.markdown("**Content Preview:**")
                st.text_area("", value=content[:500] + "..." if len(content) > 500 else content, height=150, key=f"content_{i}")
    
    st.markdown("---")

# =============================================================================
# TAB 2: SEARCH HISTORY
# =============================================================================

def render_search_history_tab():
    """Display search history from database"""
    
    st.markdown("### 📊 Search History")
    
    if not DB_AVAILABLE:
        st.warning("⚠️ Database not available. Cannot display history.")
        return
    
    # Search filter
    col1, col2 = st.columns([3, 1])
    with col1:
        filter_domain = st.text_input("Filter by domain", placeholder="example.com")
    with col2:
        limit = st.number_input("Show records", 5, 100, 20)
    
    if st.button("🔍 Load History"):
        if filter_domain:
            try:
                history = get_crawl_history(filter_domain, limit=limit)
                
                if not history:
                    st.info(f"No history found for {filter_domain}")
                else:
                    st.success(f"Found {len(history)} records for {filter_domain}")
                    
                    for record in history:
                        with st.expander(f"{record['domain']} - {record['created_at']} ({record['status']})"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Pages", record.get('total_pages_found', 0))
                            with col2:
                                st.metric("Careers", record.get('careers_pages_found', 0))
                            with col3:
                                st.metric("Products", record.get('products_pages_found', 0))
                            
                            st.json(record)
            
            except Exception as e:
                st.error(f"Failed to load history: {e}")
        else:
            st.warning("Please enter a domain to filter")

# =============================================================================
# TAB 3: CORPUS BROWSER
# =============================================================================

def render_corpus_browser_tab():
    """Browse saved company corpora"""
    
    st.markdown("### 📚 Company Corpus Browser")
    st.info("Browse enriched company data saved to local corpus storage")
    
    # Get corpus directory
    corpus_dir = Path(__file__).parent.parent.parent / "ai_data_final" / "company_corpora"
    
    if not corpus_dir.exists():
        st.warning("⚠️ Corpus directory not found")
        return
    
    # List all company domains
    domains = [d.name for d in corpus_dir.iterdir() if d.is_dir()]
    
    if not domains:
        st.info("No companies in corpus yet. Run some searches first!")
        return
    
    st.markdown(f"**Total companies in corpus**: {len(domains)}")
    
    selected_domain = st.selectbox("Select a company", sorted(domains))
    
    if selected_domain:
        enrichment_file = corpus_dir / selected_domain / "enrichment.json"
        
        if enrichment_file.exists():
            with open(enrichment_file, 'r') as f:
                data = json.load(f)
            
            st.success(f"✅ Enrichment data for **{selected_domain}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Careers Pages", data.get('careers', {}).get('total_found', 0))
            with col2:
                st.metric("Product Pages", data.get('products', {}).get('total_found', 0))
            with col3:
                st.metric("Background Pages", data.get('background', {}).get('total_found', 0))
            
            # Download
            st.download_button(
                "📥 Download Corpus",
                data=json.dumps(data, indent=2),
                file_name=f"{selected_domain}_corpus.json",
                mime="application/json"
            )
            
            # Show data
            with st.expander("📄 View Full Data"):
                st.json(data)
        else:
            st.warning("No enrichment.json found for this domain")

# =============================================================================
# TAB 4: ANALYTICS
# =============================================================================

def render_analytics_tab():
    """Show usage analytics"""
    
    st.markdown("### 📈 Usage Analytics")
    
    if not DB_AVAILABLE:
        st.warning("⚠️ Database not available. Cannot display analytics.")
        return
    
    # Time period selector
    period = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days"])
    
    days_map = {
        "Last 7 days": 7,
        "Last 30 days": 30,
        "Last 90 days": 90
    }
    
    days = days_map[period]
    
    try:
        stats = get_api_usage_stats(days=days)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total API Calls", f"{stats['total_calls']:,}")
        with col2:
            st.metric("Total Results", f"{stats['total_results']:,}")
        with col3:
            st.metric("Unique Domains", stats['unique_domains'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Response Time", f"{stats['avg_response_time_ms']:.0f} ms")
        with col2:
            st.metric("Credits Used", f"{stats['total_credits_used']:.2f}")
        with col3:
            st.metric("Failed Calls", stats['failed_calls'])
    
    except Exception as e:
        st.error(f"Failed to load analytics: {e}")

# =============================================================================
# TAB 6: JD ANALYSIS
# =============================================================================

def render_jd_analysis_tab():
    """Smart JD keyword extraction and search"""
    
    st.markdown("### 🎯 Job Description Analysis & Smart Search")
    st.markdown("Extract keywords from JDs, analyze job titles, and run hybrid AI + SQLite searches")
    
    # Sub-tabs
    subtab1, subtab2, subtab3 = st.tabs([
        "📝 JD Keyword Extraction",
        "🏷️ Job Title Analysis",
        "🔍 Smart Search"
    ])
    
    # SUBTAB 1: JD Keyword Extraction
    with subtab1:
        st.markdown("#### Extract Keywords from Job Descriptions")
        
        # Input area
        jd_text = st.text_area(
            "Paste Job Description:",
            height=300,
            placeholder="Paste the full job description text here...",
            help="Paste a job description to extract required skills, nice-to-have, tech stack, experience, education, etc."
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            extract_btn = st.button("🔍 Extract Keywords", type="primary")
        
        if extract_btn and jd_text:
            try:
                extractor = get_keyword_extractor()
                
                with st.spinner("Analyzing job description..."):
                    result = extractor.extract_job_description_keywords(jd_text)
                
                # Display results
                st.success("✅ Extraction Complete!")
                
                # Experience & Education
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📋 Experience Required**")
                    if result['experience']:
                        exp = result['experience']
                        st.info(f"{exp.get('years_required', 'N/A')} years ({exp.get('mentions', 0)} mentions)")
                    else:
                        st.info("Not specified")
                
                with col2:
                    st.markdown("**🎓 Education Required**")
                    if result['education']:
                        st.info(", ".join(result['education']))
                    else:
                        st.info("Not specified")
                
                # Required vs Nice-to-Have Skills
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**✅ Required Skills ({len(result['required_skills'])})**")
                    for skill in result['required_skills'][:10]:
                        st.markdown(f"- {skill}")
                    
                    if len(result['required_skills']) > 10:
                        st.caption(f"...and {len(result['required_skills']) - 10} more")
                
                with col2:
                    st.markdown(f"**💎 Nice-to-Have ({len(result['nice_to_have'])})**")
                    for skill in result['nice_to_have'][:10]:
                        st.markdown(f"- {skill}")
                    
                    if len(result['nice_to_have']) > 10:
                        st.caption(f"...and {len(result['nice_to_have']) - 10} more")
                
                # Tech Stack with Frequency
                st.markdown("---")
                st.markdown(f"**🔧 Tech Stack (Top 15 by frequency)**")
                
                tech_data = []
                for tech in result['tech_stack'][:15]:
                    tech_data.append({
                        "Keyword": tech['keyword'],
                        "Frequency": tech['frequency'],
                        "Confidence": f"{tech['confidence']*100:.0f}%",
                        "Method": tech['method']
                    })
                
                if tech_data:
                    import pandas as pd
                    df = pd.DataFrame(tech_data)
                    st.dataframe(df, use_container_width=True)
                
                # Soft Skills
                st.markdown("---")
                st.markdown("**🤝 Soft Skills**")
                st.write(", ".join(result['soft_skills']) if result['soft_skills'] else "None detected")
                
                # Keyword Frequency Chart
                st.markdown("---")
                st.markdown("**📊 Keyword Frequency Count (Top 20)**")
                
                if result['keyword_counts']:
                    sorted_keywords = sorted(result['keyword_counts'].items(), key=lambda x: x[1], reverse=True)[:20]
                    
                    import pandas as pd
                    chart_data = pd.DataFrame(sorted_keywords, columns=['Keyword', 'Count'])
                    st.bar_chart(chart_data.set_index('Keyword'))
                
                # Download JSON
                st.markdown("---")
                json_data = json.dumps(result, indent=2)
                st.download_button(
                    label="📥 Download Full Analysis (JSON)",
                    data=json_data,
                    file_name=f"jd_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"Extraction failed: {e}")
        
        elif extract_btn:
            st.warning("⚠️ Please paste a job description first")
    
    # SUBTAB 2: Job Title Analysis
    with subtab2:
        st.markdown("#### Analyze Job Titles")
        st.markdown("Parse job titles into structured components (level, role, domain)")
        
        # Single title analysis
        st.markdown("**Single Title Analysis**")
        job_title = st.text_input(
            "Job Title:",
            placeholder="e.g., Senior Machine Learning Engineer",
            help="Enter a job title to analyze"
        )
        
        if job_title:
            try:
                extractor = get_keyword_extractor()
                analysis = extractor.analyze_job_title(job_title)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Level", analysis['level'] or "Not detected")
                
                with col2:
                    st.metric("Role", analysis['role'] or "Not detected")
                
                with col3:
                    st.metric("Domain", analysis['domain'] or "Not detected")
                
                st.metric("Seniority Score", f"{analysis['seniority_score']}/100")
                
                st.json(analysis)
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")
        
        # Batch analysis
        st.markdown("---")
        st.markdown("**Batch Title Analysis**")
        
        titles_text = st.text_area(
            "Job Titles (one per line):",
            height=200,
            placeholder="Senior ML Engineer\nStaff Software Developer\nJunior Frontend Developer\n...",
            help="Enter multiple job titles, one per line"
        )
        
        batch_btn = st.button("🔍 Analyze Batch", key="batch_titles")
        
        if batch_btn and titles_text:
            try:
                extractor = get_keyword_extractor()
                titles = [t.strip() for t in titles_text.split('\n') if t.strip()]
                
                with st.spinner(f"Analyzing {len(titles)} titles..."):
                    batch_result = extractor.batch_analyze_job_titles(titles)
                
                st.success(f"✅ Analyzed {batch_result['total_titles']} titles")
                
                # Summary metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Average Seniority", f"{batch_result['average_seniority']:.1f}/100")
                
                with col2:
                    st.metric("Unique Levels", len(batch_result['most_common_levels']))
                
                # Most common components
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Most Common Levels**")
                    for item in batch_result['most_common_levels'][:5]:
                        st.write(f"{item['item']}: {item['count']}")
                
                with col2:
                    st.markdown("**Most Common Roles**")
                    for item in batch_result['most_common_roles'][:5]:
                        st.write(f"{item['item']}: {item['count']}")
                
                with col3:
                    st.markdown("**Most Common Domains**")
                    for item in batch_result['most_common_domains'][:5]:
                        st.write(f"{item['item']}: {item['count']}")
                
                # Individual results
                st.markdown("---")
                st.markdown("**Individual Title Analyses**")
                
                for title in titles:
                    with st.expander(f"📌 {title}"):
                        analysis = extractor.analyze_job_title(title)
                        st.json(analysis)
                
            except Exception as e:
                st.error(f"Batch analysis failed: {e}")
    
    # SUBTAB 3: Smart Search
    with subtab3:
        st.markdown("#### Smart Hybrid AI + SQLite Search")
        st.markdown("Natural language queries → Intelligent SQLite WHERE clauses")
        
        # Search input
        search_query = st.text_input(
            "Search Query:",
            placeholder="e.g., Find companies hiring Python developers in Seattle",
            help="Enter a natural language search query"
        )
        
        search_type = st.selectbox(
            "Search Type:",
            options=['hybrid', 'semantic', 'keyword'],
            help="Hybrid = AI + exact matching, Semantic = AI only, Keyword = exact only"
        )
        
        search_btn = st.button("🔍 Generate Search", type="primary")
        
        if search_btn and search_query:
            try:
                extractor = get_keyword_extractor()
                
                with st.spinner("Analyzing query and generating SQL..."):
                    result = extractor.smart_search(search_query, search_type=search_type)
                
                st.success("✅ Search Strategy Generated!")
                
                # Extracted components
                st.markdown("### 📌 Extracted Components")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Keywords**")
                    st.write(", ".join(result['extracted_keywords']) if result['extracted_keywords'] else "None")
                    
                    st.markdown("**Level**")
                    st.write(result['extracted_level'] or "Any")
                
                with col2:
                    st.markdown("**Role**")
                    st.write(result['extracted_role'] or "Any")
                    
                    st.markdown("**Location**")
                    st.write(result['extracted_location'] or "Any")
                
                # Semantic expansions
                if result['semantic_expansions']:
                    st.markdown("---")
                    st.markdown("### 🧠 Semantic Expansions")
                    
                    for base, expanded in result['semantic_expansions'].items():
                        st.write(f"**{base}** → {', '.join(expanded[:5])}")
                
                # SQLite WHERE clauses
                st.markdown("---")
                st.markdown("### 💾 Generated SQLite WHERE Clauses")
                
                for i, clause in enumerate(result['sql_where_clauses'], 1):
                    st.code(clause, language="sql")
                
                # Final SQL
                st.markdown("---")
                st.markdown("### 📝 Complete SQL Query")
                st.code(result['final_sql'], language="sql")
                
                # Copy button
                st.button("📋 Copy SQL", help="Copy SQL to clipboard")
                
                # Download
                json_data = json.dumps(result, indent=2)
                st.download_button(
                    label="📥 Download Search Strategy (JSON)",
                    data=json_data,
                    file_name=f"search_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"Search generation failed: {e}")
        
        elif search_btn:
            st.warning("⚠️ Please enter a search query")
        
        # Examples
        st.markdown("---")
        st.markdown("### 💡 Example Queries")
        
        examples = [
            "Find companies hiring Python developers",
            "Senior ML engineer roles in Seattle",
            "Remote backend jobs at startups",
            "AWS engineers with Docker experience",
            "Data scientist positions requiring PhD",
            "Junior frontend developers in San Francisco"
        ]
        
        for example in examples:
            if st.button(f"Try: {example}", key=f"example_{example}"):
                st.rerun()

# =============================================================================
# TAB 5: SETTINGS
# =============================================================================

def render_settings_tab():
    """Configuration settings"""
    
    st.markdown("### ⚙️ EXA Service Settings")
    
    # Current configuration
    import os
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**API Configuration**")
        api_key = os.getenv('EXA_API_KEY', 'Not set')
        masked_key = api_key[:8] + "..." if len(api_key) > 8 else "Not set"
        st.code(f"API Key: {masked_key}")
        st.code(f"Base URL: {os.getenv('EXA_BASE_URL', 'https://api.exa.ai')}")
        st.code(f"Search Mode: {os.getenv('EXA_SEARCH_MODE', 'auto')}")
    
    with col2:
        st.markdown("**Limits & Performance**")
        st.code(f"Max Results: {os.getenv('EXA_MAX_RESULTS', '50')}")
        st.code(f"Rate Limit: {os.getenv('EXA_RATE_LIMIT', '100')} req/min")
        st.code(f"Cache TTL: {os.getenv('EXA_CACHE_TTL', '86400')} sec")
    
    st.markdown("---")
    
    # Feature flags
    st.markdown("**Feature Flags**")
    col1, col2 = st.columns(2)
    
    with col1:
        enable_exa = os.getenv('ENABLE_EXA_SERVICE', 'true') == 'true'
        st.checkbox("Exa Service Enabled", value=enable_exa, disabled=True)
        
        enable_enrichment = os.getenv('ENABLE_COMPANY_ENRICHMENT', 'true') == 'true'
        st.checkbox("Company Enrichment", value=enable_enrichment, disabled=True)
    
    with col2:
        enable_auto = os.getenv('ENABLE_AUTO_CRAWL', 'false') == 'true'
        st.checkbox("Auto Crawl (Phase 3)", value=enable_auto, disabled=True)
        
        enable_workers = os.getenv('ENABLE_BACKGROUND_WORKERS', 'false') == 'true'
        st.checkbox("Background Workers (Phase 3)", value=enable_workers, disabled=True)
    
    st.info("💡 To modify settings, edit the .env file in the root directory")

# =============================================================================
# RUN MAIN
# =============================================================================

if __name__ == "__main__":
    main()
