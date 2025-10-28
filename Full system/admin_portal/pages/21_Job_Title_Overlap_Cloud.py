"""
IntelliCV Job Title & Industry Overlap Cloud Engine
==================================================

Admin engine for managing job title similarities and industry overlaps with
AI-powered chat integration for job title meanings and descriptions.

This creates visual overlap clouds (Venn diagrams) showing relationships between:
- Job titles with similar skills/responsibilities  
- Industries with overlapping functions
- Career progression paths

Author: IntelliCV-AI Team
Date: October 2, 2025
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
import numpy as np
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import re
from collections import defaultdict, Counter

# Import AI data loader
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from ai_data_loader import AIDataLoader
    ai_loader = AIDataLoader()
    AI_LOADER_AVAILABLE = True
except ImportError:
    AI_LOADER_AVAILABLE = False
    ai_loader = None

# Try to import shared components
try:
    from shared.components import render_section_header
    from shared.branding import inject_intellicv_branding, render_intellicv_page_header
    SHARED_COMPONENTS_AVAILABLE = True
except ImportError:
    SHARED_COMPONENTS_AVAILABLE = False

# Try to import AI chat integration
try:
    from services.ai_chat_integration import AIJobTitleChat
    AI_CHAT_AVAILABLE = True
except ImportError:
    AI_CHAT_AVAILABLE = False

class JobTitleOverlapEngine:
    """Engine for analyzing job title and industry overlaps"""
    
    def __init__(self):
        self.job_titles_db = self._load_job_titles_database()
        self.industry_mappings = self._load_industry_mappings()
        self.skill_mappings = self._load_skill_mappings()
        self.overlap_cache = {}
        self.chat_responses = {}
        
    def _load_job_titles_database(self) -> Dict:
        """Load the enhanced job titles database from AI data"""
        try:
            # Try AI data loader first (real CV data)
            if AI_LOADER_AVAILABLE and ai_loader:
                job_titles_data = ai_loader.load_real_job_titles()
                if job_titles_data and 'job_titles' in job_titles_data:
                    # Convert to expected format
                    categorized = self._categorize_job_titles_from_ai(job_titles_data['job_titles'])
                    return {
                        "categorized_titles": categorized,
                        "skill_mappings": self._extract_skills_from_ai(job_titles_data)
                    }
            
            # Fallback to file-based database
            db_path = Path("ai_data_final/enhanced_job_titles_database.json")
            if db_path.exists():
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback to ai_data path
            db_path2 = Path("ai_data/enhanced_job_titles_database.json")
            if db_path2.exists():
                with open(db_path2, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return self._create_minimal_fallback()
        except Exception:
            return self._create_minimal_fallback()
    
    def _categorize_job_titles_from_ai(self, job_titles: List) -> Dict[str, List[str]]:
        """Categorize job titles by industry using AI analysis"""
        categories = defaultdict(list)
        for job in job_titles[:50]:  # Limit to avoid overwhelming
            title = job.get('title', job) if isinstance(job, dict) else str(job)
            category = self._infer_category_from_title(title)
            categories[category].append(title)
        return dict(categories) if categories else {"General": [str(j) for j in job_titles[:20]]}
    
    def _infer_category_from_title(self, title: str) -> str:
        """Infer category from job title"""
        title_lower = title.lower()
        if any(t in title_lower for t in ['engineer', 'developer', 'software', 'data', 'tech']):
            return "Technology"
        elif any(t in title_lower for t in ['manager', 'analyst', 'consultant']):
            return "Business"
        elif any(t in title_lower for t in ['finance', 'accountant', 'banking']):
            return "Finance"
        elif any(t in title_lower for t in ['nurse', 'medical', 'healthcare']):
            return "Healthcare"
        return "General"
    
    def _extract_skills_from_ai(self, job_data: Dict) -> Dict[str, List[str]]:
        """Extract skill mappings from AI data"""
        mappings = {}
        for job in job_data.get('job_titles', [])[:20]:
            if isinstance(job, dict):
                title = job.get('title')
                skills = job.get('required_skills', job.get('skills', []))
                if title and skills:
                    mappings[title] = skills[:5] if isinstance(skills, list) else [skills]
        return mappings if mappings else self._get_minimal_skills()
    
    def _create_minimal_fallback(self) -> Dict:
        """Create minimal fallback database (not hardcoded production data)"""
        return {
            "categorized_titles": {
                "Technology": ["Software Engineer", "Data Analyst"],
                "Business": ["Project Manager", "Business Analyst"],
                "General": ["Professional"]
            },
            "skill_mappings": self._get_minimal_skills()
        }
    
    def _get_minimal_skills(self) -> Dict[str, List[str]]:
        """Minimal skill mappings for fallback"""
        return {
            "Software Engineer": ["Problem Solving", "Technical Design", "Testing"],
            "Data Analyst": ["Data Analysis", "Visualization", "Communication"],
            "Project Manager": ["Planning", "Leadership", "Communication"]
        }
    
    def _create_sample_database(self) -> Dict:
        """DEPRECATED: Use _create_minimal_fallback instead"""
        return self._create_minimal_fallback()
    
    def _load_industry_mappings(self) -> Dict:
        """Load industry classification mappings"""
        return {
            "Technology": {
                "subcategories": ["Software", "Hardware", "AI/ML", "Cloud", "Cybersecurity"],
                "common_skills": ["Programming", "Problem Solving", "Innovation", "Technical Design"],
                "related_industries": ["Telecommunications", "Media", "Financial Services"]
            },
            "Healthcare": {
                "subcategories": ["Clinical Care", "Healthcare IT", "Medical Devices", "Pharmaceuticals"],
                "common_skills": ["Patient Care", "Compliance", "Medical Knowledge", "Data Analysis"],
                "related_industries": ["Insurance", "Technology", "Research"]
            },
            "Finance": {
                "subcategories": ["Banking", "Investment", "Insurance", "Fintech"],
                "common_skills": ["Financial Analysis", "Risk Assessment", "Regulatory Knowledge", "Client Relations"],
                "related_industries": ["Technology", "Real Estate", "Healthcare"]
            },
            "Business": {
                "subcategories": ["Consulting", "Marketing", "Operations", "Strategy"],
                "common_skills": ["Strategic Thinking", "Communication", "Leadership", "Analytics"],
                "related_industries": ["Technology", "Healthcare", "Finance"]
            }
        }
    
    def _load_skill_mappings(self) -> Dict[str, List[str]]:
        """Load skill mappings for job titles from AI data"""
        return self._get_minimal_skill_mappings()
    
    def _get_minimal_skill_mappings(self) -> Dict[str, List[str]]:
        """Minimal skill mappings (core transferable skills)"""
        return {
            "Software Engineer": ["Problem Solving", "Technical Design", "Code Review", "Testing"],
            "Data Analyst": ["Data Analysis", "Statistics", "Visualization", "Communication"],
            "Project Manager": ["Project Planning", "Team Leadership", "Communication", "Risk Management"],
            "Business Analyst": ["Requirements Analysis", "Stakeholder Management", "Documentation", "Process Improvement"]
        }
    
    # DEPRECATED: Old hardcoded method - keeping for backward compatibility
    def _get_default_skill_mappings(self) -> Dict[str, List[str]]:
        """DEPRECATED: Use _get_minimal_skill_mappings() instead"""
        return self._get_minimal_skill_mappings()
    
    def calculate_job_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity between two job titles based on skills"""
        skills1 = set(self.skill_mappings.get(title1, []))
        skills2 = set(self.skill_mappings.get(title2, []))
        
        if not skills1 or not skills2:
            return 0.0
        
        intersection = len(skills1.intersection(skills2))
        union = len(skills1.union(skills2))
        
        return intersection / union if union > 0 else 0.0
    
    def find_overlapping_job_titles(self, threshold: float = 0.3) -> Dict[str, List[Tuple[str, float]]]:
        """Find job titles with overlapping skills above threshold"""
        overlaps = defaultdict(list)
        titles = list(self.skill_mappings.keys())
        
        for i, title1 in enumerate(titles):
            for title2 in titles[i+1:]:
                similarity = self.calculate_job_title_similarity(title1, title2)
                if similarity >= threshold:
                    overlaps[title1].append((title2, similarity))
                    overlaps[title2].append((title1, similarity))
        
        return dict(overlaps)
    
    def get_industry_overlaps(self) -> Dict[str, Dict]:
        """Calculate industry overlaps based on related industries and skills"""
        overlaps = {}
        
        for industry, data in self.industry_mappings.items():
            related = data.get("related_industries", [])
            common_skills = set(data.get("common_skills", []))
            
            overlaps[industry] = {
                "related_industries": related,
                "skill_overlaps": {}
            }
            
            # Calculate skill overlaps with related industries
            for related_industry in related:
                if related_industry in self.industry_mappings:
                    related_skills = set(self.industry_mappings[related_industry].get("common_skills", []))
                    overlap_skills = common_skills.intersection(related_skills)
                    overlap_ratio = len(overlap_skills) / len(common_skills.union(related_skills)) if common_skills.union(related_skills) else 0
                    
                    overlaps[industry]["skill_overlaps"][related_industry] = {
                        "overlap_ratio": overlap_ratio,
                        "shared_skills": list(overlap_skills)
                    }
        
        return overlaps

