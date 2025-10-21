"""
SQLite Database Manager for IntelliCV AI Learning System
Provides robust database operations with fallback support
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

# Try multiple SQLite approaches
SQLITE_AVAILABLE = False
sqlite_conn = None

# Primary approach - built-in sqlite3
try:
    import sqlite3
    SQLITE_AVAILABLE = True
    sqlite_module = sqlite3
    print("✅ Using built-in sqlite3")
except ImportError:
    print("❌ Built-in sqlite3 not available")

# Fallback 1 - Alternative sqlite implementations
if not SQLITE_AVAILABLE:
    try:
        import apsw as sqlite3
        SQLITE_AVAILABLE = True
        sqlite_module = sqlite3
        print("✅ Using APSW SQLite")
    except ImportError:
        pass

# Fallback 2 - File-based storage as last resort
if not SQLITE_AVAILABLE:
    print("⚠️ SQLite not available - using file-based storage")

class IntelliCVSQLiteManager:
    """
    Comprehensive SQLite manager for AI learning system
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize SQLite manager with database path"""
        self.db_path = db_path or "ai_data_system/ai_learning/intellicv_ai_learning.db"
        self.db_directory = Path(self.db_path).parent
        self.db_directory.mkdir(parents=True, exist_ok=True)
        
        # Fallback storage for when SQLite unavailable
        self.fallback_dir = Path("ai_data_system/ai_learning/fallback_storage")
        self.fallback_dir.mkdir(parents=True, exist_ok=True)
        
        self.connection = None
        self.sqlite_available = SQLITE_AVAILABLE
        
        if self.sqlite_available:
            self._initialize_database()
        else:
            self._initialize_fallback_storage()
    
    def _initialize_database(self):
        """Initialize SQLite database with required tables"""
        try:
            self.connection = sqlite_module.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            
            # Enable WAL mode for better concurrency
            self.connection.execute("PRAGMA journal_mode=WAL")
            self.connection.execute("PRAGMA synchronous=NORMAL")
            self.connection.execute("PRAGMA cache_size=10000")
            
            self._create_tables()
            print(f"✅ SQLite database initialized: {self.db_path}")
            
        except Exception as e:
            print(f"❌ SQLite initialization failed: {e}")
            self.sqlite_available = False
            self._initialize_fallback_storage()
    
    def _initialize_fallback_storage(self):
        """Initialize file-based fallback storage"""
        self.storage_files = {
            'ai_learning': self.fallback_dir / 'ai_learning.json',
            'processing_history': self.fallback_dir / 'processing_history.json',
            'model_performance': self.fallback_dir / 'model_performance.json',
            'system_metrics': self.fallback_dir / 'system_metrics.json'
        }
        
        # Initialize empty files if they don't exist
        for file_path in self.storage_files.values():
            if not file_path.exists():
                file_path.write_text(json.dumps([], indent=2))
        
        print("✅ Fallback file storage initialized")
    
    def _create_tables(self):
        """Create all required database tables"""
        
        # AI Learning Results Table
        create_ai_learning = """
        CREATE TABLE IF NOT EXISTS ai_learning_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT NOT NULL,
            processing_mode TEXT NOT NULL,
            input_type TEXT NOT NULL,
            bayesian_confidence REAL,
            nlp_sentiment REAL,
            fuzzy_logic_score REAL,
            llm_coherence REAL,
            combined_score REAL,
            processing_time REAL,
            data_size INTEGER,
            model_version TEXT,
            feedback_rating INTEGER,
            user_corrections TEXT,
            raw_input_hash TEXT,
            processed_output_hash TEXT,
            error_messages TEXT,
            metadata TEXT
        )
        """
        
        # Processing History Table
        create_processing_history = """
        CREATE TABLE IF NOT EXISTS processing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT,
            operation_type TEXT NOT NULL,
            input_files INTEGER DEFAULT 0,
            processed_files INTEGER DEFAULT 0,
            failed_files INTEGER DEFAULT 0,
            total_processing_time REAL,
            average_confidence REAL,
            status TEXT NOT NULL,
            configuration TEXT,
            results_summary TEXT
        )
        """
        
        # Model Performance Tracking
        create_model_performance = """
        CREATE TABLE IF NOT EXISTS model_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_type TEXT NOT NULL,
            accuracy_score REAL,
            precision_score REAL,
            recall_score REAL,
            f1_score REAL,
            processing_speed REAL,
            memory_usage REAL,
            training_data_size INTEGER,
            test_data_size INTEGER,
            hyperparameters TEXT,
            performance_notes TEXT
        )
        """
        
        # System Metrics Table
        create_system_metrics = """
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            active_sessions INTEGER,
            queue_length INTEGER,
            response_time REAL,
            error_rate REAL,
            throughput REAL,
            system_health TEXT
        )
        """
        
        tables = [
            create_ai_learning,
            create_processing_history,
            create_model_performance,
            create_system_metrics
        ]
        
        for table_sql in tables:
            self.connection.execute(table_sql)
        
        self.connection.commit()
        print("✅ Database tables created successfully")
    
    def save_ai_learning_result(self, result_data: Dict[str, Any]) -> bool:
        """Save AI learning result to database or fallback storage"""
        
        if self.sqlite_available and self.connection:
            return self._save_to_sqlite('ai_learning_results', result_data)
        else:
            return self._save_to_fallback('ai_learning', result_data)
    
    def save_processing_history(self, history_data: Dict[str, Any]) -> bool:
        """Save processing history"""
        
        if self.sqlite_available and self.connection:
            return self._save_to_sqlite('processing_history', history_data)
        else:
            return self._save_to_fallback('processing_history', history_data)
    
    def save_model_performance(self, performance_data: Dict[str, Any]) -> bool:
        """Save model performance metrics"""
        
        if self.sqlite_available and self.connection:
            return self._save_to_sqlite('model_performance', performance_data)
        else:
            return self._save_to_fallback('model_performance', performance_data)
    
    def save_system_metrics(self, metrics_data: Dict[str, Any]) -> bool:
        """Save system metrics"""
        
        if self.sqlite_available and self.connection:
            return self._save_to_sqlite('system_metrics', metrics_data)
        else:
            return self._save_to_fallback('system_metrics', metrics_data)
    
    def _save_to_sqlite(self, table_name: str, data: Dict[str, Any]) -> bool:
        """Save data to SQLite table"""
        try:
            # Prepare column names and placeholders
            columns = list(data.keys())
            placeholders = ['?' for _ in columns]
            values = list(data.values())
            
            sql = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
            """
            
            self.connection.execute(sql, values)
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ SQLite save error: {e}")
            return False
    
    def _save_to_fallback(self, storage_key: str, data: Dict[str, Any]) -> bool:
        """Save data to fallback file storage"""
        try:
            file_path = self.storage_files[storage_key]
            
            # Load existing data
            existing_data = json.loads(file_path.read_text())
            
            # Add timestamp if not present
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().isoformat()
            
            # Add new data
            existing_data.append(data)
            
            # Keep only last 1000 records to prevent unlimited growth
            if len(existing_data) > 1000:
                existing_data = existing_data[-1000:]
            
            # Save back to file
            file_path.write_text(json.dumps(existing_data, indent=2))
            return True
            
        except Exception as e:
            print(f"❌ Fallback save error: {e}")
            return False
    
    def get_ai_learning_stats(self) -> Dict[str, Any]:
        """Get AI learning statistics"""
        
        if self.sqlite_available and self.connection:
            return self._get_sqlite_stats()
        else:
            return self._get_fallback_stats()
    
    def _get_sqlite_stats(self) -> Dict[str, Any]:
        """Get statistics from SQLite database"""
        try:
            cursor = self.connection.cursor()
            
            # Basic counts
            cursor.execute("SELECT COUNT(*) FROM ai_learning_results")
            total_records = cursor.fetchone()[0]
            
            # Average scores
            cursor.execute("""
                SELECT 
                    AVG(bayesian_confidence),
                    AVG(nlp_sentiment),
                    AVG(fuzzy_logic_score),
                    AVG(llm_coherence),
                    AVG(combined_score)
                FROM ai_learning_results
                WHERE bayesian_confidence IS NOT NULL
            """)
            
            avg_scores = cursor.fetchone()
            
            # Recent activity
            cursor.execute("""
                SELECT COUNT(*) FROM ai_learning_results 
                WHERE timestamp > datetime('now', '-24 hours')
            """)
            recent_activity = cursor.fetchone()[0]
            
            return {
                'total_records': total_records,
                'average_bayesian_confidence': avg_scores[0] or 0,
                'average_nlp_sentiment': avg_scores[1] or 0,
                'average_fuzzy_logic_score': avg_scores[2] or 0,
                'average_llm_coherence': avg_scores[3] or 0,
                'average_combined_score': avg_scores[4] or 0,
                'recent_activity_24h': recent_activity,
                'database_type': 'SQLite'
            }
            
        except Exception as e:
            print(f"❌ SQLite stats error: {e}")
            return {'error': str(e), 'database_type': 'SQLite (Error)'}
    
    def _get_fallback_stats(self) -> Dict[str, Any]:
        """Get statistics from fallback storage"""
        try:
            ai_learning_data = json.loads(self.storage_files['ai_learning'].read_text())
            
            total_records = len(ai_learning_data)
            
            if total_records == 0:
                return {
                    'total_records': 0,
                    'database_type': 'File Storage'
                }
            
            # Calculate averages
            scores = {
                'bayesian_confidence': [],
                'nlp_sentiment': [],
                'fuzzy_logic_score': [],
                'llm_coherence': [],
                'combined_score': []
            }
            
            for record in ai_learning_data:
                for key in scores.keys():
                    if key in record and record[key] is not None:
                        scores[key].append(float(record[key]))
            
            return {
                'total_records': total_records,
                'average_bayesian_confidence': sum(scores['bayesian_confidence']) / len(scores['bayesian_confidence']) if scores['bayesian_confidence'] else 0,
                'average_nlp_sentiment': sum(scores['nlp_sentiment']) / len(scores['nlp_sentiment']) if scores['nlp_sentiment'] else 0,
                'average_fuzzy_logic_score': sum(scores['fuzzy_logic_score']) / len(scores['fuzzy_logic_score']) if scores['fuzzy_logic_score'] else 0,
                'average_llm_coherence': sum(scores['llm_coherence']) / len(scores['llm_coherence']) if scores['llm_coherence'] else 0,
                'average_combined_score': sum(scores['combined_score']) / len(scores['combined_score']) if scores['combined_score'] else 0,
                'database_type': 'File Storage'
            }
            
        except Exception as e:
            print(f"❌ Fallback stats error: {e}")
            return {'error': str(e), 'database_type': 'File Storage (Error)'}
    
    def get_recent_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent AI learning results"""
        
        if self.sqlite_available and self.connection:
            return self._get_sqlite_recent_results(limit)
        else:
            return self._get_fallback_recent_results(limit)
    
    def _get_sqlite_recent_results(self, limit: int) -> List[Dict[str, Any]]:
        """Get recent results from SQLite"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM ai_learning_results 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
            
        except Exception as e:
            print(f"❌ SQLite recent results error: {e}")
            return []
    
    def _get_fallback_recent_results(self, limit: int) -> List[Dict[str, Any]]:
        """Get recent results from fallback storage"""
        try:
            ai_learning_data = json.loads(self.storage_files['ai_learning'].read_text())
            
            # Sort by timestamp (most recent first) and limit
            sorted_data = sorted(
                ai_learning_data,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )
            
            return sorted_data[:limit]
            
        except Exception as e:
            print(f"❌ Fallback recent results error: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

# Global instance for easy access
_sqlite_manager = None

def get_sqlite_manager() -> IntelliCVSQLiteManager:
    """Get global SQLite manager instance"""
    global _sqlite_manager
    if _sqlite_manager is None:
        _sqlite_manager = IntelliCVSQLiteManager()
    return _sqlite_manager

def test_sqlite_functionality():
    """Test SQLite functionality with sample data"""
    manager = get_sqlite_manager()
    
    # Test data
    test_result = {
        'session_id': 'test_session_001',
        'processing_mode': 'medium',
        'input_type': 'cv_document',
        'bayesian_confidence': 0.85,
        'nlp_sentiment': 0.72,
        'fuzzy_logic_score': 0.91,
        'llm_coherence': 0.88,
        'combined_score': 0.84,
        'processing_time': 1.23,
        'data_size': 1024,
        'model_version': 'v2.1.0',
        'metadata': json.dumps({'test': True})
    }
    
    # Save test result
    if manager.save_ai_learning_result(test_result):
        print("✅ Test data saved successfully")
    else:
        print("❌ Test data save failed")
    
    # Get stats
    stats = manager.get_ai_learning_stats()
    print(f"📊 Database stats: {stats}")
    
    # Get recent results
    recent = manager.get_recent_results(5)
    print(f"📋 Recent results: {len(recent)} records")
    
    return manager

if __name__ == "__main__":
    test_sqlite_functionality()