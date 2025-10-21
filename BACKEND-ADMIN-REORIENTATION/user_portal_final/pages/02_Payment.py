"""
💳 IntelliCV-AI Payment Page
===========================
Step 2: Payment Processing
"""

import streamlit as st
from pathlib import Path
import sys
import time
from datetime import datetime

# Setup paths and imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Import utilities with fallbacks
try:
    from utils.error_handler import handle_exceptions, log_user_action, show_error, show_success
    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def handle_exceptions(func):
        return func
    def log_user_action(action, details=None):
        pass
    def show_error(msg, details=None):
        st.error(f"❌ {msg}")
    def show_success(msg, details=None):
        st.success(f"✅ {msg}")

# Import admin portal integration for payment gateway and subscription sync
try:
    from user_portal_admin_integration import (
        process_payment_with_stripe,
        sync_subscription_to_admin_portal,
        get_features_for_plan
    )
    ADMIN_PORTAL_INTEGRATION_AVAILABLE = True
except ImportError:
    ADMIN_PORTAL_INTEGRATION_AVAILABLE = False
    def process_payment_with_stripe(payment_data):
        return {'success': False, 'message': 'Payment gateway not available'}
    def sync_subscription_to_admin_portal(user_data, subscription_data):
        return {'success': False, 'message': 'Admin portal sync not available'}
    def get_features_for_plan(plan):
        return []

