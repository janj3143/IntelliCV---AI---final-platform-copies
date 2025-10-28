"""
=============================================================================
Real AI Data Integration Demo Page
=============================================================================

Demonstrates the successful integration of real ai_data_final data
across all admin portal AI pages, replacing demo/sample data.

This page shows:
1. Real data loading and processing
2. Live analytics from ai_data_final
3. Comparison between demo and real data
4. Integration status across all pages

Author: IntelliCV-AI System
Date: December 2024
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, Any, List
import json

# Import the real AI data connector
try:
    from shared.real_ai_data_connector import (
        get_real_ai_connector, 
        get_real_sample_data, 
        get_real_analytics_data
    )
    REAL_AI_AVAILABLE = True
except ImportError:
    REAL_AI_AVAILABLE = False

def main():
    """Main demo page"""
    
    # Check authentication
    if not st.session_state.get('admin_authenticated', False):
        st.error("🔒 **Authentication Required**")
        st.info("Please login through the main admin portal to access this demo.")
        st.stop()
    
    st.set_page_config(
        page_title="Real AI Data Integration Demo",
        page_icon="🧠",
        layout="wide"
    )
    
    # Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;'>
        <h1>🧠 Real AI Data Integration Demo</h1>
        <h3>Production Data from ai_data_final</h3>
        <p>Showcasing real resume, profile, company, and job title data integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not REAL_AI_AVAILABLE:
        st.error("❌ **Real AI Data Connector Not Available**")
        st.warning("Please ensure the real_ai_data_connector module is properly installed.")
        st.stop()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Live Analytics", 
        "🧠 AI Processing Demo", 
        "📈 Market Intelligence", 
        "🔍 Data Explorer",
        "🔗 Integration Status"
    ])
    
    with tab1:
        show_live_analytics()
    
    with tab2:
        show_ai_processing_demo()
    
    with tab3:
        show_market_intelligence()
    
    with tab4:
        show_data_explorer()
    
    with tab5:
        show_integration_status()

def show_live_analytics():
    """Show live analytics from real ai_data_final"""
    
    st.markdown("### 📊 Live Analytics from ai_data_final")
    
    try:
        # Get real analytics
        analytics_data = get_real_analytics_data()
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_files = analytics_data['summary'].get('total_files', 0)
            st.metric("📁 Total Files", f"{total_files:,}", "Real JSON files")
        
        with col2:
            total_skills = analytics_data['skills_analysis'].get('total_skills', 0)
            st.metric("🔧 Unique Skills", f"{total_skills:,}", "AI-extracted")
        
        with col3:
            total_companies = analytics_data['company_analysis'].get('total_companies', 0)
            st.metric("🏢 Companies", f"{total_companies:,}", "In database")
        
        with col4:
            total_titles = analytics_data['job_titles_analysis'].get('total_unique_titles', 0)
            st.metric("💼 Job Titles", f"{total_titles:,}", "Unique positions")
        
        # Skills analysis
        st.markdown("#### 🏆 Top Skills from Real Data")
        
        top_skills = analytics_data['skills_analysis'].get('top_skills', {})
        if top_skills:
            # Create skills chart
            skills_df = pd.DataFrame([
                {'Skill': skill.title(), 'Mentions': count}
                for skill, count in list(top_skills.items())[:15]
            ])
            
            fig = px.bar(
                skills_df,
                x='Mentions',
                y='Skill',
                orientation='h',
                title="Most Mentioned Skills (Real ai_data_final)",
                color='Mentions',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Industry analysis  
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🏭 Top Industries")
            top_industries = analytics_data['company_analysis'].get('top_industries', {})
            
            for industry, count in list(top_industries.items())[:10]:
                st.write(f"• **{industry}** ({count:,} companies)")
        
        with col_b:
            st.markdown("#### 💼 Popular Job Titles")
            top_titles = analytics_data['job_titles_analysis'].get('top_job_titles', {})
            
            for title, count in list(top_titles.items())[:10]:
                st.write(f"• **{title.title()}** ({count:,})")
        
        st.success("✅ **All data above is REAL** - sourced directly from ai_data_final")
        
    except Exception as e:
        st.error(f"❌ Error loading real analytics: {e}")

def show_ai_processing_demo():
    """Demonstrate AI processing with real data"""
    
    st.markdown("### 🧠 AI Processing Demo - Real Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_type = st.selectbox(
            "Select Data Type:",
            ["resumes", "profiles", "companies", "job_titles"],
            help="Choose which type of real data to process"
        )
    
    with col2:
        limit = st.slider("Processing Limit:", 10, 500, 100)
    
    if st.button("🚀 Process Real Data", type="primary"):
        with st.spinner(f"Processing {limit} real {data_type} records..."):
            
            # Load real data
            real_data = get_real_sample_data(data_type, limit)
            
            if real_data:
                st.success(f"✅ Loaded {len(real_data)} real {data_type} records")
                
                # Process and analyze
                analysis = analyze_real_data(real_data, data_type)
                
                # Show results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Records Processed", len(real_data))
                
                with col2:
                    st.metric("Data Points Extracted", analysis.get('data_points', 0))
                
                with col3:
                    st.metric("Processing Quality", f"{analysis.get('quality_score', 0):.1f}/10")
                
                # Show sample processed data
                with st.expander(f"📋 Sample Processed {data_type.title()} Data"):
                    for i, record in enumerate(real_data[:3]):
                        st.markdown(f"**Record {i+1}:**")
                        
                        # Show key fields
                        key_fields = ['name', 'full_name', 'job_title', 'title', 'company', 'skills', 'industry']
                        displayed_data = {}
                        
                        for field in key_fields:
                            if field in record:
                                displayed_data[field] = record[field]
                        
                        if displayed_data:
                            st.json(displayed_data)
                        else:
                            # Show first few fields if no standard fields found
                            sample_fields = dict(list(record.items())[:5])
                            st.json(sample_fields)
                        
                        st.markdown("---")
            
            else:
                st.warning(f"⚠️ No {data_type} data found in ai_data_final")

def analyze_real_data(data: List[Dict], data_type: str) -> Dict:
    """Analyze real data and return metrics"""
    
    total_fields = 0
    quality_indicators = 0
    
    for record in data:
        total_fields += len(record)
        
        # Check for quality indicators
        if data_type == 'resumes':
            if 'skills' in record and record['skills']:
                quality_indicators += 1
            if 'experience' in record and record['experience']:
                quality_indicators += 1
        elif data_type == 'companies':
            if 'industry' in record and record['industry']:
                quality_indicators += 1
            if 'location' in record and record['location']:
                quality_indicators += 1
        # Add more quality checks as needed
    
    quality_score = min(10, (quality_indicators / len(data)) * 5) if data else 0
    
    return {
        'data_points': total_fields,
        'quality_score': quality_score,
        'quality_indicators': quality_indicators
    }

def show_market_intelligence():
    """Show market intelligence derived from real data"""
    
    st.markdown("### 📈 Market Intelligence from Real Data")
    
    try:
        analytics_data = get_real_analytics_data()
        
        # Skills market analysis
        st.markdown("#### 🎯 Skills Market Analysis")
        
        skills_analysis = analytics_data['skills_analysis']
        top_skills = skills_analysis.get('top_skills', {})
        
        if top_skills:
            # Create market value estimation
            market_data = []
            
            for skill, mentions in list(top_skills.items())[:20]:
                # Estimate market value based on mentions and skill type
                base_value = 75000
                
                # Premium skills
                if any(tech in skill.lower() for tech in ['ai', 'ml', 'machine learning']):
                    base_value = 150000
                elif any(tech in skill.lower() for tech in ['python', 'javascript', 'react']):
                    base_value = 120000
                elif any(tech in skill.lower() for tech in ['aws', 'cloud', 'docker']):
                    base_value = 130000
                
                # Adjust by demand (mentions)
                demand_factor = min(1.5, mentions / 50)
                estimated_salary = int(base_value * demand_factor)
                
                market_data.append({
                    'Skill': skill.title(),
                    'Mentions': mentions,
                    'Est. Salary': estimated_salary,
                    'Market Demand': 'High' if mentions > 50 else 'Medium' if mentions > 20 else 'Low'
                })
            
            market_df = pd.DataFrame(market_data)
            
            # Salary vs Demand chart
            fig = px.scatter(
                market_df,
                x='Mentions',
                y='Est. Salary',
                hover_data=['Skill', 'Market Demand'],
                title="Skills: Market Demand vs Estimated Salary (Real Data)",
                color='Market Demand',
                size='Mentions',
                size_max=20
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Top paying skills table
            top_paying = market_df.nlargest(10, 'Est. Salary')
            st.markdown("#### 💰 Highest Value Skills (Based on Real Data)")
            st.dataframe(top_paying, use_container_width=True)
        
        # Company analysis
        st.markdown("#### 🏢 Company & Industry Insights")
        
        company_analysis = analytics_data['company_analysis']
        top_industries = company_analysis.get('top_industries', {})
        
        if top_industries:
            col1, col2 = st.columns(2)
            
            with col1:
                # Industry distribution pie chart
                industries_df = pd.DataFrame([
                    {'Industry': industry, 'Companies': count}
                    for industry, count in list(top_industries.items())[:8]
                ])
                
                fig = px.pie(
                    industries_df,
                    values='Companies',
                    names='Industry',
                    title="Industry Distribution (Real Companies)"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Industry Rankings:**")
                for i, (industry, count) in enumerate(list(top_industries.items())[:10], 1):
                    st.write(f"{i}. **{industry}** - {count:,} companies")
        
        st.info("📊 All market intelligence above is derived from REAL data in ai_data_final")
        
    except Exception as e:
        st.error(f"❌ Error generating market intelligence: {e}")

def show_data_explorer():
    """Interactive data explorer for real ai_data_final"""
    
    st.markdown("### 🔍 Real Data Explorer")
    
    connector = get_real_ai_connector()
    
    # Data type selector
    data_types = {
        'Parsed Resumes': 'resumes',
        'Normalized Profiles': 'profiles', 
        'Company Data': 'companies',
        'Job Titles': 'job_titles',
        'User Profiles': 'users',
        'Email Extractions': 'emails'
    }
    
    selected_type = st.selectbox("Select Data Type to Explore:", list(data_types.keys()))
    data_key = data_types[selected_type]
    
    # Load and display data
    col1, col2 = st.columns([3, 1])
    
    with col2:
        sample_size = st.slider("Sample Size:", 5, 100, 20)
        
        if st.button("🔄 Load Sample", type="primary"):
            st.session_state[f'sample_{data_key}'] = get_real_sample_data(data_key, sample_size)
    
    with col1:
        if f'sample_{data_key}' in st.session_state:
            data = st.session_state[f'sample_{data_key}']
            
            if data:
                st.success(f"✅ Loaded {len(data)} real {selected_type.lower()} records")
                
                # Show data structure
                st.markdown("#### 📋 Data Structure Analysis")
                
                # Analyze fields across all records
                all_fields = set()
                for record in data:
                    all_fields.update(record.keys())
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric("Total Records", len(data))
                    st.metric("Unique Fields", len(all_fields))
                
                with col_b:
                    # Calculate completeness
                    total_possible = len(data) * len(all_fields)
                    filled_fields = sum(1 for record in data for field in all_fields if field in record and record[field])
                    completeness = (filled_fields / total_possible) * 100 if total_possible > 0 else 0
                    
                    st.metric("Data Completeness", f"{completeness:.1f}%")
                    st.metric("Avg Fields per Record", f"{sum(len(record) for record in data) / len(data):.1f}")
                
                # Show sample records
                st.markdown("#### 👀 Sample Records")
                
                # Display first few records
                for i, record in enumerate(data[:3]):
                    with st.expander(f"Record {i+1}"):
                        st.json(record)
                
                # Field frequency analysis
                st.markdown("#### 📊 Field Frequency Analysis")
                
                field_counts = {}
                for record in data:
                    for field in record:
                        if field in field_counts:
                            field_counts[field] += 1
                        else:
                            field_counts[field] = 1
                
                field_df = pd.DataFrame([
                    {'Field': field, 'Frequency': count, 'Coverage': f"{(count/len(data)*100):.1f}%"}
                    for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True)
                ])
                
                st.dataframe(field_df, use_container_width=True)
            
            else:
                st.warning(f"⚠️ No {selected_type.lower()} data found")

def show_integration_status():
    """Show integration status across all admin pages"""
    
    from shared.ai_data_integration_status import show_integration_status
    show_integration_status()

if __name__ == "__main__":
    main()