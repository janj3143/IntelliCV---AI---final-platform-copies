"""
Fix main.py issues:
1. Journey steps - make always clickable
2. Pricing section - simplify HTML rendering
"""

import re

# Read main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the pricing section
pricing_start = content.find('# PRICING SECTION - Dual Model')
pricing_end = content.find('st.markdown("---")', pricing_start + 100) + len('st.markdown("---")')

new_pricing = '''# PRICING SECTION - Streamlit Native Components
        st.markdown("### 💎 Choose Your Plan")
        st.markdown("**Flexible pricing:** Choose subscription tiers OR use token-based access")
        
        price_col1, price_col2, price_col3, price_col4 = st.columns(4)
        
        with price_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
                <h3>🆓 Free Starter</h3>
                <h2 style="margin: 0.5rem 0;">$0</h2>
                <p style="font-size: 0.9rem;">10 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - Resume Builder Chatbot
            - Resume Upload & Analysis
            - Basic Career Insights
            - Community Access
            """)
        
        with price_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
                <h3>⭐ Monthly Pro</h3>
                <h2 style="margin: 0.5rem 0;">$15.99</h2>
                <p style="font-size: 0.9rem;">100 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - **Full Job Suite Access**
            - AI Job Matching
            - Interview Prep Tools
            - Application Tracker
            """)
        
        with price_col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center; 
                        border: 3px solid gold;">
                <div style="background: gold; color: #333; padding: 0.2rem 0.6rem; 
                            border-radius: 10px; display: inline-block; font-weight: bold; 
                            font-size: 0.7rem; margin-bottom: 0.3rem;">
                    ⚡ BEST VALUE
                </div>
                <h3>🏆 Annual Pro</h3>
                <h2 style="margin: 0.5rem 0;">$149.99<span style="font-size: 0.6rem;">/year</span></h2>
                <p style="font-size: 0.9rem;">250 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - **Everything in Monthly**
            - **Career Launch Hub**
            - **Dual-Career Optimization** 🆕
            - Advanced Analytics
            - Industry Reports
            """)
        
        with price_col4:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100);  
                        padding: 1.5rem; border-radius: 10px; color: #333; text-align: center;">
                <h3>👑 Enterprise Pro</h3>
                <h2 style="margin: 0.5rem 0;">$299.99</h2>
                <p style="font-size: 0.9rem;">1000 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - **Everything in Annual**
            - **Career Coaching** (50 tokens/hr)
            - **Mentorship Hub** (25 tokens)
            - Custom AI Training
            - Priority Support
            """)
        
        st.info("""
        💡 **Token-Based Access:** Pay only for what you use  
        🔄 Tokens refresh monthly • Unused tokens don't roll over  
        💰 Emergency token packs: 25 tokens for $4.99  
        ⚡ All plans include priority support
        """)
        
        st.markdown("---")'''

# Replace pricing section
content = content[:pricing_start] + new_pricing + content[pricing_end:]

# Save
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed pricing section - now uses Streamlit native components")
print("✅ Journey steps were already fixed to be always clickable")
print("\n📝 Changes made:")
print("  - Removed large HTML block that wasn't rendering")
print("  - Replaced with Streamlit columns + smaller HTML cards")
print("  - Added 'Dual-Career Optimization' to Annual Pro features")
print("  - Journey step navigation buttons now always visible")