# Page configuration
st.set_page_config(
    page_title="💳 Payment | IntelliCV-AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Check if user has completed registration
if not st.session_state.get('registration_data'):
    st.error("❌ Please complete registration first")
    if st.button("🔙 Go to Registration"):
        st.switch_page("pages/01_Registration.py")
    st.stop()

# Professional CSS styling
def load_payment_css():
    """Load payment page specific CSS"""
    css = '''
    <style>
    /* Clean background */
    .stApp {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
    }
    
    /* Main Container */
    .main .block-container {
        background: rgba(255,255,255,0.97) !important;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Header styling */
    .payment-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .payment-header h1 {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Payment cards */
    .payment-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    /* Order summary */
    .order-summary {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Progress steps */
    .progress-steps {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .step {
        padding: 0.5rem 1rem;
        margin: 0 0.5rem;
        background: #f8f9fa;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .step.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .step.completed {
        background: #28a745;
        color: white;
    }
    
    /* Security badges */
    .security-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .security-badge {
        background: #e8f5e8;
        color: #28a745;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        border: 1px solid #28a745;
    }
    
    /* Payment methods */
    .payment-methods {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .payment-method {
        padding: 0.5rem 1rem;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        background: white;
    }
    
    .payment-method:hover {
        border-color: #667eea;
    }
    
    .payment-method.selected {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_payment_css()

# Log page access
if ERROR_HANDLER_AVAILABLE:
    log_user_action("page_view", {"page": "payment", "timestamp": datetime.now().isoformat()})

# Progress steps
st.markdown('''
<div class="progress-steps">
    <div class="step completed">1. Registration</div>
    <div class="step active">2. Payment</div>
    <div class="step">3. Profile Setup</div>
</div>
''', unsafe_allow_html=True)

# Header
st.markdown('''
<div class="payment-header">
    <h1>💳 Complete Your Purchase</h1>
    <p>Secure payment processing for your IntelliCV-AI subscription</p>
</div>
''', unsafe_allow_html=True)

# Get registration data
reg_data = st.session_state['registration_data']
selected_plan = reg_data.get('selected_plan', 'free')
plan_price = reg_data.get('plan_price', 0)

# Plan details mapping
plan_details = {
    'free': {'name': 'Free Trial', 'price': 0, 'billing': 'No charge', 'features': ['3 Resume generations', 'Basic job matching', 'Standard templates', 'Email support']},
    'monthly': {'name': 'Monthly Pro', 'price': 9.99, 'billing': 'Billed monthly', 'features': ['Unlimited resume generations', 'Advanced AI job matching', 'Premium templates', 'Priority support', 'LinkedIn integration', 'Application tracking']},
    'annual': {'name': 'Annual Pro', 'price': 89.99, 'billing': 'Billed annually (Save $30!)', 'features': ['Everything in Monthly Pro', 'Career workbook generator', 'Industry insights', '1-on-1 career consultation', 'Early access to new features']}
}

current_plan = plan_details[selected_plan]

# Sidebar navigation
with st.sidebar:
    if st.button("🔙 Back to Registration", use_container_width=True):
        st.switch_page("pages/01_Registration.py")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("pages/00_Home.py")
    
    st.markdown("---")
    st.markdown("### 🛡️ Security Features")
    st.markdown("""
    - 🔒 **SSL Encrypted** - All data encrypted in transit
    - 💳 **PCI Compliant** - Secure payment processing
    - 🛡️ **Fraud Protection** - Advanced security monitoring
    - 📱 **2FA Ready** - Two-factor authentication available
    """)

# Main content
col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.markdown('<div class="payment-card">', unsafe_allow_html=True)
    
    if current_plan['price'] == 0:
        # Free plan - no payment needed
        st.markdown("### 🎉 Free Trial - No Payment Required!")
        st.success("Your Free Trial is ready to activate - no payment needed!")
        
        st.markdown("**What happens next:**")
        st.markdown("""
        1. ✅ Your account will be created immediately
        2. 🚀 You'll be redirected to complete your profile
        3. 🎯 Start using IntelliCV-AI right away
        4. 📧 You'll receive a welcome email with tips
        """)
        
        if st.button("🚀 Activate Free Trial & Continue", use_container_width=True, type="primary"):
            # Sync free trial to admin portal
            if ADMIN_PORTAL_INTEGRATION_AVAILABLE:
                user_data = {
                    'user_id': st.session_state.get('user_id', f"user_{int(time.time())}"),
                    'username': reg_data['username'],
                    'email': reg_data['email']
                }
                subscription_data = {
                    'plan': 'free',
                    'price': 0,
                    'status': 'active',
                    'payment_method': 'none',
                    'billing_cycle': 'none'
                }
                admin_sync = sync_subscription_to_admin_portal(user_data, subscription_data)
                
                if admin_sync['success']:
                    st.success("🔗 Free trial synced to admin portal")
                    with st.expander("✨ Your Enabled Features"):
                        for feature in admin_sync['access_features']:
                            st.markdown(f"✅ {feature.replace('_', ' ').title()}")
            
            # Create user account
            st.session_state['authenticated_user'] = reg_data['username']
            st.session_state['user_role'] = 'user'
            st.session_state['user_email'] = reg_data['email']
            st.session_state['session_token'] = f"token_{int(time.time())}"
            st.session_state['is_new_user'] = True
            st.session_state['subscription_plan'] = 'free'
            st.session_state['subscription_status'] = 'active'
            
            if ERROR_HANDLER_AVAILABLE:
                log_user_action("free_trial_activated", {
                    "username": reg_data['username'], 
                    "email": reg_data['email'],
                    "plan": "free"
                })
            
            show_success("🎉 Free trial activated! Redirecting to profile setup...")
            st.balloons()
            time.sleep(2)
            st.switch_page("pages/03_Profile_Setup.py")
    
    else:
        # Paid plans - show payment form
        st.markdown(f"### 💳 Payment for {current_plan['name']}")
        
        # Payment method selection
        st.markdown("**Select Payment Method:**")
        payment_method = st.radio(
            "Choose payment method",
            ["💳 Credit/Debit Card", "🏦 PayPal", "🍎 Apple Pay", "📱 Google Pay"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if "Credit/Debit Card" in payment_method:
            # Credit card form
            with st.form("payment_form"):
                st.markdown("**Card Information**")
                
                # Card brand detection helper
                def detect_card_brand(card_num):
                    """Detect card brand from card number"""
                    clean_num = card_num.replace(" ", "").replace("-", "")
                    if not clean_num:
                        return None
                    
                    # Visa: starts with 4
                    if clean_num[0] == '4':
                        return 'Visa'
                    # Mastercard: starts with 51-55 or 2221-2720
                    elif len(clean_num) >= 2:
                        if clean_num[:2] in [str(i) for i in range(51, 56)]:
                            return 'Mastercard'
                        elif len(clean_num) >= 4 and 2221 <= int(clean_num[:4]) <= 2720:
                            return 'Mastercard'
                    return None
                
                # Display accepted card brands
                st.markdown("**We Accept:** 💳 Visa | 💳 Mastercard | 💳 American Express | 💳 Discover")
                
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", max_chars=19, 
                                               help="Enter your 16-digit card number")
                    # Display detected card brand
                    if card_number:
                        brand = detect_card_brand(card_number)
                        if brand:
                            st.caption(f"✅ {brand} detected")
                with col_b:
                    cvv = st.text_input("CVV", placeholder="123", max_chars=4, type="password")
                
                col_c, col_d = st.columns(2)
                with col_c:
                    exp_month = st.selectbox("Expiry Month", [f"{i:02d}" for i in range(1, 13)])
                with col_d:
                    exp_year = st.selectbox("Expiry Year", [str(2024 + i) for i in range(10)])
                
                card_name = st.text_input("Cardholder Name", placeholder="John Doe")
                
                st.markdown("**Billing Address**")
                billing_address = st.text_input("Address", placeholder="123 Main St")
                
                col_e, col_f = st.columns([2, 1])
                with col_e:
                    billing_city = st.text_input("City", placeholder="New York")
                with col_f:
                    billing_zip = st.text_input("ZIP Code", placeholder="10001")
                
                billing_country = st.selectbox("Country", ["United States", "Canada", "United Kingdom", "Australia", "Other"])
                
                # Terms
                agree_billing = st.checkbox("✅ I agree to the billing terms and conditions")
                
                # Submit payment
                col_pay, col_cancel = st.columns(2)
                
                with col_pay:
                    submitted = st.form_submit_button(f"💳 Pay ${current_plan['price']:.2f}", use_container_width=True, type="primary")
                
                with col_cancel:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.switch_page("pages/01_Registration.py")
                
                if submitted:
                    # Validation
                    required_fields = [card_number, cvv, card_name, billing_address, billing_city, billing_zip]
                    if not all(required_fields):
                        show_error("Please fill in all payment fields")
                    elif not agree_billing:
                        show_error("Please agree to the billing terms")
                    elif len(card_number.replace(" ", "")) < 13:
                        show_error("Please enter a valid card number")
                    else:
                        # Process payment through Stripe and sync to admin portal
                        with st.spinner("Processing payment..."):
                            # Prepare payment data
                            payment_data = {
                                'user_id': st.session_state.get('user_id', f"user_{int(time.time())}"),
                                'username': reg_data['username'],
                                'email': reg_data['email'],
                                'plan': selected_plan,
                                'amount': current_plan['price'],
                                'payment_method': 'card',
                                'billing_cycle': 'monthly' if selected_plan == 'monthly' else 'annual',
                                'cardholder_name': card_name,
                                'card_last4': card_number.replace(" ", "")[-4:] if len(card_number.replace(" ", "")) >= 4 else '****'
                            }
                            
                            # Process payment with Stripe and admin portal sync
                            if ADMIN_PORTAL_INTEGRATION_AVAILABLE:
                                payment_result = process_payment_with_stripe(payment_data)
                                
                                if payment_result['success']:
                                    show_success(f"✅ Payment processed successfully! Transaction ID: {payment_result['payment']['transaction_id']}")
                                    
                                    # Display enabled features
                                    if payment_result['admin_sync']['success']:
                                        st.success("🔗 Subscription synced to admin portal")
                                        enabled_features = payment_result['admin_sync']['access_features']
                                        with st.expander("✨ Your Enabled Features"):
                                            for feature in enabled_features:
                                                st.markdown(f"✅ {feature.replace('_', ' ').title()}")
                                else:
                                    show_error(f"Payment failed: {payment_result.get('message', 'Unknown error')}")
                                    st.stop()
                            else:
                                # Fallback to simulation if admin portal not available
                                time.sleep(3)
                                show_success("✅ Payment processed (simulation mode)")
                        
                        # Create user account with paid subscription
                        st.session_state['authenticated_user'] = reg_data['username']
                        st.session_state['user_role'] = 'user'
                        st.session_state['user_email'] = reg_data['email']
                        st.session_state['session_token'] = f"token_{int(time.time())}"
                        st.session_state['is_new_user'] = True
                        st.session_state['subscription_plan'] = selected_plan
                        st.session_state['subscription_status'] = 'active'
                        st.session_state['payment_method'] = payment_method
                        
                        if ERROR_HANDLER_AVAILABLE:
                            log_user_action("payment_completed", {
                                "username": reg_data['username'],
                                "email": reg_data['email'], 
                                "plan": selected_plan,
                                "amount": current_plan['price'],
                                "payment_method": payment_method
                            })
                        
                        show_success(f"✅ Payment successful! Welcome to {current_plan['name']}!")
                        st.balloons()
                        time.sleep(2)
                        st.switch_page("pages/03_Profile_Setup.py")
        
        else:
            # Other payment methods (placeholder)
            st.info(f"🚧 {payment_method} integration coming soon! Please use Credit/Debit Card for now.")
            
            if st.button("🔙 Use Credit/Debit Card Instead", use_container_width=True):
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Order summary
    st.markdown("### 📋 Order Summary")
    st.markdown('<div class="order-summary">', unsafe_allow_html=True)
    
    st.markdown(f"**Plan:** {current_plan['name']}")
    st.markdown(f"**Price:** ${current_plan['price']:.2f}")
    st.markdown(f"**Billing:** {current_plan['billing']}")
    
    st.markdown("**Features Included:**")
    for feature in current_plan['features']:
        st.markdown(f"• {feature}")
    
    if current_plan['price'] > 0:
        st.markdown("---")
        st.markdown("**Total:** $" + f"{current_plan['price']:.2f}")
        
        if selected_plan == 'annual':
            st.success("💰 You save $30 compared to monthly billing!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Security badges
    st.markdown("### 🛡️ Secure Payment")
    st.markdown('''
    <div class="security-badges">
        <div class="security-badge">🔒 SSL Encrypted</div>
        <div class="security-badge">💳 PCI Compliant</div>
        <div class="security-badge">🛡️ Fraud Protected</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Customer info
    st.markdown("### 👤 Account Details")
    st.info(f"""
    **Name:** {reg_data['first_name']} {reg_data['last_name']}
    **Email:** {reg_data['email']}
    **Username:** {reg_data['username']}
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>IntelliCV-AI</strong> | Secure Payment Processing</p>
    <p>🔒 256-bit SSL Encryption • 💳 PCI DSS Compliant • 🛡️ Fraud Protection • 📞 24/7 Support</p>
</div>
""", unsafe_allow_html=True)
