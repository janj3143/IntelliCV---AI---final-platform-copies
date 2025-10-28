"""
Job Title Backend Integration Helper
Connects user portal pages to the backend job title service
"""

import sys
from pathlib import Path
import streamlit as st
from typing import Dict, List, Any, Optional

# Add backend service path
backend_path = Path(__file__).parent.parent.parent / "admin_portal_final" / "backend" / "services"
sys.path.insert(0, str(backend_path))

try:
    from job_title_service import get_job_title_service, generate_word_cloud, analyze_job_title
    BACKEND_SERVICE_AVAILABLE = True
except ImportError:
    BACKEND_SERVICE_AVAILABLE = False

def call_backend_word_cloud(job_titles: List[str], user_id: str = "anonymous", source_page: str = "user_portal") -> Dict[str, Any]:
    """
    Call backend word cloud generation service.
    
    Args:
        job_titles: List of job titles to visualize
        user_id: User identifier
        source_page: Calling page name
    
    Returns:
        Dictionary with word cloud results or error message
    """
    if not BACKEND_SERVICE_AVAILABLE:
        return {
            'error': 'Backend service not available',
            'fallback_message': 'Job title word cloud service is temporarily unavailable. Please try again later.',
            'tokens_used': 0
        }
    
    try:
        # Get user ID from session if not provided
        if user_id == "anonymous" and 'user_id' in st.session_state:
            user_id = st.session_state['user_id']
        
        # Call backend service
        result = generate_word_cloud(job_titles, user_id, source_page)
        
        # Track token usage in session
        if 'tokens_used_today' not in st.session_state:
            st.session_state['tokens_used_today'] = 0
        st.session_state['tokens_used_today'] += result.get('tokens_used', 0)
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'fallback_message': 'Unable to generate word cloud. Please try again.',
            'tokens_used': 0
        }

def call_backend_job_analysis(title: str, context: Dict[str, Any], user_id: str = "anonymous") -> Dict[str, Any]:
    """
    Call backend job title analysis service.
    
    Args:
        title: Job title to analyze
        context: Analysis context (current_title, target_titles, etc.)
        user_id: User identifier
    
    Returns:
        Dictionary with analysis results or error message
    """
    if not BACKEND_SERVICE_AVAILABLE:
        return {
            'error': 'Backend service not available',
            'fallback_message': 'Job title analysis service is temporarily unavailable. Please try again later.',
            'tokens_used': 0
        }
    
    try:
        # Get user ID from session if not provided
        if user_id == "anonymous" and 'user_id' in st.session_state:
            user_id = st.session_state['user_id']
        
        # Call backend service
        result = analyze_job_title(title, context, user_id)
        
        # Track token usage in session
        if 'tokens_used_today' not in st.session_state:
            st.session_state['tokens_used_today'] = 0
        st.session_state['tokens_used_today'] += result.get('tokens_used', 0)
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'fallback_message': 'Unable to analyze job title. Please try again.',
            'tokens_used': 0
        }

def display_word_cloud_result(result: Dict[str, Any]) -> None:
    """
    Display word cloud result in Streamlit UI.
    
    Args:
        result: Result from backend word cloud service
    """
    if 'error' in result:
        st.error(f"❌ {result.get('fallback_message', result['error'])}")
        return
    
    # Display word cloud image
    if 'wordcloud_image_base64' in result:
        import base64
        image_data = base64.b64decode(result['wordcloud_image_base64'])
        st.image(image_data, caption="Job Title Word Cloud", use_container_width=True)
    
    # Display insights
    if 'insights' in result:
        st.markdown(result['insights'])
    
    # Display token usage
    tokens_used = result.get('tokens_used', 0)
    if tokens_used > 0:
        st.info(f"🪙 **{tokens_used} tokens used** | Analysis completed successfully")

def display_job_analysis_result(result: Dict[str, Any]) -> None:
    """
    Display job analysis result in Streamlit UI.
    
    Args:
        result: Result from backend job analysis service
    """
    if 'error' in result:
        st.error(f"❌ {result.get('fallback_message', result['error'])}")
        return
    
    # Display similarity scores
    if 'similarity_scores' in result:
        st.subheader("🎯 Similarity Analysis")
        for score in result['similarity_scores']:
            st.write(f"**{score['target_title']}**: {score['similarity_score']}% match")
            if score.get('common_keywords'):
                st.write(f"Common keywords: {', '.join(score['common_keywords'])}")
    
    # Display skill overlaps
    if 'skill_overlaps' in result:
        st.subheader("🛠️ Skill Overlaps")
        for overlap in result['skill_overlaps']:
            st.write(f"**{overlap['skill_category']}**: {overlap['overlap_percentage']}%")
            st.write(f"Skills: {', '.join(overlap['skills'])}")
    
    # Display salary ranges
    if 'salary_ranges' in result:
        st.subheader("💰 Salary Estimates")
        salary = result['salary_ranges']
        st.write(f"**Range**: ${salary['min_salary']:,} - ${salary['max_salary']:,}")
        st.write(f"**Median**: ${salary['median_salary']:,}")
        st.write(f"**Confidence**: {salary['confidence']}")
    
    # Display career fit
    if 'career_fit' in result:
        st.subheader("📈 Career Fit Analysis")
        fit = result['career_fit']
        st.write(f"**Fit Score**: {fit['fit_score']}/100")
        st.write(f"**Transition Difficulty**: {fit['transition_difficulty']}")
        st.write(f"**Recommended Timeline**: {fit['recommended_timeline']}")
    
    # Display token usage
    tokens_used = result.get('tokens_used', 0)
    if tokens_used > 0:
        st.info(f"🪙 **{tokens_used} tokens used** | Analysis completed successfully")

