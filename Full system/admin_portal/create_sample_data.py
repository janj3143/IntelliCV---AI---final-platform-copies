#!/usr/bin/env python3
"""
Sample data generator for testing revenue maximization system
Uses real CV data from ai_data_final for realistic user profiles
"""
import sqlite3
import json
import uuid
import sys
from datetime import datetime, timedelta
import random
from pathlib import Path

# Import AI data loader
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from ai_data_loader import AIDataLoader
    ai_loader = AIDataLoader()
    AI_LOADER_AVAILABLE = True
except ImportError:
    AI_LOADER_AVAILABLE = False
    ai_loader = None

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
        
        # Load sample users from AI data (real CV data) or use minimal fallback
        sample_users = []
        
        if AI_LOADER_AVAILABLE and ai_loader:
            try:
                # Get real CV files from ai_data_final
                cv_files = ai_loader.get_cv_files()[:8]  # Get up to 8 CVs
                
                tier_rotation = ["Premium", "Pro", "Basic+", "Enterprise"]
                value_map = {"Premium": 299, "Pro": 149, "Basic+": 79, "Enterprise": 599}
                
                for idx, cv_file in enumerate(cv_files):
                    try:
                        cv_data = ai_loader.load_cv_data(cv_file)
                        name = cv_data.get('name', f'User {idx+1}')
                        # Generate email from name
                        email_name = name.lower().replace(' ', '.').replace("'", '')
                        domain = cv_data.get('company', 'example.com').lower().replace(' ', '').replace(',', '')[:20]
                        email = f"{email_name}@{domain}.com"
                        
                        tier = tier_rotation[idx % len(tier_rotation)]
                        sample_users.append({
                            "name": name,
                            "email": email,
                            "tier": tier,
                            "value": value_map[tier]
                        })
                    except Exception as e:
                        print(f"Warning: Could not load CV {cv_file}: {e}")
                        continue
                
                if sample_users:
                    print(f"✅ Loaded {len(sample_users)} users from real CV data")
            except Exception as e:
                print(f"Warning: Could not load AI data: {e}")
        
        # Minimal fallback if AI loader unavailable or no CVs found
        if not sample_users:
            print("Using minimal fallback user data (AI loader unavailable)")
            sample_users = [
                {"name": "Test User 1", "email": "user1@example.com", "tier": "Premium", "value": 299},
                {"name": "Test User 2", "email": "user2@example.com", "tier": "Pro", "value": 149},
                {"name": "Test User 3", "email": "user3@example.com", "tier": "Basic+", "value": 79},
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