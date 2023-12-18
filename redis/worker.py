import redis
import json
import os
import random
import time
import datetime

#Simple logging direct to a directory
def kLog(message):
    podName = os.getenv('POD_NAME')
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("/kube/home/logs/exampleRedis/" + str(podName), "a") as f:
        f.write(str(timestamp) + " --- " + str(podName) + ":" + str(message) + "\n")

# Connect to Redis
redis_host = os.getenv('REDIS_SERVICE_HOST', 'redis')
redis_port = os.getenv('REDIS_SERVICE_PORT', '6379')
# Connect to Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True, socket_timeout=10)

def process_job(redis_client, queue_name, processing_queue_name):
    job = redis_client.brpoplpush(queue_name, processing_queue_name)

    try:
        # Process the job
        kLog(f"Processing job: {job}")
        time.sleep(10)
        # Remove the job from the processing list
        redis_client.lrem(processing_queue_name, 1, job)
    except Exception as e:
        kLog(f"Error processing job: {e}")

# Process jobs
while True:
    process_job(redis_client, 'exampleQueue', 'checkoutQueue')