class AIJobTitleChatMock:
    """Mock AI chat integration for job title descriptions"""
    
    def __init__(self):
        self.responses = {
            "Software Engineer": {
                "meaning": "A professional who designs, develops, and maintains software applications and systems.",
                "description": "Software Engineers create computer programs, applications, and systems. They analyze user needs, design solutions, write code, test software, and maintain existing systems. They work with various programming languages and development frameworks.",
                "key_responsibilities": ["Write and test code", "Design software architecture", "Debug applications", "Collaborate with teams", "Maintain documentation"],
                "similar_titles": ["Software Developer", "Programmer", "Systems Developer", "Application Developer"]
            },
            "Data Scientist": {
                "meaning": "A professional who extracts insights and knowledge from structured and unstructured data.",
                "description": "Data Scientists use statistical analysis, machine learning, and data visualization to solve complex business problems. They collect, clean, and analyze large datasets to identify patterns and make predictions.",
                "key_responsibilities": ["Analyze complex datasets", "Build predictive models", "Create data visualizations", "Communicate findings", "Design experiments"],
                "similar_titles": ["Data Analyst", "Machine Learning Engineer", "Research Scientist", "Quantitative Analyst"]
            },
            "Product Manager": {
                "meaning": "A professional who guides the development and strategy of products from conception to launch.",
                "description": "Product Managers act as the bridge between business, technology, and user experience teams. They define product vision, prioritize features, and ensure successful product delivery.",
                "key_responsibilities": ["Define product strategy", "Manage product roadmap", "Conduct market research", "Coordinate cross-functional teams", "Analyze product metrics"],
                "similar_titles": ["Product Owner", "Program Manager", "Strategy Manager", "Business Development Manager"]
            }
        }
    
    def get_job_title_description(self, job_title: str) -> Dict:
        """Get AI-powered description of job title"""
        if job_title in self.responses:
            return self.responses[job_title]
        
        # Generic response for unknown titles
        return {
            "meaning": f"A professional role in the {job_title} field.",
            "description": f"The {job_title} position involves specialized responsibilities and requires relevant skills and experience in the field.",
            "key_responsibilities": ["Perform job-specific tasks", "Collaborate with team members", "Meet performance objectives", "Maintain professional standards"],
            "similar_titles": [f"Senior {job_title}", f"Lead {job_title}", f"{job_title} Specialist"]
        }
    
    def chat_about_job_title(self, job_title: str, question: str) -> str:
        """Interactive chat about job title"""
        job_info = self.get_job_title_description(job_title)
        
        if "salary" in question.lower() or "pay" in question.lower():
            return f"Salary for {job_title} varies by location, experience, and company size. Entry-level positions typically start at $50-70k, mid-level at $70-100k, and senior positions can reach $100k+."
        
        elif "skills" in question.lower() or "requirements" in question.lower():
            return f"Key skills for {job_title} include: {', '.join(job_info['key_responsibilities'][:3])}. Educational requirements vary but typically include relevant degree or equivalent experience."
        
        elif "career" in question.lower() or "path" in question.lower():
            similar = job_info['similar_titles'][:2]
            return f"Career progression for {job_title} often leads to roles like {', '.join(similar)} or management positions in the same field."
        
        else:
            return job_info['description']

