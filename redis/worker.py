import redis
import json
import os
import random
import time

# Connect to Redis
redis_host = os.getenv('REDIS_SERVICE_HOST', 'localhost')
redis_port = os.getenv('REDIS_SERVICE_PORT', 6379)
# Connect to Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def process_job(redis_client, queue_name, processing_queue_name):
    job = redis_client.brpoplpush(queue_name, processing_queue_name)

    try:
        # Process the job
        print(f"Processing job: {job}")
        time.sleep(10)
        # Remove the job from the processing list
        redis_client.lrem(processing_queue_name, 1, job)
    except Exception as e:
        print(f"Error processing job: {e}")

# Process jobs
while True:
    process_job(redis_client, 'myexampleQueue', 'checkoutQueue')