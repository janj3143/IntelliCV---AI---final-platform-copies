"""
🎯 IntelliCV Requirements Sidebar Display
Comprehensive requirements organization and installation guide
"""

import streamlit as st
import pandas as pd
from pathlib import Path

def display_requirements_sidebar():
    """Display comprehensive requirements in sidebar with installation guides"""
    
    st.sidebar.markdown("## 📦 **IntelliCV Requirements**")
    st.sidebar.markdown("*Modular Dependency Management*")
    
    # Category selector
    category = st.sidebar.selectbox(
        "📋 Select Category:",
        [
            "🎯 Core Platform",
            "🤖 AI & Machine Learning", 
            "🌐 Web Framework & APIs",
            "📊 Data Processing",
            "🛠️ Development Tools",
            "🏢 Enterprise Features",
            "📈 Installation Statistics",
            "🔧 Quick Setup Guide"
        ]
    )
    
    if category == "🎯 Core Platform":
        show_core_requirements()
    elif category == "🤖 AI & Machine Learning":
        show_ai_requirements()
    elif category == "🌐 Web Framework & APIs":
        show_web_requirements()
    elif category == "📊 Data Processing":
        show_data_requirements()
    elif category == "🛠️ Development Tools":
        show_dev_requirements()
    elif category == "🏢 Enterprise Features":
        show_enterprise_requirements()
    elif category == "📈 Installation Statistics":
        show_installation_stats()
    elif category == "🔧 Quick Setup Guide":
        show_quick_setup()

def show_core_requirements():
    """Display core platform requirements"""
    st.sidebar.markdown("### 🎯 **Core Platform**")
    st.sidebar.markdown("*Essential for basic functionality*")
    
    core_packages = [
        ("streamlit", "≥1.28.0", "Primary UI framework"),
        ("pandas", "≥2.1.0", "Data processing core"),
        ("plotly", "≥5.17.0", "Interactive visualizations"),
        ("requests", "≥2.31.0", "HTTP client"),
        ("pillow", "≥10.0.0", "Image processing"),
        ("psutil", "≥5.9.0", "System monitoring"),
        ("python-dotenv", "≥1.0.0", "Environment config")
    ]
    
    for pkg, version, desc in core_packages:
        st.sidebar.markdown(f"• **{pkg}** `{version}`")
        st.sidebar.caption(f"  ↳ {desc}")
    
    st.sidebar.markdown("**Installation:**")
    st.sidebar.code("pip install -r requirements_core.txt", language="bash")
    
    st.sidebar.markdown("**Size:** ~150MB | **Time:** ~2-3 minutes")

def show_ai_requirements():
    """Display AI/ML requirements"""
    st.sidebar.markdown("### 🤖 **AI & Machine Learning**")
    st.sidebar.markdown("*Advanced AI capabilities*")
    
    ai_packages = [
        ("openai", "≥1.0.0", "OpenAI API integration"),
        ("anthropic", "≥0.7.0", "Claude AI integration"),
        ("transformers", "≥4.35.0", "HuggingFace models"),
        ("torch", "≥2.1.0", "PyTorch ML framework"),
        ("spacy", "≥3.7.0", "Advanced NLP"),
        ("langchain", "≥0.0.350", "LLM framework"),
        ("sentence-transformers", "≥2.2.2", "Embeddings")
    ]
    
    for pkg, version, desc in ai_packages:
        st.sidebar.markdown(f"• **{pkg}** `{version}`")
        st.sidebar.caption(f"  ↳ {desc}")
    
    st.sidebar.markdown("**Installation:**")
    st.sidebar.code("pip install -r requirements_ai.txt", language="bash")
    
    st.sidebar.warning("⚠️ **Large Download**: ~2-4GB | **Time**: 15-30 minutes")

def show_web_requirements():
    """Display web framework requirements"""
    st.sidebar.markdown("### 🌐 **Web Framework & APIs**")
    st.sidebar.markdown("*Web services and integrations*")
    
    web_packages = [
        ("fastapi", "≥0.104.0", "High-performance web framework"),
        ("uvicorn", "≥0.24.0", "ASGI server"),
        ("httpx", "≥0.25.0", "Async HTTP client"),
        ("beautifulsoup4", "≥4.12.0", "HTML parsing"),
        ("selenium", "≥4.15.0", "Browser automation"),
        ("redis", "≥5.0.0", "In-memory data store"),
        ("sqlalchemy", "≥2.0.0", "ORM framework")
    ]
    
    for pkg, version, desc in web_packages:
        st.sidebar.markdown(f"• **{pkg}** `{version}`")
        st.sidebar.caption(f"  ↳ {desc}")
    
    st.sidebar.markdown("**Installation:**")
    st.sidebar.code("pip install -r requirements_web.txt", language="bash")
    
    st.sidebar.markdown("**Size:** ~300MB | **Time:** ~5-8 minutes")

def show_data_requirements():
    """Display data processing requirements"""
    st.sidebar.markdown("### 📊 **Data Processing**")
    st.sidebar.markdown("*Advanced analytics and file processing*")
    
    data_packages = [
        ("seaborn", "≥0.12.0", "Statistical visualizations"),
        ("scipy", "≥1.11.0", "Scientific computing"),
        ("PyPDF2", "≥3.0.1", "PDF processing"),
        ("python-docx", "≥0.8.11", "Word documents"),
        ("geopandas", "≥0.14.0", "Geospatial analysis"),
        ("folium", "≥0.14.0", "Interactive mapping"),
        ("prophet", "≥1.1.4", "Time series forecasting")
    ]
    
    for pkg, version, desc in data_packages:
        st.sidebar.markdown(f"• **{pkg}** `{version}`")
        st.sidebar.caption(f"  ↳ {desc}")
    
    st.sidebar.markdown("**Installation:**")
    st.sidebar.code("pip install -r requirements_data.txt", language="bash")
    
    st.sidebar.markdown("**Size:** ~500MB | **Time:** ~8-12 minutes")