def check_backend_service_status() -> Dict[str, Any]:
    """
    Check if backend service is available and get status.
    
    Returns:
        Service status dictionary
    """
    if not BACKEND_SERVICE_AVAILABLE:
        return {
            'available': False,
            'error': 'Backend service not imported',
            'message': 'Job title backend service is not available'
        }
    
    try:
        service = get_job_title_service()
        status = service.get_service_status()
        return {
            'available': True,
            'status': status,
            'message': 'Backend service is available'
        }
    except Exception as e:
        return {
            'available': False,
            'error': str(e),
            'message': 'Backend service encountered an error'
        }

# Helper function for easy UI integration
def show_backend_word_cloud_section(job_titles: List[str] = None, user_id: str = "anonymous", source_page: str = "user_portal"):
    """
    Show complete word cloud section with backend integration.
    
    Args:
        job_titles: Optional list of job titles (will use sample if not provided)
        user_id: User identifier
        source_page: Source page name
    """
    st.subheader("🎨 Job Title Word Cloud")
    st.write("Generate visual insights from job market data")
    
    # Input section
    if job_titles is None:
        job_titles_input = st.text_area(
            "Enter job titles (one per line)",
            value="Data Scientist\nSoftware Engineer\nProduct Manager\nUX Designer\nMarketing Manager",
            height=120
        )
        job_titles = [title.strip() for title in job_titles_input.split('\n') if title.strip()]
    
    # Token cost display
    st.info("🪙 **Cost: 5 tokens** | Generate visual insights from job market data")
    
    # Generate button
    if st.button("Generate Job Title Cloud", key="generate_word_cloud"):
        with st.spinner("Generating word cloud..."):
            result = call_backend_word_cloud(job_titles, user_id, source_page)
            display_word_cloud_result(result)

def show_backend_job_analysis_section(user_id: str = "anonymous"):
    """
    Show complete job analysis section with backend integration.
    
    Args:
        user_id: User identifier
    """
    st.subheader("🎯 Job Title Intelligence")
    st.write("Advanced job title analysis and career pathway intelligence")
    
    # Input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Analysis Input**")
        title_to_analyze = st.text_input("Job title to analyze", value="Data Scientist")
        current_title = st.text_input("Your current title", value="Data Analyst")
        industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Marketing", "Other"])
        experience_years = st.number_input("Years of experience", min_value=0, max_value=50, value=3)
    
    with col2:
        st.write("**Target Titles**")
        target_titles_input = st.text_area(
            "Target job titles (one per line)",
            value="Senior Data Analyst\nData Scientist\nBusiness Intelligence Analyst\nProduct Analyst",
            height=120
        )
        target_titles = [title.strip() for title in target_titles_input.split('\n') if title.strip()]
    
    # Token cost display
    st.info("🪙 **Cost: 7 tokens** | Advanced Tier Feature")
    
    # Analyze button
    if st.button("Analyze Job Title", key="analyze_job_title"):
        context = {
            'current_title': current_title,
            'target_titles': target_titles,
            'industry': industry,
            'experience_years': experience_years
        }
        
        with st.spinner("Analyzing job title..."):
            result = call_backend_job_analysis(title_to_analyze, context, user_id)
            display_job_analysis_result(result)

# Test function
def test_backend_integration():
    """Test backend integration functionality."""
    st.header("🧪 Backend Integration Test")
    
    # Check service status
    status = check_backend_service_status()
    if status['available']:
        st.success(f"✅ {status['message']}")
    else:
        st.error(f"❌ {status['message']}")
        if 'error' in status:
            st.write(f"Error: {status['error']}")
        return
    
    # Test word cloud
    st.subheader("Test Word Cloud Generation")
    if st.button("Test Word Cloud"):
        result = call_backend_word_cloud(
            job_titles=["Data Scientist", "Software Engineer", "Product Manager"],
            user_id="test_user",
            source_page="test"
        )
        display_word_cloud_result(result)
    
    # Test job analysis
    st.subheader("Test Job Analysis")
    if st.button("Test Job Analysis"):
        context = {
            'current_title': "Data Analyst",
            'target_titles': ["Senior Data Analyst", "Data Scientist"],
            'industry': "Technology",
            'experience_years': 3
        }
        result = call_backend_job_analysis("Data Scientist", context, "test_user")
        display_job_analysis_result(result)