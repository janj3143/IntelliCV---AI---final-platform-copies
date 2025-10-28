"""
Exa Background Worker
=====================
Purpose: Process Exa enrichment jobs from Redis queue in the background.

This worker:
- Polls Redis queue for enrichment jobs
- Processes company enrichment automatically
- Stores results in database and corpus
- Logs metrics and errors
- Supports scheduled and on-demand crawls

Usage:
    python exa_worker.py --queue exa_enrichment --workers 2
"""

import os
import sys
import time
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import signal

# Add shared_backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.exa_service.company_enrichment import get_company_enricher
from database.exa_db import (
    create_company_crawl,
    update_crawl_status,
    save_company_source,
    log_api_usage
)

# Try to import Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    print("⚠️  Redis not installed. Install with: pip install redis")
    REDIS_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '0'))
REDIS_QUEUE = os.getenv('EXA_QUEUE_NAME', 'exa_enrichment')

WORKER_ID = os.getenv('WORKER_ID', f"worker_{os.getpid()}")
POLL_INTERVAL = int(os.getenv('WORKER_POLL_INTERVAL', '5'))  # seconds
MAX_RETRIES = int(os.getenv('WORKER_MAX_RETRIES', '3'))

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ExaWorker')

# ============================================================================
# REDIS QUEUE CLIENT
# ============================================================================

class RedisQueue:
    """Simple Redis queue for job management."""
    
    def __init__(self, queue_name: str, redis_client):
        self.queue_name = queue_name
        self.redis = redis_client
        self.processing_set = f"{queue_name}:processing"
        self.failed_set = f"{queue_name}:failed"
    
    def enqueue(self, job_data: Dict[str, Any]) -> str:
        """Add a job to the queue."""
        job_id = f"job_{int(time.time() * 1000)}"
        job_data['job_id'] = job_id
        job_data['enqueued_at'] = datetime.now().isoformat()
        
        self.redis.rpush(self.queue_name, json.dumps(job_data))
        logger.info(f"Enqueued job: {job_id}")
        return job_id
    
    def dequeue(self, timeout: int = 0) -> Optional[Dict[str, Any]]:
        """Get next job from queue (blocking)."""
        result = self.redis.blpop(self.queue_name, timeout=timeout)
        
        if result:
            _, job_json = result
            job_data = json.loads(job_json)
            
            # Mark as processing
            self.redis.sadd(self.processing_set, job_data['job_id'])
            
            return job_data
        
        return None
    
    def complete(self, job_id: str):
        """Mark job as completed."""
        self.redis.srem(self.processing_set, job_id)
    
    def fail(self, job_id: str, error: str):
        """Mark job as failed."""
        self.redis.srem(self.processing_set, job_id)
        self.redis.sadd(self.failed_set, json.dumps({
            'job_id': job_id,
            'error': error,
            'failed_at': datetime.now().isoformat()
        }))
    
    def get_stats(self) -> Dict[str, int]:
        """Get queue statistics."""
        return {
            'queued': self.redis.llen(self.queue_name),
            'processing': self.redis.scard(self.processing_set),
            'failed': self.redis.scard(self.failed_set)
        }

# ============================================================================
# WORKER
# ============================================================================