def show_dev_requirements():
    """Display development tools requirements"""
    st.sidebar.markdown("### 🛠️ **Development Tools**")
    st.sidebar.markdown("*Testing, linting, and quality tools*")
    
    dev_packages = [
        ("pytest", "≥7.4.0", "Testing framework"),
        ("black", "≥23.9.0", "Code formatting"),
        ("mypy", "≥1.6.0", "Type checking"),
        ("bandit", "≥1.7.5", "Security analysis"),
        ("sphinx", "≥7.2.0", "Documentation"),
        ("jupyter", "≥1.0.0", "Interactive development"),
        ("locust", "≥2.17.0", "Load testing")
    ]
    
    for pkg, version, desc in dev_packages:
        st.sidebar.markdown(f"• **{pkg}** `{version}`")
        st.sidebar.caption(f"  ↳ {desc}")
    
    st.sidebar.markdown("**Installation:**")
    st.sidebar.code("pip install -r requirements_dev.txt", language="bash")
    
    st.sidebar.info("💡 **Development Only** - Not needed for production")

def show_enterprise_requirements():
    """Display enterprise features requirements"""
    st.sidebar.markdown("### 🏢 **Enterprise Features**")
    st.sidebar.markdown("*Scalability and enterprise integration*")
    
    enterprise_packages = [
        ("celery", "≥5.3.0", "Distributed task queue"),
        ("sentry-sdk", "≥1.38.0", "Error monitoring"),
        ("prometheus-client", "≥0.19.0", "Metrics collection"),
        ("kubernetes", "≥28.1.0", "Container orchestration"),
        ("hvac", "≥2.0.0", "HashiCorp Vault client"),
        ("azure-identity", "≥1.15.0", "Azure authentication"),
        ("slack-sdk", "≥3.25.0", "Team communication")
    ]
    
    for pkg, version, desc in enterprise_packages:
        st.sidebar.markdown(f"• **{pkg}** `{version}`")
        st.sidebar.caption(f"  ↳ {desc}")
    
    st.sidebar.markdown("**Installation:**")
    st.sidebar.code("pip install -r requirements_enterprise.txt", language="bash")
    
    st.sidebar.error("🏢 **Enterprise Only** - Requires additional infrastructure")

def show_installation_stats():
    """Show installation statistics and metrics"""
    st.sidebar.markdown("### 📈 **Installation Statistics**")
    
    # Create stats data
    stats_data = {
        "Category": ["Core", "AI/ML", "Web", "Data", "Dev", "Enterprise"],
        "Packages": [7, 15, 12, 10, 18, 20],
        "Size (MB)": [150, 3500, 300, 500, 200, 400],
        "Time (min)": [3, 25, 8, 12, 5, 10]
    }
    
    df = pd.DataFrame(stats_data)
    
    st.sidebar.dataframe(df, use_container_width=True)
    
    # Total statistics
    st.sidebar.markdown("**📊 Totals:**")
    st.sidebar.markdown(f"• **Total Packages**: {df['Packages'].sum()}")
    st.sidebar.markdown(f"• **Total Size**: ~{df['Size (MB)'].sum():,} MB")
    st.sidebar.markdown(f"• **Total Time**: ~{df['Time (min)'].sum()} minutes")
    
    st.sidebar.markdown("**🎯 Recommendations:**")
    st.sidebar.markdown("• Start with **Core** requirements")
    st.sidebar.markdown("• Add **AI/ML** for intelligent features")
    st.sidebar.markdown("• Use **Dev** tools during development")
    st.sidebar.markdown("• **Enterprise** for production scaling")

def show_quick_setup():
    """Show quick setup guide"""
    st.sidebar.markdown("### 🔧 **Quick Setup Guide**")
    
    st.sidebar.markdown("**1. 🎯 Minimal Setup (Core Only)**")
    st.sidebar.code("""
pip install -r requirements_core.txt
streamlit run admin_portal/pages/00_Home.py
    """, language="bash")
    
    st.sidebar.markdown("**2. 🤖 AI-Powered Setup**")
    st.sidebar.code("""
pip install -r requirements_core.txt
pip install -r requirements_ai.txt
    """, language="bash")
    
    st.sidebar.markdown("**3. 🌐 Full Web Platform**")
    st.sidebar.code("""
pip install -r requirements_core.txt
pip install -r requirements_web.txt
pip install -r requirements_data.txt
    """, language="bash")
    
    st.sidebar.markdown("**4. 🚀 Complete Installation**")
    st.sidebar.code("""
# Install all categories (except enterprise)
pip install -r requirements_core.txt
pip install -r requirements_ai.txt
pip install -r requirements_web.txt
pip install -r requirements_data.txt
pip install -r requirements_dev.txt
    """, language="bash")
    
    st.sidebar.warning("⚠️ **Note**: Enterprise features require additional infrastructure setup")
    
    st.sidebar.markdown("**🔗 Docker Quick Start:**")
    st.sidebar.code("""
docker-compose up --build
# Access at http://localhost:8501
    """, language="bash")

# Usage example
if __name__ == "__main__":
    display_requirements_sidebar()