"""
Exa Job Queue Manager
=====================
Purpose: Manage Exa enrichment job queue with Redis.

This module provides:
- Job enqueueing for enrichment tasks
- Scheduled job management
- Queue monitoring and stats
- Priority queue support
- Job retry logic

Usage:
    from queue.exa_queue import get_queue_manager
    
    qm = get_queue_manager()
    job_id = qm.enqueue_enrichment('microsoft.com', search_types=['careers', 'products'])
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

# Try to import Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    logger.warning("Redis not installed. Queue features will be limited.")
    REDIS_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '0'))

# Queue names
QUEUE_ENRICHMENT = 'exa_enrichment'
QUEUE_ENRICHMENT_PRIORITY = 'exa_enrichment_priority'
QUEUE_SCHEDULED = 'exa_scheduled'

# ============================================================================
# QUEUE MANAGER
# ============================================================================

class ExaQueueManager:
    """Manages Exa enrichment job queues."""
    
    def __init__(self):
        """Initialize queue manager."""
        self.redis_client = None
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    db=REDIS_DB,
                    decode_responses=True
                )
                self.redis_client.ping()
                logger.info(f"✅ Queue manager connected to Redis")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self.redis_client = None
    
    def enqueue_enrichment(
        self,
        domain: str,
        search_types: List[str] = None,
        company_name: Optional[str] = None,
        num_results: int = 5,
        use_cache: bool = True,
        priority: bool = False,
        triggered_by: str = 'api',
        metadata: Dict[str, Any] = None
    ) -> Optional[str]:
        """
        Enqueue a company enrichment job.
        
        Args:
            domain: Company domain (e.g., 'microsoft.com')
            search_types: List of search types (['careers', 'products', 'background'])
            company_name: Optional company name
            num_results: Number of results per search
            use_cache: Use cached results if available
            priority: Use priority queue
            triggered_by: Who/what triggered this job
            metadata: Additional metadata
        
        Returns:
            Job ID if enqueued successfully, None otherwise
        """
        if not self.redis_client:
            logger.error("Redis not available, cannot enqueue job")
            return None
        
        search_types = search_types or ['careers', 'products', 'background']
        
        job = {
            'job_id': str(uuid4()),
            'domain': domain,
            'company_name': company_name,
            'search_types': search_types,
            'num_results': num_results,
            'use_cache': use_cache,
            'triggered_by': triggered_by,
            'enqueued_at': datetime.now().isoformat(),
            'status': 'queued',
            'metadata': metadata or {}
        }
        
        # Choose queue
        queue_name = QUEUE_ENRICHMENT_PRIORITY if priority else QUEUE_ENRICHMENT
        
        # Enqueue
        try:
            self.redis_client.rpush(queue_name, json.dumps(job))
            
            # Store job metadata
            self.redis_client.setex(
                f"job:{job['job_id']}",
                86400,  # 24 hour TTL
                json.dumps(job)
            )
            
            logger.info(f"Enqueued job {job['job_id']} for {domain} in {queue_name}")
            return job['job_id']
        
        except Exception as e:
            logger.error(f"Failed to enqueue job: {e}")
            return None
    
    def enqueue_batch(
        self,
        domains: List[str],
        search_types: List[str] = None,
        **kwargs
    ) -> List[str]:
        """
        Enqueue multiple enrichment jobs.
        
        Args:
            domains: List of company domains
            search_types: Search types for all jobs
            **kwargs: Additional arguments passed to enqueue_enrichment
        
        Returns:
            List of job IDs
        """
        job_ids = []
        
        for domain in domains:
            job_id = self.enqueue_enrichment(
                domain=domain,
                search_types=search_types,
                **kwargs
            )
            if job_id:
                job_ids.append(job_id)
        
        logger.info(f"Enqueued batch: {len(job_ids)}/{len(domains)} jobs")
        return job_ids
    
    def schedule_enrichment(
        self,
        domain: str,
        schedule_time: datetime,
        **kwargs
    ) -> Optional[str]:
        """
        Schedule an enrichment job for future execution.
        
        Args:
            domain: Company domain
            schedule_time: When to execute the job
            **kwargs: Additional arguments passed to enqueue_enrichment
        
        Returns:
            Job ID if scheduled successfully
        """
        if not self.redis_client:
            return None
        
        job = {
            'job_id': str(uuid4()),
            'domain': domain,
            'scheduled_for': schedule_time.isoformat(),
            'scheduled_at': datetime.now().isoformat(),
            'kwargs': kwargs
        }
        
        # Add to scheduled set with score = timestamp
        score = schedule_time.timestamp()
        
        try:
            self.redis_client.zadd(
                QUEUE_SCHEDULED,
                {json.dumps(job): score}
            )
            
            logger.info(f"Scheduled job {job['job_id']} for {domain} at {schedule_time}")
            return job['job_id']
        
        except Exception as e:
            logger.error(f"Failed to schedule job: {e}")
            return None
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        if not self.redis_client:
            return {'error': 'Redis not available'}
        
        try:
            return {
                'queued': self.redis_client.llen(QUEUE_ENRICHMENT),
                'priority_queued': self.redis_client.llen(QUEUE_ENRICHMENT_PRIORITY),
                'scheduled': self.redis_client.zcard(QUEUE_SCHEDULED),
                'processing': self.redis_client.scard(f"{QUEUE_ENRICHMENT}:processing"),
                'failed': self.redis_client.scard(f"{QUEUE_ENRICHMENT}:failed"),
            }
        except Exception as e:
            logger.error(f"Failed to get queue stats: {e}")
            return {'error': str(e)}
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific job."""
        if not self.redis_client:
            return None
        
        try:
            job_json = self.redis_client.get(f"job:{job_id}")
            if job_json:
                return json.loads(job_json)
            return None
        except Exception as e:
            logger.error(f"Failed to get job status: {e}")
            return None
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a queued job."""
        if not self.redis_client:
            return False
        
        try:
            # Delete from job store
            self.redis_client.delete(f"job:{job_id}")
            logger.info(f"Cancelled job {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel job: {e}")
            return False
    
    def process_scheduled_jobs(self) -> int:
        """
        Check scheduled jobs and enqueue those ready to run.
        Should be called periodically (e.g., every minute).
        
        Returns:
            Number of jobs enqueued
        """
        if not self.redis_client:
            return 0
        
        now = time.time()
        count = 0
        
        try:
            # Get all jobs scheduled before now
            ready_jobs = self.redis_client.zrangebyscore(
                QUEUE_SCHEDULED,
                0,
                now
            )
            
            for job_json in ready_jobs:
                job = json.loads(job_json)
                
                # Enqueue the job
                job_id = self.enqueue_enrichment(
                    domain=job['domain'],
                    **job.get('kwargs', {})
                )
                
                if job_id:
                    # Remove from scheduled set
                    self.redis_client.zrem(QUEUE_SCHEDULED, job_json)
                    count += 1
            
            if count > 0:
                logger.info(f"Processed {count} scheduled jobs")
            
            return count
        
        except Exception as e:
            logger.error(f"Failed to process scheduled jobs: {e}")
            return 0
    
    def clear_queue(self, queue_name: str = QUEUE_ENRICHMENT) -> bool:
        """Clear all jobs from a queue (use with caution!)."""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(queue_name)
            logger.warning(f"Cleared queue: {queue_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear queue: {e}")
            return False

# ============================================================================
# SINGLETON
# ============================================================================

_queue_manager_instance = None

def get_queue_manager() -> ExaQueueManager:
    """Get or create ExaQueueManager singleton."""
    global _queue_manager_instance
    
    if _queue_manager_instance is None:
        _queue_manager_instance = ExaQueueManager()
    
    return _queue_manager_instance

def reset_queue_manager():
    """Reset the queue manager singleton (for testing)."""
    global _queue_manager_instance
    _queue_manager_instance = None