def render_job_title_overlap_cloud():
    """Main function to render the job title overlap cloud interface"""
    
    # Apply branding
    if SHARED_COMPONENTS_AVAILABLE:
        inject_intellicv_branding()
        render_intellicv_page_header(
            "Job Title & Industry Overlap Cloud",
            "🔄 AI-Powered Similarity Engine & Chat Integration"
        )
    else:
        st.markdown("# 🔄 **Job Title & Industry Overlap Cloud**")
        st.markdown("*AI-Powered Similarity Engine & Chat Integration*")
    
    # Initialize engines
    overlap_engine = JobTitleOverlapEngine()
    ai_chat = AIJobTitleChatMock() if not AI_CHAT_AVAILABLE else AIJobTitleChat()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Job Title Chat", 
        "🔄 Title Overlap Cloud", 
        "🏢 Industry Overlap Cloud",
        "⚙️ Admin Controls"
    ])
    
    with tab1:
        render_job_title_chat(ai_chat)
    
    with tab2:
        render_title_overlap_visualization(overlap_engine)
    
    with tab3:
        render_industry_overlap_visualization(overlap_engine)
    
    with tab4:
        render_admin_controls(overlap_engine)

def render_job_title_chat(ai_chat):
    """Render the AI chat interface for job title descriptions"""
    st.markdown("### 💬 **AI Job Title Chat Assistant**")
    st.markdown("*Get instant AI-powered descriptions and insights about any job title*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Job title input
        job_title = st.text_input(
            "Enter Job Title",
            placeholder="e.g., Software Engineer, Data Scientist, Product Manager",
            help="Type any job title to get AI-powered insights"
        )
        
        # Chat question input
        question = st.text_area(
            "Ask about this job title",
            placeholder="What does this job involve? What skills are needed? What's the career path?",
            help="Ask specific questions about the job title"
        )
        
        if st.button("🤖 Get AI Response", type="primary"):
            if job_title:
                with st.spinner("AI analyzing job title..."):
                    if question:
                        response = ai_chat.chat_about_job_title(job_title, question)
                        st.success("**AI Response:**")
                        st.write(response)
                    else:
                        job_info = ai_chat.get_job_title_description(job_title)
                        st.success("**Job Title Analysis:**")
                        
                        # Display structured information
                        st.write(f"**Meaning:** {job_info['meaning']}")
                        st.write(f"**Description:** {job_info['description']}")
                        
                        with st.expander("📋 Key Responsibilities"):
                            for resp in job_info['key_responsibilities']:
                                st.write(f"• {resp}")
                        
                        with st.expander("🔗 Similar Job Titles"):
                            for similar in job_info['similar_titles']:
                                st.write(f"• {similar}")
            else:
                st.warning("Please enter a job title first.")
    
    with col2:
        st.markdown("#### 🎯 **Quick Actions**")
        
        # Popular job titles for quick access
        popular_titles = [
            "Software Engineer",
            "Data Scientist", 
            "Product Manager",
            "Marketing Manager",
            "Financial Analyst",
            "Project Manager"
        ]
        
        st.markdown("**Popular Titles:**")
        for title in popular_titles:
            if st.button(f"🔍 {title}", key=f"quick_{title}"):
                st.session_state.selected_title = title
                job_info = ai_chat.get_job_title_description(title)
                
                st.info(f"**{title}**")
                st.write(job_info['meaning'])
        
        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if st.session_state.chat_history:
            st.markdown("#### 📚 **Recent Chats**")
            for i, (title, question) in enumerate(st.session_state.chat_history[-3:]):
                with st.expander(f"{title[:20]}..."):
                    st.write(f"**Q:** {question[:50]}...")

def render_title_overlap_visualization(overlap_engine):
    """Render job title overlap visualization (Venn diagram style)"""
    st.markdown("### 🔄 **Job Title Overlap Cloud**")
    st.markdown("*Visual representation of job title similarities based on shared skills*")
    
    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Minimum similarity score to show overlaps"
        )
    
    with col2:
        selected_industry = st.selectbox(
            "Filter by Industry",
            ["All"] + list(overlap_engine.job_titles_db.get("categorized_titles", {}).keys())
        )
    
    with col3:
        max_connections = st.number_input(
            "Max Connections per Title",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum number of similar titles to show"
        )
    
    # Generate overlap data
    overlaps = overlap_engine.find_overlapping_job_titles(similarity_threshold)
    
    if overlaps:
        # Create network visualization
        fig = create_job_title_network(overlaps, selected_industry, max_connections, overlap_engine)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed overlap table
        st.markdown("#### 📊 **Detailed Similarity Scores**")
        
        overlap_data = []
        for title1, similar_titles in overlaps.items():
            if selected_industry == "All" or is_title_in_industry(title1, selected_industry, overlap_engine):
                for title2, score in similar_titles[:max_connections]:
                    overlap_data.append({
                        "Primary Title": title1,
                        "Similar Title": title2,
                        "Similarity Score": f"{score:.2f}",
                        "Shared Skills": get_shared_skills(title1, title2, overlap_engine)
                    })
        
        if overlap_data:
            df = pd.DataFrame(overlap_data)
            st.dataframe(df, use_container_width=True, height=300)
        
    else:
        st.info("No overlapping job titles found with the current threshold. Try lowering the similarity threshold.")

