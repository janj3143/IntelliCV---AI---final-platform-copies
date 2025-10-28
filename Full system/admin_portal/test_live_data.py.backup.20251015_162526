#!/usr/bin/env python3
"""
Test script for live data integration
"""
import sys
sys.path.append('/app')

from modules.core.live_data_manager import LiveDataManager

def test_live_data():
    print("🔍 Testing Live Data Integration")
    print("=" * 50)
    
    try:
        ldm = LiveDataManager()
        
        # Test user data loading
        users = ldm.get_real_user_data()
        print(f"✅ Live data loaded: {len(users)} users")
        
        if users:
            print(f"📊 Sample user: {users[0]['name']} ({users[0]['subscription_tier']})")
        
        # Test renewal alerts
        alerts = ldm.get_subscription_renewal_alerts(30)
        print(f"🚨 Renewal alerts: {len(alerts)} users need attention")
        
        # Test marketing database
        marketing = ldm.get_marketing_database_users()
        print(f"📧 Marketing database: {marketing['marketing_opted_in']}/{marketing['total_users']} opted in")
        
        # Test real-time metrics
        metrics = ldm.get_real_time_metrics()
        print(f"💰 Monthly revenue: ${metrics['monthly_subscription_revenue']:,}")
        print(f"📊 Critical alerts: {metrics['critical_renewal_alerts']}")
        
        print("✅ All live data systems operational")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_live_data()