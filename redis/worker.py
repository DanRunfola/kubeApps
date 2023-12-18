import redis
import json
import os
import random
import time
from datetime import datetime

#Simple logging direct to a directory
def kLog(message):
    podName = os.getenv('POD_NAME')
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("/kube/home/logs/exampleRedis/" + str(podName), "a") as f:
        f.write(str(timestamp) + " --- " + str(podName) + ":" + str(message) + "\n")

#Connection logic
def connect_to_redis_with_retry(redis_host, redis_port, max_retries=5, delay=2):
    """
    Try to connect to Redis with a specified number of retries.

    :param redis_host: Hostname of the Redis server
    :param redis_port: Port number of the Redis server
    :param max_retries: Maximum number of connection attempts
    :param delay: Delay between retries in seconds
    :return: Redis connection object or None
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            kLog("Attempt " + str(retry_count + 1) + " to connect to Redis...")
            return redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True, socket_timeout=10)
        except redis.exceptions.ConnectionError as e:
            kLog("Connection failed: " + str(e))
            time.sleep(delay)
            retry_count += 1

    kLog("Failed to connect to Redis after all retries.")
    return None

redis_host = os.getenv('REDIS_SERVICE_HOST', 'redis')
redis_port = os.getenv('REDIS_SERVICE_PORT', '6379')

# Connect to Redis
redis_client = connect_to_redis_with_retry(redis_host, redis_port)

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