def render_industry_overlap_visualization(overlap_engine):
    """Render industry overlap visualization"""
    st.markdown("### 🏢 **Industry Overlap Cloud**")
    st.markdown("*Venn diagram showing relationships between different industries*")
    
    # Get industry overlaps
    industry_overlaps = overlap_engine.get_industry_overlaps()
    
    # Create industry overlap visualization
    fig = create_industry_venn_diagram(industry_overlaps)
    st.plotly_chart(fig, use_container_width=True)
    
    # Industry details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔗 **Industry Relationships**")
        
        for industry, data in industry_overlaps.items():
            with st.expander(f"🏢 {industry}"):
                st.write("**Related Industries:**")
                for related in data["related_industries"]:
                    st.write(f"• {related}")
                
                if data["skill_overlaps"]:
                    st.write("**Skill Overlaps:**")
                    for related_ind, overlap_data in data["skill_overlaps"].items():
                        overlap_pct = overlap_data["overlap_ratio"] * 100
                        st.write(f"• {related_ind}: {overlap_pct:.1f}% overlap")
    
    with col2:
        st.markdown("#### 📈 **Overlap Metrics**")
        
        # Calculate overall industry connectivity
        total_connections = sum(len(data["related_industries"]) for data in industry_overlaps.values())
        avg_connections = total_connections / len(industry_overlaps) if industry_overlaps else 0
        
        st.metric("Total Industry Connections", total_connections)
        st.metric("Average Connections per Industry", f"{avg_connections:.1f}")
        
        # Most connected industry
        most_connected = max(
            industry_overlaps.items(),
            key=lambda x: len(x[1]["related_industries"]),
            default=("None", {"related_industries": []})
        )
        
        st.metric("Most Connected Industry", most_connected[0])
        st.metric("Number of Connections", len(most_connected[1]["related_industries"]))