class ExaWorker:
    """Background worker for Exa enrichment jobs."""
    
    def __init__(self, worker_id: str, queue: RedisQueue):
        self.worker_id = worker_id
        self.queue = queue
        self.enricher = get_company_enricher()
        self.is_running = False
        self.jobs_processed = 0
        self.jobs_failed = 0
        
        logger.info(f"Worker {worker_id} initialized")
    
    def process_job(self, job: Dict[str, Any]) -> bool:
        """
        Process a single enrichment job.
        
        Args:
            job: Job data dictionary with 'domain', 'search_types', etc.
        
        Returns:
            True if successful, False otherwise
        """
        job_id = job.get('job_id', 'unknown')
        domain = job.get('domain')
        search_types = job.get('search_types', ['careers', 'products', 'background'])
        
        logger.info(f"Processing job {job_id}: {domain}")
        
        # Create crawl record
        try:
            crawl_id = create_company_crawl(
                domain=domain,
                crawl_type='auto' if job.get('scheduled') else 'manual',
                search_types=search_types,
                triggered_by=job.get('triggered_by', 'background_worker'),
                triggered_from='exa_worker',
                company_name=job.get('company_name')
            )
            
            # Update status to running
            update_crawl_status(crawl_id, 'running')
            
            start_time = time.time()
            total_pages = 0
            api_calls = 0
            
            # Perform enrichment
            results = {
                'careers': None,
                'products': None,
                'background': None
            }
            
            if 'careers' in search_types:
                logger.info(f"Searching careers pages for {domain}")
                results['careers'] = self.enricher.find_careers_pages(
                    domain=domain,
                    num_results=job.get('num_results', 5),
                    use_cache=job.get('use_cache', True)
                )
                total_pages += results['careers'].get('total_found', 0)
                api_calls += 1 if not results['careers'].get('from_cache') else 0
            
            if 'products' in search_types:
                logger.info(f"Searching product pages for {domain}")
                results['products'] = self.enricher.find_product_pages(
                    domain=domain,
                    num_results=job.get('num_results', 5),
                    use_cache=job.get('use_cache', True)
                )
                total_pages += results['products'].get('total_found', 0)
                api_calls += 1 if not results['products'].get('from_cache') else 0
            
            if 'background' in search_types:
                logger.info(f"Searching background for {domain}")
                results['background'] = self.enricher.get_company_background(
                    domain=domain,
                    num_results=job.get('num_results', 5),
                    use_cache=job.get('use_cache', True)
                )
                total_pages += results['background'].get('total_found', 0)
                api_calls += 1 if not results['background'].get('from_cache') else 0
            
            duration = int(time.time() - start_time)
            
            # Update crawl status
            update_crawl_status(
                crawl_id,
                'completed',
                total_pages_found=total_pages,
                careers_pages_found=results['careers'].get('total_found', 0) if results['careers'] else 0,
                products_pages_found=results['products'].get('total_found', 0) if results['products'] else 0,
                background_pages_found=results['background'].get('total_found', 0) if results['background'] else 0,
                duration_seconds=duration,
                api_calls_made=api_calls
            )
            
            logger.info(f"✅ Job {job_id} completed: {total_pages} pages, {duration}s")
            self.jobs_processed += 1
            return True
        
        except Exception as e:
            logger.error(f"❌ Job {job_id} failed: {e}")
            
            # Update crawl as failed
            try:
                update_crawl_status(
                    crawl_id,
                    'failed',
                    error_message=str(e)
                )
            except:
                pass
            
            self.jobs_failed += 1
            return False
    
    def start(self):
        """Start the worker (blocking)."""
        self.is_running = True
        logger.info(f"Worker {self.worker_id} starting...")
        
        # Graceful shutdown handler
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Main loop
        while self.is_running:
            try:
                # Get next job (blocking with timeout)
                job = self.queue.dequeue(timeout=POLL_INTERVAL)
                
                if job:
                    success = self.process_job(job)
                    
                    if success:
                        self.queue.complete(job['job_id'])
                    else:
                        self.queue.fail(job['job_id'], "Processing failed")
                
                else:
                    # No jobs, wait a bit
                    time.sleep(1)
            
            except Exception as e:
                logger.error(f"Worker error: {e}")
                time.sleep(5)  # Back off on error
        
        logger.info(f"Worker {self.worker_id} stopped. Processed: {self.jobs_processed}, Failed: {self.jobs_failed}")
    
    def stop(self):
        """Stop the worker."""
        self.is_running = False

# ============================================================================
# CLI
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Exa Background Worker")
    parser.add_argument('--queue', default=REDIS_QUEUE, help='Redis queue name')
    parser.add_argument('--worker-id', default=WORKER_ID, help='Worker ID')
    parser.add_argument('--poll-interval', type=int, default=POLL_INTERVAL, help='Poll interval in seconds')
    
    args = parser.parse_args()
    
    if not REDIS_AVAILABLE:
        logger.error("Redis is not available. Install with: pip install redis")
        sys.exit(1)
    
    # Connect to Redis
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
        redis_client.ping()
        logger.info(f"✅ Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Redis: {e}")
        sys.exit(1)
    
    # Create queue
    queue = RedisQueue(args.queue, redis_client)
    
    # Show stats
    stats = queue.get_stats()
    logger.info(f"Queue stats: {stats}")
    
    # Create and start worker
    worker = ExaWorker(args.worker_id, queue)
    
    logger.info("="*70)
    logger.info(f"EXA WORKER STARTING")
    logger.info(f"Worker ID: {args.worker_id}")
    logger.info(f"Queue: {args.queue}")
    logger.info(f"Poll Interval: {args.poll_interval}s")
    logger.info("="*70)
    
    try:
        worker.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        worker.stop()

if __name__ == "__main__":
    main()
