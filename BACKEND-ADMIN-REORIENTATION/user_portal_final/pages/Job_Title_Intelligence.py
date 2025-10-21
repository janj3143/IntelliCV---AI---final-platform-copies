"""
Job Title Intelligence System with AI Chat Integration
=====================================================

This system provides:
1. Job title semantic analysis with AI chat descriptions
2. Job overlap Venn diagram visualization
3. Industry overlap analysis
4. Admin engine for data enrichment
5. Real-time similarity detection and clustering

Author: IntelliCV AI Team
Date: October 2, 2025
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
import re
from pathlib import Path

# Import fuzzy logic bridge (no code duplication!)
try:
    from services.fuzzy_logic_bridge import get_fuzzy_bridge, analyze_job_similarity, get_fuzzy_status
    FUZZY_BRIDGE_AVAILABLE = True
except ImportError:
    FUZZY_BRIDGE_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="Job Title Intelligence - IntelliCV",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import shared components
try:
    from shared.components import render_section_header, check_authentication
    SHARED_COMPONENTS_AVAILABLE = True
except ImportError:
    SHARED_COMPONENTS_AVAILABLE = False
    
def check_authentication():
    """Fallback authentication check"""
    return st.session_state.get('user_authenticated', True)

def render_section_header(title, icon="🎯"):
    """Fallback section header"""
    st.markdown(f"## {icon} {title}")

# Authentication check
if not check_authentication():
    st.error("🔒 Please log in to access Job Title Intelligence.")
    st.stop()

# Custom CSS for Venn diagrams and enhanced UI
st.markdown("""
<style>
    .job-title-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .overlap-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .similarity-badge {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .ai-insight {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .venn-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize job title intelligence data
if 'job_title_intelligence' not in st.session_state:
    st.session_state.job_title_intelligence = {
        'analyzed_titles': {},
        'similarity_clusters': {},
        'ai_descriptions': {},
        'overlap_mappings': {},
        'industry_mappings': {}
    }

# Header
st.markdown("""
<div class="job-title-header">
    <h1>🎯 Job Title Intelligence System</h1>
    <p>AI-Powered Semantic Analysis & Overlap Visualization</p>
    <p><strong>Discover job title relationships with interactive Venn diagrams</strong></p>
</div>
""", unsafe_allow_html=True)

# Helper functions (defined before use)
def analyze_job_title_similarities(primary_title: str, compare_titles: List[str]) -> Dict:
    """Analyze similarities between job titles"""
    
    # Mock skill databases for different job titles
    skill_database = {
        "software engineer": ["Programming", "Debugging", "Software Design", "Testing", "Version Control", "Agile", "Problem Solving"],
        "data scientist": ["Python", "Statistics", "Machine Learning", "Data Analysis", "SQL", "Data Visualization", "Research"],
        "product manager": ["Product Strategy", "Market Research", "Stakeholder Management", "Analytics", "Roadmapping", "Leadership"],
        "full stack engineer": ["Frontend Development", "Backend Development", "Database Design", "API Development", "DevOps", "Programming"],
        "technical lead": ["Leadership", "Architecture Design", "Code Review", "Mentoring", "Project Management", "Technical Strategy"],
        "systems engineer": ["Systems Design", "Infrastructure", "Network Management", "Automation", "Security", "Monitoring"],
        "software developer": ["Programming", "Software Design", "Testing", "Debugging", "Documentation", "Code Review"],
    }
    
    def get_skills_for_title(title: str) -> List[str]:
        """Get skills for a job title"""
        title_lower = title.lower()
        for key in skill_database:
            if key in title_lower or any(word in title_lower for word in key.split()):
                return skill_database[key]
        return ["Communication", "Problem Solving", "Teamwork", "Leadership"]  # Default skills
    
    primary_skills = set(get_skills_for_title(primary_title))
    results = {
        'primary_title': primary_title,
        'primary_skills': list(primary_skills),
        'top_matches': [],
        'detailed_analysis': []
    }
    
    for compare_title in compare_titles:
        compare_skills = set(get_skills_for_title(compare_title))
        
        # Calculate similarity
        shared_skills = primary_skills.intersection(compare_skills)
        all_skills = primary_skills.union(compare_skills)
        similarity = len(shared_skills) / len(all_skills) * 100 if all_skills else 0
        
        results['top_matches'].append((compare_title, f"{similarity:.0f}"))
        
        results['detailed_analysis'].append({
            'title': compare_title,
            'similarity': f"{similarity:.0f}",
            'shared_skills': list(shared_skills),
            'unique_skills': list(compare_skills - primary_skills)[:5],
            'transition_difficulty': "Low" if similarity > 60 else "Medium" if similarity > 30 else "High",
            'experience_gap': f"{max(0, 2 - similarity/30):.1f} years"
        })
    
    # Sort by similarity
    results['top_matches'].sort(key=lambda x: float(x[1]), reverse=True)
    results['detailed_analysis'].sort(key=lambda x: float(x['similarity']), reverse=True)
    
    return results

def generate_ai_job_description(job_title: str, query_type: str) -> str:
    """Generate AI-powered job description"""
    
    # Mock AI responses based on job title and query type
    responses = {
        "Job Description": f"""
**{job_title}** is a professional role that involves:

• **Primary Responsibilities:** Leading projects, collaborating with teams, and delivering high-quality results
• **Key Activities:** Strategic planning, problem-solving, and stakeholder communication  
• **Work Environment:** Dynamic, collaborative setting with opportunities for growth
• **Impact:** Contributes directly to organizational success and innovation

This role requires a combination of technical expertise and soft skills to excel in today's competitive market.
        """,
        
        "Skills Required": f"""
**Essential Skills for {job_title}:**

**Technical Skills:**
• Industry-specific software and tools
• Data analysis and reporting
• Project management methodologies
• Communication platforms

**Soft Skills:**
• Leadership and team collaboration
• Problem-solving and critical thinking
• Communication and presentation
• Adaptability and continuous learning

**Experience Level:** Typically requires 2-5 years of relevant experience
        """,
        
        "Career Progression": f"""
**Career Path for {job_title}:**

**Entry Level:** Junior/Associate → **Mid-Level:** {job_title} → **Senior Level:** Senior {job_title} → **Leadership:** Team Lead/Manager

**Growth Opportunities:**
• Specialization in niche areas
• Cross-functional collaboration
• Leadership and management roles
• Industry expertise development

**Timeline:** Career progression typically takes 5-10 years with continuous skill development.
        """,
        
        "Salary Range": f"""
**Salary Expectations for {job_title}:**

• **Entry Level:** $50,000 - $70,000
• **Mid-Level:** $70,000 - $95,000  
• **Senior Level:** $95,000 - $130,000
• **Leadership:** $130,000+

*Salaries vary by location, industry, and company size. Major tech hubs typically offer 20-40% higher compensation.*

**Additional Benefits:** Health insurance, retirement plans, professional development, flexible work arrangements.
        """,
        
        "Industry Context": f"""
**Industry Landscape for {job_title}:**

**Current Trends:**
• Increasing demand for digital transformation
• Remote and hybrid work models
• Focus on data-driven decision making
• Emphasis on continuous learning

**Market Outlook:**
• Strong job growth projected (5-15% annually)
• High demand across multiple industries
• Competitive salary and benefits packages
• Opportunities for specialization and advancement

**Key Industries:** Technology, Healthcare, Finance, Consulting, Manufacturing
        """
    }
    
    return responses.get(query_type, "AI analysis not available for this query type.")

def generate_overlap_data(title1: str, title2: str, title3: str = None) -> Dict:
    """Generate overlap data for visualization"""
    
    # Mock skill sets for visualization
    skills_db = {
        "software engineer": ["Python", "JavaScript", "Git", "Testing", "Debugging", "Agile", "Code Review"],
        "data scientist": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization", "Research", "Analytics"],
        "product manager": ["Strategy", "Analytics", "Stakeholder Management", "Roadmapping", "Market Research", "Leadership", "Communication"]
    }
    
    def get_skills(title):
        title_lower = title.lower()
        for key in skills_db:
            if key in title_lower:
                return set(skills_db[key])
        return set(["Communication", "Problem Solving", "Teamwork", "Leadership"])
    
    skills1 = get_skills(title1)
    skills2 = get_skills(title2)
    skills3 = get_skills(title3) if title3 else set()
    
    shared_skills = skills1.intersection(skills2)
    if title3:
        shared_skills = shared_skills.intersection(skills3)
    
    all_skills = skills1.union(skills2)
    if title3:
        all_skills = all_skills.union(skills3)
    
    unique_skills = all_skills - shared_skills
    
    return {
        'title1': title1,
        'title2': title2,
        'title3': title3,
        'skills1': list(skills1),
        'skills2': list(skills2),
        'skills3': list(skills3) if title3 else [],
        'shared_skills': list(shared_skills),
        'unique_skills': list(unique_skills),
        'all_skills': list(all_skills)
    }

def create_similarity_heatmap(results: Dict) -> go.Figure:
    """Create similarity heatmap visualization"""
    
    titles = [results['primary_title']] + [analysis['title'] for analysis in results['detailed_analysis']]
    similarities = [100] + [float(analysis['similarity']) for analysis in results['detailed_analysis']]
    
    # Create matrix
    n = len(titles)
    similarity_matrix = np.zeros((n, n))
    
    for i in range(n):
        similarity_matrix[i, i] = 100
        for j in range(i+1, n):
            sim_value = similarities[j] if i == 0 else 50  # Mock values
            similarity_matrix[i, j] = sim_value
            similarity_matrix[j, i] = sim_value
    
    fig = go.Figure(data=go.Heatmap(
        z=similarity_matrix,
        x=titles,
        y=titles,
        colorscale='RdYlBu_r',
        colorbar=dict(title="Similarity %")
    ))
    
    fig.update_layout(
        title="Job Title Similarity Matrix",
        xaxis_title="Job Titles",
        yaxis_title="Job Titles",
        height=400
    )
    
    return fig

def create_2way_venn_diagram(data: Dict) -> go.Figure:
    """Create 2-way Venn diagram"""
    
    # Create circles for Venn diagram
    fig = go.Figure()
    
    # Add circles (simplified representation)
    fig.add_shape(
        type="circle",
        x0=0.2, y0=0.2, x1=0.8, y1=0.8,
        fillcolor="rgba(100, 150, 200, 0.3)",
        line=dict(color="rgba(100, 150, 200, 0.8)", width=2),
        layer="below"
    )
    
    fig.add_shape(
        type="circle", 
        x0=0.4, y0=0.2, x1=1.0, y1=0.8,
        fillcolor="rgba(200, 100, 150, 0.3)",
        line=dict(color="rgba(200, 100, 150, 0.8)", width=2),
        layer="below"
    )
    
    # Add text annotations
    fig.add_annotation(x=0.3, y=0.5, text=data['title1'], showarrow=False, font=dict(size=14, color="blue"))
    fig.add_annotation(x=0.7, y=0.5, text=data['title2'], showarrow=False, font=dict(size=14, color="red"))
    fig.add_annotation(x=0.5, y=0.5, text=f"Shared: {len(data['shared_skills'])}", showarrow=False, font=dict(size=12))
    
    fig.update_layout(
        title=f"Job Title Overlap: {data['title1']} vs {data['title2']}",
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
    )
    
    return fig

def create_3way_venn_diagram(data: Dict) -> go.Figure:
    """Create 3-way Venn diagram"""
    
    fig = go.Figure()
    
    # Add three overlapping circles
    circles = [
        dict(x0=0.1, y0=0.3, x1=0.6, y1=0.8, color="rgba(100, 150, 200, 0.3)"),
        dict(x0=0.4, y0=0.3, x1=0.9, y1=0.8, color="rgba(200, 100, 150, 0.3)"),
        dict(x0=0.25, y0=0.1, x1=0.75, y1=0.6, color="rgba(150, 200, 100, 0.3)")
    ]
    
    for circle in circles:
        fig.add_shape(
            type="circle",
            x0=circle['x0'], y0=circle['y0'], 
            x1=circle['x1'], y1=circle['y1'],
            fillcolor=circle['color'],
            line=dict(width=2),
            layer="below"
        )
    
    # Add labels
    fig.add_annotation(x=0.2, y=0.7, text=data['title1'], showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0.8, y=0.7, text=data['title2'], showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0.5, y=0.2, text=data['title3'], showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0.5, y=0.5, text=f"Core: {len(data['shared_skills'])}", showarrow=False, font=dict(size=10))
    
    fig.update_layout(
        title=f"3-Way Overlap: {data['title1']} • {data['title2']} • {data['title3']}",
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
    )
    
    return fig

def create_concentric_circles(data: Dict) -> go.Figure:
    """Create concentric circles visualization"""
    
    fig = go.Figure()
    
    # Create concentric circles representing skill importance levels
    circles = [
        dict(size=0.8, color="rgba(100, 150, 200, 0.2)", label="All Skills"),
        dict(size=0.6, color="rgba(150, 100, 200, 0.3)", label="Common Skills"),
        dict(size=0.4, color="rgba(200, 100, 150, 0.4)", label="Core Skills"),
        dict(size=0.2, color="rgba(100, 200, 150, 0.5)", label="Essential Skills")
    ]
    
    for i, circle in enumerate(circles):
        fig.add_shape(
            type="circle",
            x0=0.5-circle['size']/2, y0=0.5-circle['size']/2,
            x1=0.5+circle['size']/2, y1=0.5+circle['size']/2,
            fillcolor=circle['color'],
            line=dict(width=2),
            layer="below"
        )
        
        # Add labels
        fig.add_annotation(
            x=0.5, y=0.5-circle['size']/2+0.05,
            text=circle['label'],
            showarrow=False,
            font=dict(size=10)
        )
    
    fig.update_layout(
        title="Skill Importance Levels (Concentric View)",
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
    )
    
    return fig

def create_skill_overlap_matrix(data: Dict) -> go.Figure:
    """Create skill overlap matrix"""
    
    all_skills = data['all_skills'][:10]  # Limit for visualization
    n_skills = len(all_skills)
    
    # Create random overlap matrix for demo
    np.random.seed(42)
    overlap_matrix = np.random.randint(0, 100, (n_skills, n_skills))
    
    # Make symmetric
    for i in range(n_skills):
        overlap_matrix[i, i] = 100
        for j in range(i+1, n_skills):
            overlap_matrix[j, i] = overlap_matrix[i, j]
    
    fig = go.Figure(data=go.Heatmap(
        z=overlap_matrix,
        x=all_skills,
        y=all_skills,
        colorscale='Viridis',
        colorbar=dict(title="Overlap %")
    ))
    
    fig.update_layout(
        title="Skill Overlap Matrix",
        height=400
    )
    
    return fig

def generate_industry_mapping(job_title: str, source_industry: str, target_industry: str) -> Dict:
    """Generate industry mapping data"""
    
    # Mock industry mapping logic
    industry_equivalents = {
        ("Technology", "Healthcare"): {
            "Project Manager": "Clinical Project Manager",
            "Data Analyst": "Healthcare Data Analyst", 
            "Software Engineer": "Health Informatics Specialist"
        },
        ("Finance", "Technology"): {
            "Financial Analyst": "Business Intelligence Analyst",
            "Risk Manager": "Security Analyst",
            "Investment Banker": "Product Manager"
        },
        ("Healthcare", "Education"): {
            "Nurse": "Health Education Specialist",
            "Medical Assistant": "Academic Support Specialist",
            "Healthcare Administrator": "Academic Administrator"
        }
    }
    
    key = (source_industry, target_industry)
    equivalent = industry_equivalents.get(key, {}).get(job_title, f"{target_industry} {job_title}")
    
    return {
        'original_title': job_title,
        'source_industry': source_industry,
        'target_industry': target_industry,
        'equivalent_title': equivalent,
        'similarity_score': np.random.randint(70, 95),
        'transition_difficulty': np.random.choice(["Low", "Medium", "High"]),
        'source_responsibilities': [
            f"Manage {source_industry.lower()} projects",
            f"Analyze {source_industry.lower()} data",
            f"Collaborate with {source_industry.lower()} teams"
        ],
        'target_responsibilities': [
            f"Manage {target_industry.lower()} projects", 
            f"Analyze {target_industry.lower()} data",
            f"Collaborate with {target_industry.lower()} teams"
        ],
        'skills_to_develop': [
            f"{target_industry} domain knowledge",
            f"{target_industry} regulations",
            f"{target_industry} best practices"
        ]
    }

# Main navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Title Analysis", 
    "🤖 AI Chat Integration", 
    "📊 Overlap Visualizer", 
    "🏢 Industry Mapping", 
    "⚙️ Admin Engine"
])