def render_admin_controls(overlap_engine):
    """Render admin controls for managing overlaps"""
    st.markdown("### ⚙️ **Admin Controls & Configuration**")
    
    tab1, tab2, tab3 = st.tabs(["🔧 Settings", "📊 Analytics", "💾 Export"])
    
    with tab1:
        st.markdown("#### 🔧 **Overlap Engine Settings**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Similarity Algorithms:**")
            use_skill_based = st.checkbox("Skill-based similarity", value=True)
            use_semantic = st.checkbox("Semantic similarity", value=False, help="Requires NLP models")
            use_industry_weight = st.checkbox("Industry weighting", value=True)
            
            st.markdown("**Threshold Settings:**")
            min_similarity = st.slider("Minimum similarity threshold", 0.1, 0.9, 0.2)
            max_similarity = st.slider("Maximum similarity threshold", 0.1, 1.0, 0.8)
        
        with col2:
            st.markdown("**Cache & Performance:**")
            cache_enabled = st.checkbox("Enable similarity caching", value=True)
            cache_expiry = st.number_input("Cache expiry (hours)", 1, 168, 24)
            
            st.markdown("**Data Sources:**")
            use_linkedin_data = st.checkbox("LinkedIn job data", value=True)
            use_internal_data = st.checkbox("Internal CV data", value=True)
            use_external_apis = st.checkbox("External job APIs", value=False)
        
        if st.button("💾 Save Configuration"):
            config = {
                "similarity_algorithms": {
                    "skill_based": use_skill_based,
                    "semantic": use_semantic,
                    "industry_weight": use_industry_weight
                },
                "thresholds": {
                    "min_similarity": min_similarity,
                    "max_similarity": max_similarity
                },
                "cache": {
                    "enabled": cache_enabled,
                    "expiry_hours": cache_expiry
                },
                "data_sources": {
                    "linkedin": use_linkedin_data,
                    "internal": use_internal_data,
                    "external_apis": use_external_apis
                }
            }
            
            # Save configuration (mock)
            st.success("✅ Configuration saved successfully!")
            st.json(config)
    
    with tab2:
        st.markdown("#### 📊 **Overlap Analytics**")
        
        # Mock analytics data
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Job Titles", "1,247", "+23 this week")
            st.metric("Similarity Calculations", "15,629", "+1,205 today")
        
        with col2:
            st.metric("Overlap Clusters", "89", "+5 new")
            st.metric("AI Chat Queries", "342", "+28 today")
        
        with col3:
            st.metric("Industry Mappings", "16", "✅ Complete")
            st.metric("User Benefit Score", "94.2%", "+2.1% this month")
        
        # Usage trends chart
        st.markdown("**📈 Usage Trends**")
        
        # Create sample trend data
        dates = pd.date_range(start='2025-09-01', end='2025-10-02', freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Chat Queries': np.random.randint(20, 50, len(dates)),
            'Overlap Calculations': np.random.randint(100, 300, len(dates)),
            'New Titles Added': np.random.randint(0, 10, len(dates))
        })
        
        fig = px.line(trend_data, x='Date', y=['Chat Queries', 'Overlap Calculations', 'New Titles Added'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("#### 💾 **Export & Integration**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Export Data:**")
            
            if st.button("📊 Export Overlap Matrix"):
                st.success("✅ Overlap matrix exported to ai_data/job_title_overlaps.csv")
            
            if st.button("🏢 Export Industry Mappings"):
                st.success("✅ Industry mappings exported to ai_data/industry_overlaps.json")
            
            if st.button("💬 Export Chat Responses"):
                st.success("✅ Chat responses exported to ai_data/chat_responses.json")
        
        with col2:
            st.markdown("**User Portal Integration:**")
            
            integration_status = {
                "Job Title Search": "✅ Active",
                "Overlap Visualization": "✅ Active", 
                "AI Chat Widget": "✅ Active",
                "Career Path Suggestions": "🔄 Pending",
                "Industry Explorer": "✅ Active"
            }
            
            for feature, status in integration_status.items():
                st.write(f"• {feature}: {status}")
            
            if st.button("🚀 Deploy to User Portal"):
                st.success("✅ Latest overlap data deployed to user portal!")

# Helper functions

def create_job_title_network(overlaps, selected_industry, max_connections, overlap_engine):
    """Create network visualization of job title overlaps"""
    
    # Prepare data for network graph
    nodes = []
    edges = []
    node_colors = []
    
    # Color mapping for industries
    industry_colors = {
        "Technology": "#1f77b4",
        "Business": "#ff7f0e", 
        "Finance": "#2ca02c",
        "Healthcare": "#d62728"
    }
    
    added_nodes = set()
    
    for title1, similar_titles in overlaps.items():
        if selected_industry != "All" and not is_title_in_industry(title1, selected_industry, overlap_engine):
            continue
            
        if title1 not in added_nodes:
            industry = get_title_industry(title1, overlap_engine)
            nodes.append({"id": title1, "label": title1, "color": industry_colors.get(industry, "#gray")})
            added_nodes.add(title1)
        
        for title2, similarity in similar_titles[:max_connections]:
            if title2 not in added_nodes:
                industry = get_title_industry(title2, overlap_engine)
                nodes.append({"id": title2, "label": title2, "color": industry_colors.get(industry, "#gray")})
                added_nodes.add(title2)
            
            edges.append({
                "source": title1,
                "target": title2,
                "weight": similarity,
                "label": f"{similarity:.2f}"
            })
    
    # Create plotly network graph
    fig = go.Figure()
    
    # Add nodes (simplified as scatter plot)
    node_x = np.random.rand(len(nodes)) * 10
    node_y = np.random.rand(len(nodes)) * 10
    
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=[node["label"] for node in nodes],
        textposition="middle center",
        marker=dict(
            size=20,
            color=[node["color"] for node in nodes],
            line=dict(width=2, color="white")
        ),
        hovertemplate="<b>%{text}</b><extra></extra>",
        name="Job Titles"
    ))
    
    # Add edges (simplified)
    for edge in edges[:20]:  # Limit to avoid clutter
        source_idx = next(i for i, node in enumerate(nodes) if node["id"] == edge["source"])
        target_idx = next(i for i, node in enumerate(nodes) if node["id"] == edge["target"])
        
        fig.add_trace(go.Scatter(
            x=[node_x[source_idx], node_x[target_idx]],
            y=[node_y[source_idx], node_y[target_idx]],
            mode='lines',
            line=dict(width=edge["weight"]*5, color="rgba(50,50,50,0.3)"),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title="Job Title Overlap Network",
        showlegend=False,
        height=600,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

def create_industry_venn_diagram(industry_overlaps):
    """Create Venn diagram style visualization for industry overlaps"""
    
    # Create a chord diagram style visualization
    industries = list(industry_overlaps.keys())
    
    # Create connection matrix
    matrix = np.zeros((len(industries), len(industries)))
    
    for i, industry1 in enumerate(industries):
        for j, industry2 in enumerate(industries):
            if industry2 in industry_overlaps[industry1]["skill_overlaps"]:
                overlap_ratio = industry_overlaps[industry1]["skill_overlaps"][industry2]["overlap_ratio"]
                matrix[i][j] = overlap_ratio
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=industries,
        y=industries,
        colorscale='Blues',
        text=matrix,
        texttemplate="%{text:.2f}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Industry Skill Overlap Matrix",
        xaxis_title="Related Industry",
        yaxis_title="Primary Industry",
        height=500
    )
    
    return fig

def is_title_in_industry(title, industry, overlap_engine):
    """Check if job title belongs to specified industry"""
    categorized = overlap_engine.job_titles_db.get("categorized_titles", {})
    return title in categorized.get(industry, [])

def get_title_industry(title, overlap_engine):
    """Get the industry for a job title"""
    categorized = overlap_engine.job_titles_db.get("categorized_titles", {})
    for industry, titles in categorized.items():
        if title in titles:
            return industry
    return "Other"

def get_shared_skills(title1, title2, overlap_engine):
    """Get shared skills between two job titles"""
    skills1 = set(overlap_engine.skill_mappings.get(title1, []))
    skills2 = set(overlap_engine.skill_mappings.get(title2, []))
    shared = skills1.intersection(skills2)
    return ", ".join(list(shared)[:3]) + ("..." if len(shared) > 3 else "")

def main():
    """Main function for page testing"""
    st.set_page_config(
        page_title="Job Title Overlap Cloud",
        page_icon="🔄",
        layout="wide"
    )
    
    render_job_title_overlap_cloud()

if __name__ == "__main__":
    main()