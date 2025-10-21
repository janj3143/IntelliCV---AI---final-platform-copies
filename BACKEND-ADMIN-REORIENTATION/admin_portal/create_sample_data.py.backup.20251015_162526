#!/usr/bin/env python3
"""
Sample data generator for testing revenue maximization system
"""
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
import random

def create_sample_subscription_data():
    """Create sample subscription data for testing."""
    db_path = "/app/db/intellicv_data.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create subscriptions table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_subscriptions (
                id TEXT PRIMARY KEY,
                user_email TEXT NOT NULL,
                user_name TEXT NOT NULL,
                subscription_tier TEXT NOT NULL,
                monthly_value INTEGER NOT NULL,
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                marketing_consent BOOLEAN DEFAULT 0,
                partner_sharing_consent BOOLEAN DEFAULT 0,
                birthday_campaign_consent BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sample subscription data
        sample_users = [
            {"name": "John Smith", "email": "john.smith@techcorp.com", "tier": "Premium", "value": 299},
            {"name": "Sarah Johnson", "email": "sarah.j@startup.io", "tier": "Pro", "value": 149}, 
            {"name": "Mike Davis", "email": "m.davis@consulting.com", "tier": "Basic+", "value": 79},
            {"name": "Lisa Chen", "email": "lisa.chen@enterprise.com", "tier": "Enterprise", "value": 599},
            {"name": "David Wilson", "email": "david.w@freelance.com", "tier": "Pro", "value": 149},
            {"name": "Emma Brown", "email": "emma.brown@agency.com", "tier": "Premium", "value": 299},
            {"name": "Alex Martinez", "email": "alex.m@tech.com", "tier": "Basic+", "value": 79},
            {"name": "Rachel Green", "email": "r.green@corp.com", "tier": "Enterprise", "value": 599},
        ]
        
        for user in sample_users:
            # Random subscription dates
            start_date = datetime.now() - timedelta(days=random.randint(30, 365))
            end_date = start_date + timedelta(days=365)  # 1 year subscription
            
            # Some subscriptions expiring soon for testing
            if random.random() < 0.3:  # 30% chance of expiring soon
                end_date = datetime.now() + timedelta(days=random.randint(1, 30))
            
            subscription_data = {
                "id": str(uuid.uuid4()),
                "user_email": user["email"],
                "user_name": user["name"],
                "subscription_tier": user["tier"],
                "monthly_value": user["value"],
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "is_active": 1,
                "marketing_consent": random.choice([0, 1]),
                "partner_sharing_consent": random.choice([0, 1]),
                "birthday_campaign_consent": random.choice([0, 1])
            }
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_subscriptions 
                (id, user_email, user_name, subscription_tier, monthly_value, 
                 start_date, end_date, is_active, marketing_consent, 
                 partner_sharing_consent, birthday_campaign_consent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                subscription_data["id"],
                subscription_data["user_email"],
                subscription_data["user_name"],
                subscription_data["subscription_tier"],
                subscription_data["monthly_value"],
                subscription_data["start_date"],
                subscription_data["end_date"],
                subscription_data["is_active"],
                subscription_data["marketing_consent"],
                subscription_data["partner_sharing_consent"],
                subscription_data["birthday_campaign_consent"]
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Created sample subscription data for {len(sample_users)} users")
        print("💰 Subscription tiers: Premium, Pro, Basic+, Enterprise")
        print("🔄 Some subscriptions set to expire soon for testing renewal system")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

if __name__ == "__main__":
    create_sample_subscription_data()