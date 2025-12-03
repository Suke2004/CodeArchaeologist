"""
Celery application configuration for background task processing.
"""

import os
from celery import Celery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis URL from environment
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Create Celery app
celery_app = Celery(
    'codearchaeologist',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['tasks.analysis_tasks']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=1800,  # 30 minutes max
    task_soft_time_limit=1500,  # 25 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

# Task routes
celery_app.conf.task_routes = {
    'tasks.analysis_tasks.analyze_repository_task': {'queue': 'analysis'},
}

if __name__ == '__main__':
    celery_app.start()