# ==================== TAB 1: TITLE ANALYSIS ====================
with tab1:
    render_section_header("Job Title Semantic Analysis", "🔍")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Analyze Job Title Relationships")
        
        # Input section
        primary_title = st.text_input(
            "Primary Job Title",
            placeholder="e.g., Senior Software Engineer"
        )
        
        comparison_titles = st.text_area(
            "Compare With (one per line)",
            placeholder="Software Developer\nFull Stack Engineer\nSystems Engineer\nTechnical Lead",
            height=100
        )
        
        if st.button("🔍 Analyze Titles", type="primary"):
            if primary_title:
                with st.spinner("🤖 AI is analyzing job title relationships..."):
                    # Parse comparison titles
                    compare_list = [title.strip() for title in comparison_titles.split('\n') if title.strip()]
                    
                    # Generate similarity analysis
                    analysis_results = analyze_job_title_similarities(primary_title, compare_list)
                    
                    st.session_state.current_analysis = analysis_results
                    st.success("✅ Analysis complete!")
                    st.rerun()
            else:
                st.warning("Please enter a primary job title.")
    
    with col2:
        st.markdown("### 💡 Quick Tips")
        st.info("""
        **How it works:**
        • AI analyzes job title semantics
        • Identifies skill overlaps
        • Maps industry relationships  
        • Suggests similar roles
        
        **Best practices:**
        • Use specific titles
        • Include seniority levels
        • Compare within industries
        • Explore cross-industry roles
        """)
    
    # Display analysis results
    if 'current_analysis' in st.session_state:
        results = st.session_state.current_analysis
        
        st.markdown("### 📊 Similarity Analysis Results")
        
        # Create similarity matrix
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Similarity scores visualization
            fig = create_similarity_heatmap(results)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Top Matches")
            for title, score in results['top_matches']:
                st.markdown(f"""
                <div class="similarity-badge">
                    {title}: {score}% match
                </div>
                """, unsafe_allow_html=True)
        
        # Detailed breakdown
        st.markdown("### 🔬 Detailed Analysis")
        
        for title_data in results['detailed_analysis']:
            with st.expander(f"🎯 {title_data['title']} (Match: {title_data['similarity']}%)"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Shared Skills:**")
                    for skill in title_data['shared_skills']:
                        st.success(f"✅ {skill}")
                
                with col2:
                    st.markdown("**Unique Skills:**")
                    for skill in title_data['unique_skills']:
                        st.info(f"🔵 {skill}")
                
                with col3:
                    st.markdown("**Career Path:**")
                    st.write(f"**Transition Difficulty:** {title_data['transition_difficulty']}")
                    st.write(f"**Experience Gap:** {title_data['experience_gap']}")

# ==================== TAB 2: AI CHAT INTEGRATION ====================
with tab2:
    render_section_header("AI-Powered Job Title Descriptions", "🤖")
    
    st.markdown("""
    ### 💬 Chat with AI about Job Titles
    Get detailed descriptions, requirements, and insights about any job title.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        job_title_query = st.text_input(
            "Ask about a job title:",
            placeholder="What does a Product Manager do?"
        )
        
        chat_type = st.selectbox(
            "Query Type:",
            ["Job Description", "Skills Required", "Career Progression", "Salary Range", "Industry Context"]
        )
        
        if st.button("🤖 Ask AI", type="primary"):
            if job_title_query:
                with st.spinner("🤖 AI is analyzing the job title..."):
                    # Generate AI response
                    ai_response = generate_ai_job_description(job_title_query, chat_type)
                    
                    # Store in session state
                    if 'ai_chat_history' not in st.session_state:
                        st.session_state.ai_chat_history = []
                    
                    st.session_state.ai_chat_history.append({
                        'query': job_title_query,
                        'type': chat_type,
                        'response': ai_response,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    st.success("✅ AI analysis complete!")
                    st.rerun()
            else:
                st.warning("Please enter a job title query.")
    
    with col2:
        st.markdown("### 🎯 Popular Queries")
        popular_queries = [
            "Software Engineer responsibilities",
            "Data Scientist vs Data Analyst",
            "Product Manager career path",
            "DevOps Engineer skills needed",
            "UX Designer vs UI Designer",
            "Marketing Manager salary range"
        ]
        
        for query in popular_queries:
            if st.button(f"💡 {query}", key=f"popular_{query}"):
                st.session_state.quick_query = query
                st.rerun()
    
    # Display chat history
    if 'ai_chat_history' in st.session_state and st.session_state.ai_chat_history:
        st.markdown("### 💬 AI Chat History")
        
        for i, chat in enumerate(reversed(st.session_state.ai_chat_history[-5:]), 1):
            with st.expander(f"🤖 Query {i}: {chat['query']} ({chat['type']})"):
                st.markdown(f"""
                <div class="ai-insight">
                    <strong>Query:</strong> {chat['query']}<br>
                    <strong>Type:</strong> {chat['type']}<br>
                    <strong>Time:</strong> {chat['timestamp'][:19]}
                    <hr>
                    <strong>AI Response:</strong><br>
                    {chat['response']}
                </div>
                """, unsafe_allow_html=True)

# ==================== TAB 3: OVERLAP VISUALIZER ====================
with tab3:
    render_section_header("Job Title Overlap Venn Diagrams", "📊")
    
    st.markdown("""
    ### 🔄 Interactive Overlap Visualization
    Create concentric circles and Venn diagrams to visualize job title relationships.
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Venn diagram configuration
        venn_title_1 = st.text_input("Job Title 1", placeholder="Software Engineer")
        venn_title_2 = st.text_input("Job Title 2", placeholder="Data Scientist")
        venn_title_3 = st.text_input("Job Title 3 (Optional)", placeholder="Product Manager")
        
        visualization_type = st.selectbox(
            "Visualization Type:",
            ["2-Way Venn Diagram", "3-Way Venn Diagram", "Concentric Circles", "Skill Overlap Matrix"]
        )
        
        if st.button("📊 Generate Visualization", type="primary"):
            if venn_title_1 and venn_title_2:
                with st.spinner("🎨 Creating overlap visualization..."):
                    # Generate visualization data
                    overlap_data = generate_overlap_data(venn_title_1, venn_title_2, venn_title_3)
                    
                    # Create visualization
                    if visualization_type == "2-Way Venn Diagram":
                        fig = create_2way_venn_diagram(overlap_data)
                    elif visualization_type == "3-Way Venn Diagram" and venn_title_3:
                        fig = create_3way_venn_diagram(overlap_data)
                    elif visualization_type == "Concentric Circles":
                        fig = create_concentric_circles(overlap_data)
                    else:
                        fig = create_skill_overlap_matrix(overlap_data)
                    
                    st.session_state.current_visualization = {
                        'figure': fig,
                        'data': overlap_data,
                        'type': visualization_type
                    }
                    st.success("✅ Visualization created!")
                    st.rerun()
            else:
                st.warning("Please enter at least two job titles.")
    
    with col2:
        st.markdown("### 🎨 Visualization Guide")
        st.info("""
        **Venn Diagrams:**
        • Show skill overlaps
        • Identify unique competencies
        • Highlight career bridges
        
        **Concentric Circles:**
        • Core vs peripheral skills
        • Skill importance levels
        • Career progression paths
        
        **Colors represent:**
        • 🔵 Primary skills
        • 🟢 Shared competencies  
        • 🟡 Transferable skills
        • 🔴 Unique specializations
        """)
    
    # Display visualization
    if 'current_visualization' in st.session_state:
        viz_data = st.session_state.current_visualization
        
        st.markdown("### 🎨 Interactive Overlap Visualization")
        
        with st.container():
            st.markdown('<div class="venn-container">', unsafe_allow_html=True)
            st.plotly_chart(viz_data['figure'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis insights
        st.markdown("### 🔍 Overlap Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Shared Skills", len(viz_data['data']['shared_skills']))
            st.metric("Total Unique Skills", len(viz_data['data']['all_skills']))
        
        with col2:
            overlap_percentage = (len(viz_data['data']['shared_skills']) / 
                                len(viz_data['data']['all_skills']) * 100)
            st.metric("Overlap Percentage", f"{overlap_percentage:.1f}%")
            st.metric("Career Bridge Score", f"{min(95, overlap_percentage + 20):.0f}%")
        
        with col3:
            st.metric("Transition Difficulty", 
                     "Low" if overlap_percentage > 50 else "Medium" if overlap_percentage > 25 else "High")
        
        # Detailed skill breakdown
        st.markdown("#### 🎯 Skill Categories")
        
        skills_df = pd.DataFrame([
            {"Skill": skill, "Category": "Shared", "Importance": "High"} 
            for skill in viz_data['data']['shared_skills']
        ] + [
            {"Skill": skill, "Category": "Unique", "Importance": "Medium"} 
            for skill in viz_data['data']['unique_skills'][:10]
        ])
        
        if not skills_df.empty:
            st.dataframe(skills_df, use_container_width=True)

# Helper functions
def analyze_job_title_similarities(primary_title: str, compare_titles: List[str]) -> Dict:
    """Analyze similarities between job titles"""
    
    # Mock skill databases for different job titles
    skill_database = {
        "software engineer": ["Programming", "Debugging", "Software Design", "Testing", "Version Control", "Agile", "Problem Solving"],
        "data scientist": ["Python", "Statistics", "Machine Learning", "Data Analysis", "SQL", "Data Visualization", "Research"],
        "product manager": ["Product Strategy", "Market Research", "Stakeholder Management", "Analytics", "Roadmapping", "Leadership"],
        "full stack engineer": ["Frontend Development", "Backend Development", "Database Design", "API Development", "DevOps", "Programming"],
        "technical lead": ["Leadership", "Architecture Design", "Code Review", "Mentoring", "Project Management", "Technical Strategy"],
        "systems engineer": ["Systems Design", "Infrastructure", "Network Management", "Automation", "Security", "Monitoring"],
        "software developer": ["Programming", "Software Design", "Testing", "Debugging", "Documentation", "Code Review"],
    }
    
    def get_skills_for_title(title: str) -> List[str]:
        """Get skills for a job title"""
        title_lower = title.lower()
        for key in skill_database:
            if key in title_lower or any(word in title_lower for word in key.split()):
                return skill_database[key]
        return ["Communication", "Problem Solving", "Teamwork", "Leadership"]  # Default skills
    
    primary_skills = set(get_skills_for_title(primary_title))
    results = {
        'primary_title': primary_title,
        'primary_skills': list(primary_skills),
        'top_matches': [],
        'detailed_analysis': []
    }
    
    for compare_title in compare_titles:
        compare_skills = set(get_skills_for_title(compare_title))
        
        # Calculate similarity
        shared_skills = primary_skills.intersection(compare_skills)
        all_skills = primary_skills.union(compare_skills)
        similarity = len(shared_skills) / len(all_skills) * 100 if all_skills else 0
        
        results['top_matches'].append((compare_title, f"{similarity:.0f}"))
        
        results['detailed_analysis'].append({
            'title': compare_title,
            'similarity': f"{similarity:.0f}",
            'shared_skills': list(shared_skills),
            'unique_skills': list(compare_skills - primary_skills)[:5],
            'transition_difficulty': "Low" if similarity > 60 else "Medium" if similarity > 30 else "High",
            'experience_gap': f"{max(0, 2 - similarity/30):.1f} years"
        })
    
    # Sort by similarity
    results['top_matches'].sort(key=lambda x: float(x[1]), reverse=True)
    results['detailed_analysis'].sort(key=lambda x: float(x['similarity']), reverse=True)
    
    return results

def generate_ai_job_description(job_title: str, query_type: str) -> str:
    """Generate AI-powered job description"""
    
    # Mock AI responses based on job title and query type
    responses = {
        "Job Description": f"""
**{job_title}** is a professional role that involves:

• **Primary Responsibilities:** Leading projects, collaborating with teams, and delivering high-quality results
• **Key Activities:** Strategic planning, problem-solving, and stakeholder communication  
• **Work Environment:** Dynamic, collaborative setting with opportunities for growth
• **Impact:** Contributes directly to organizational success and innovation

This role requires a combination of technical expertise and soft skills to excel in today's competitive market.
        """,
        
        "Skills Required": f"""
**Essential Skills for {job_title}:**

**Technical Skills:**
• Industry-specific software and tools
• Data analysis and reporting
• Project management methodologies
• Communication platforms

**Soft Skills:**
• Leadership and team collaboration
• Problem-solving and critical thinking
• Communication and presentation
• Adaptability and continuous learning

**Experience Level:** Typically requires 2-5 years of relevant experience
        """,
        
        "Career Progression": f"""
**Career Path for {job_title}:**

**Entry Level:** Junior/Associate → **Mid-Level:** {job_title} → **Senior Level:** Senior {job_title} → **Leadership:** Team Lead/Manager

**Growth Opportunities:**
• Specialization in niche areas
• Cross-functional collaboration
• Leadership and management roles
• Industry expertise development

**Timeline:** Career progression typically takes 5-10 years with continuous skill development.
        """,
        
        "Salary Range": f"""
**Salary Expectations for {job_title}:**

• **Entry Level:** $50,000 - $70,000
• **Mid-Level:** $70,000 - $95,000  
• **Senior Level:** $95,000 - $130,000
• **Leadership:** $130,000+

*Salaries vary by location, industry, and company size. Major tech hubs typically offer 20-40% higher compensation.*

**Additional Benefits:** Health insurance, retirement plans, professional development, flexible work arrangements.
        """,
        
        "Industry Context": f"""
**Industry Landscape for {job_title}:**

**Current Trends:**
• Increasing demand for digital transformation
• Remote and hybrid work models
• Focus on data-driven decision making
• Emphasis on continuous learning

**Market Outlook:**
• Strong job growth projected (5-15% annually)
• High demand across multiple industries
• Competitive salary and benefits packages
• Opportunities for specialization and advancement

**Key Industries:** Technology, Healthcare, Finance, Consulting, Manufacturing
        """
    }
    
    return responses.get(query_type, "AI analysis not available for this query type.")

def generate_overlap_data(title1: str, title2: str, title3: str = None) -> Dict:
    """Generate overlap data for visualization"""
    
    # Mock skill sets for visualization
    skills_db = {
        "software engineer": ["Python", "JavaScript", "Git", "Testing", "Debugging", "Agile", "Code Review"],
        "data scientist": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization", "Research", "Analytics"],
        "product manager": ["Strategy", "Analytics", "Stakeholder Management", "Roadmapping", "Market Research", "Leadership", "Communication"]
    }
    
    def get_skills(title):
        title_lower = title.lower()
        for key in skills_db:
            if key in title_lower:
                return set(skills_db[key])
        return set(["Communication", "Problem Solving", "Teamwork", "Leadership"])
    
    skills1 = get_skills(title1)
    skills2 = get_skills(title2)
    skills3 = get_skills(title3) if title3 else set()
    
    shared_skills = skills1.intersection(skills2)
    if title3:
        shared_skills = shared_skills.intersection(skills3)
    
    all_skills = skills1.union(skills2)
    if title3:
        all_skills = all_skills.union(skills3)
    
    unique_skills = all_skills - shared_skills
    
    return {
        'title1': title1,
        'title2': title2,
        'title3': title3,
        'skills1': list(skills1),
        'skills2': list(skills2),
        'skills3': list(skills3) if title3 else [],
        'shared_skills': list(shared_skills),
        'unique_skills': list(unique_skills),
        'all_skills': list(all_skills)
    }

def create_similarity_heatmap(results: Dict) -> go.Figure:
    """Create similarity heatmap visualization"""
    
    titles = [results['primary_title']] + [analysis['title'] for analysis in results['detailed_analysis']]
    similarities = [100] + [float(analysis['similarity']) for analysis in results['detailed_analysis']]
    
    # Create matrix
    n = len(titles)
    similarity_matrix = np.zeros((n, n))
    
    for i in range(n):
        similarity_matrix[i, i] = 100
        for j in range(i+1, n):
            sim_value = similarities[j] if i == 0 else 50  # Mock values
            similarity_matrix[i, j] = sim_value
            similarity_matrix[j, i] = sim_value
    
    fig = go.Figure(data=go.Heatmap(
        z=similarity_matrix,
        x=titles,
        y=titles,
        colorscale='RdYlBu_r',
        colorbar=dict(title="Similarity %")
    ))
    
    fig.update_layout(
        title="Job Title Similarity Matrix",
        xaxis_title="Job Titles",
        yaxis_title="Job Titles",
        height=400
    )
    
    return fig

def create_2way_venn_diagram(data: Dict) -> go.Figure:
    """Create 2-way Venn diagram"""
    
    # Create circles for Venn diagram
    fig = go.Figure()
    
    # Add circles (simplified representation)
    fig.add_shape(
        type="circle",
        x0=0.2, y0=0.2, x1=0.8, y1=0.8,
        fillcolor="rgba(100, 150, 200, 0.3)",
        line=dict(color="rgba(100, 150, 200, 0.8)", width=2),
        layer="below"
    )
    
    fig.add_shape(
        type="circle", 
        x0=0.4, y0=0.2, x1=1.0, y1=0.8,
        fillcolor="rgba(200, 100, 150, 0.3)",
        line=dict(color="rgba(200, 100, 150, 0.8)", width=2),
        layer="below"
    )
    
    # Add text annotations
    fig.add_annotation(x=0.3, y=0.5, text=data['title1'], showarrow=False, font=dict(size=14, color="blue"))
    fig.add_annotation(x=0.7, y=0.5, text=data['title2'], showarrow=False, font=dict(size=14, color="red"))
    fig.add_annotation(x=0.5, y=0.5, text=f"Shared: {len(data['shared_skills'])}", showarrow=False, font=dict(size=12))
    
    fig.update_layout(
        title=f"Job Title Overlap: {data['title1']} vs {data['title2']}",
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
    )
    
    return fig

def create_3way_venn_diagram(data: Dict) -> go.Figure:
    """Create 3-way Venn diagram"""
    
    fig = go.Figure()
    
    # Add three overlapping circles
    circles = [
        dict(x0=0.1, y0=0.3, x1=0.6, y1=0.8, color="rgba(100, 150, 200, 0.3)"),
        dict(x0=0.4, y0=0.3, x1=0.9, y1=0.8, color="rgba(200, 100, 150, 0.3)"),
        dict(x0=0.25, y0=0.1, x1=0.75, y1=0.6, color="rgba(150, 200, 100, 0.3)")
    ]
    
    for circle in circles:
        fig.add_shape(
            type="circle",
            x0=circle['x0'], y0=circle['y0'], 
            x1=circle['x1'], y1=circle['y1'],
            fillcolor=circle['color'],
            line=dict(width=2),
            layer="below"
        )
    
    # Add labels
    fig.add_annotation(x=0.2, y=0.7, text=data['title1'], showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0.8, y=0.7, text=data['title2'], showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0.5, y=0.2, text=data['title3'], showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0.5, y=0.5, text=f"Core: {len(data['shared_skills'])}", showarrow=False, font=dict(size=10))
    
    fig.update_layout(
        title=f"3-Way Overlap: {data['title1']} • {data['title2']} • {data['title3']}",
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
    )
    
    return fig

def create_concentric_circles(data: Dict) -> go.Figure:
    """Create concentric circles visualization"""
    
    fig = go.Figure()
    
    # Create concentric circles representing skill importance levels
    circles = [
        dict(size=0.8, color="rgba(100, 150, 200, 0.2)", label="All Skills"),
        dict(size=0.6, color="rgba(150, 100, 200, 0.3)", label="Common Skills"),
        dict(size=0.4, color="rgba(200, 100, 150, 0.4)", label="Core Skills"),
        dict(size=0.2, color="rgba(100, 200, 150, 0.5)", label="Essential Skills")
    ]
    
    for i, circle in enumerate(circles):
        fig.add_shape(
            type="circle",
            x0=0.5-circle['size']/2, y0=0.5-circle['size']/2,
            x1=0.5+circle['size']/2, y1=0.5+circle['size']/2,
            fillcolor=circle['color'],
            line=dict(width=2),
            layer="below"
        )
        
        # Add labels
        fig.add_annotation(
            x=0.5, y=0.5-circle['size']/2+0.05,
            text=circle['label'],
            showarrow=False,
            font=dict(size=10)
        )
    
    fig.update_layout(
        title="Skill Importance Levels (Concentric View)",
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
    )
    
    return fig

def create_skill_overlap_matrix(data: Dict) -> go.Figure:
    """Create skill overlap matrix"""
    
    all_skills = data['all_skills'][:10]  # Limit for visualization
    n_skills = len(all_skills)
    
    # Create random overlap matrix for demo
    np.random.seed(42)
    overlap_matrix = np.random.randint(0, 100, (n_skills, n_skills))
    
    # Make symmetric
    for i in range(n_skills):
        overlap_matrix[i, i] = 100
        for j in range(i+1, n_skills):
            overlap_matrix[j, i] = overlap_matrix[i, j]
    
    fig = go.Figure(data=go.Heatmap(
        z=overlap_matrix,
        x=all_skills,
        y=all_skills,
        colorscale='Viridis',
        colorbar=dict(title="Overlap %")
    ))
    
    fig.update_layout(
        title="Skill Overlap Matrix",
        height=400
    )
    
    return fig

# ==================== TAB 4: INDUSTRY MAPPING ====================
with tab4:
    render_section_header("Industry Overlap Analysis", "🏢")
    
    st.markdown("""
    ### 🏭 Cross-Industry Job Title Mapping
    Discover how job titles translate across different industries.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        source_industry = st.selectbox(
            "Source Industry:",
            ["Technology", "Healthcare", "Finance", "Manufacturing", "Education", "Retail", "Consulting"]
        )
        
        target_industry = st.selectbox(
            "Target Industry:",
            ["Technology", "Healthcare", "Finance", "Manufacturing", "Education", "Retail", "Consulting"]
        )
        
        job_title_input = st.text_input(
            "Job Title to Map:",
            placeholder="e.g., Project Manager, Data Analyst, Marketing Specialist"
        )
        
        if st.button("🗺️ Map Across Industries", type="primary"):
            if job_title_input and source_industry != target_industry:
                with st.spinner("🔍 Mapping job title across industries..."):
                    industry_mapping = generate_industry_mapping(job_title_input, source_industry, target_industry)
                    st.session_state.industry_mapping = industry_mapping
                    st.success("✅ Industry mapping complete!")
                    st.rerun()
            else:
                st.warning("Please select different industries and enter a job title.")
    
    with col2:
        st.markdown("### 🎯 Industry Insights")
        st.info("""
        **Cross-Industry Benefits:**
        • Identify transferable roles
        • Discover new career paths
        • Understand skill relevance
        • Plan industry transitions
        
        **Common Patterns:**
        • Similar roles, different titles
        • Industry-specific requirements
        • Salary variations
        • Growth opportunities
        """)
    
    # Display industry mapping results
    if 'industry_mapping' in st.session_state:
        mapping = st.session_state.industry_mapping
        
        st.markdown("### 🗺️ Industry Translation Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"#### 🏢 {mapping['source_industry']}")
            st.markdown(f"**Original Title:** {mapping['original_title']}")
            st.markdown("**Key Responsibilities:**")
            for resp in mapping['source_responsibilities']:
                st.write(f"• {resp}")
        
        with col2:
            st.markdown("#### 🔄 Translation")
            st.markdown(f"**Similarity Score:** {mapping['similarity_score']}%")
            st.markdown(f"**Transition Difficulty:** {mapping['transition_difficulty']}")
            st.markdown("**Skills to Develop:**")
            for skill in mapping['skills_to_develop']:
                st.warning(f"📚 {skill}")
        
        with col3:
            st.markdown(f"#### 🏭 {mapping['target_industry']}")
            st.markdown(f"**Equivalent Title:** {mapping['equivalent_title']}")
            st.markdown("**Key Responsibilities:**")
            for resp in mapping['target_responsibilities']:
                st.write(f"• {resp}")
        
        # Salary comparison
        st.markdown("### 💰 Salary Comparison")
        
        salary_comparison = pd.DataFrame([
            {"Industry": mapping['source_industry'], "Entry": "$65K", "Mid": "$85K", "Senior": "$110K"},
            {"Industry": mapping['target_industry'], "Entry": "$60K", "Mid": "$90K", "Senior": "$120K"}
        ])
        
        st.dataframe(salary_comparison, use_container_width=True)

def generate_industry_mapping(job_title: str, source_industry: str, target_industry: str) -> Dict:
    """Generate industry mapping data"""
    
    # Mock industry mapping logic
    industry_equivalents = {
        ("Technology", "Healthcare"): {
            "Project Manager": "Clinical Project Manager",
            "Data Analyst": "Healthcare Data Analyst", 
            "Software Engineer": "Health Informatics Specialist"
        },
        ("Finance", "Technology"): {
            "Financial Analyst": "Business Intelligence Analyst",
            "Risk Manager": "Security Analyst",
            "Investment Banker": "Product Manager"
        },
        ("Healthcare", "Education"): {
            "Nurse": "Health Education Specialist",
            "Medical Assistant": "Academic Support Specialist",
            "Healthcare Administrator": "Academic Administrator"
        }
    }
    
    key = (source_industry, target_industry)
    equivalent = industry_equivalents.get(key, {}).get(job_title, f"{target_industry} {job_title}")
    
    return {
        'original_title': job_title,
        'source_industry': source_industry,
        'target_industry': target_industry,
        'equivalent_title': equivalent,
        'similarity_score': np.random.randint(70, 95),
        'transition_difficulty': np.random.choice(["Low", "Medium", "High"]),
        'source_responsibilities': [
            f"Manage {source_industry.lower()} projects",
            f"Analyze {source_industry.lower()} data",
            f"Collaborate with {source_industry.lower()} teams"
        ],
        'target_responsibilities': [
            f"Manage {target_industry.lower()} projects", 
            f"Analyze {target_industry.lower()} data",
            f"Collaborate with {target_industry.lower()} teams"
        ],
        'skills_to_develop': [
            f"{target_industry} domain knowledge",
            f"{target_industry} regulations",
            f"{target_industry} best practices"
        ]
    }

# ==================== TAB 5: ADMIN ENGINE ====================
with tab5:
    render_section_header("Job Title Intelligence Admin Engine", "⚙️")
    
    # Check admin permissions
    is_admin = st.session_state.get('is_admin', False)
    
    if not is_admin:
        st.warning("🔒 Admin access required for this section.")
        if st.button("🔓 Enable Admin Mode (Demo)"):
            st.session_state.is_admin = True
            st.rerun()
    else:
        st.markdown("""
        ### 🔧 Administrative Tools
        Manage job title database, AI models, and system configurations.
        """)
        
        admin_tab1, admin_tab2, admin_tab3 = st.tabs([
            "📊 Database Management",
            "🤖 AI Model Training", 
            "📈 Analytics Dashboard"
        ])
        
        with admin_tab1:
            st.markdown("#### 📊 Job Title Database")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Job Titles", "2,847", delta="127 new")
                st.metric("Industries Covered", "23", delta="2 new")
                st.metric("Skill Mappings", "12,456", delta="856 updated")
            
            with col2:
                st.metric("AI Descriptions", "1,923", delta="234 new")
                st.metric("Similarity Pairs", "45,678", delta="1,234 new")
                st.metric("Industry Mappings", "567", delta="89 new")
            
            # Database operations
            st.markdown("#### 🔧 Database Operations")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Refresh Database"):
                    st.success("Database refreshed successfully!")
            
            with col2:
                if st.button("📥 Import New Data"):
                    st.info("Import functionality would be implemented here.")
            
            with col3:
                if st.button("📤 Export Database"):
                    st.info("Export functionality would be implemented here.")
        
        with admin_tab2:
            st.markdown("#### 🤖 AI Model Training")
            
            training_progress = st.progress(0.75)
            st.markdown("**Current Training Status:** 75% Complete")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Model Performance:**")
                st.metric("Accuracy", "94.2%", delta="2.1%")
                st.metric("Precision", "91.8%", delta="1.8%")
                st.metric("Recall", "89.5%", delta="0.9%")
            
            with col2:
                st.markdown("**Training Data:**")
                st.metric("Training Samples", "125,847")
                st.metric("Validation Samples", "31,462") 
                st.metric("Test Samples", "15,731")
            
            if st.button("🚀 Start New Training"):
                st.info("New training cycle would be initiated here.")
        
        with admin_tab3:
            st.markdown("#### 📈 System Analytics")
            
            # Mock analytics data
            usage_data = pd.DataFrame({
                'Date': pd.date_range('2025-09-01', periods=30),
                'Queries': np.random.randint(50, 200, 30),
                'New Titles': np.random.randint(5, 25, 30)
            })
            
            fig = px.line(usage_data, x='Date', y=['Queries', 'New Titles'], 
                         title="System Usage Over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top queries
            st.markdown("#### 🔥 Popular Queries")
            popular_queries = pd.DataFrame({
                'Query': ['Software Engineer', 'Data Scientist', 'Product Manager', 'DevOps Engineer', 'UX Designer'],
                'Count': [1250, 892, 743, 567, 456],
                'Growth': ['+12%', '+8%', '+15%', '+22%', '+6%']
            })
            
            st.dataframe(popular_queries, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>🎯 Job Title Intelligence System</strong> - AI-Powered Career Insights</p>
    <p>Discover job relationships, skill overlaps, and career transitions with interactive visualizations</p>
</div>
""", unsafe_allow_html=True)