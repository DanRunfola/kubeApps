import redis
import json
import os
import random

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
            print(f"Attempt {retry_count + 1} to connect to Redis...")
            return redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True, socket_timeout=10)
        except redis.exceptions.ConnectionError as e:
            print(f"Connection failed: {e}")
            time.sleep(delay)
            retry_count += 1

    print(f"Failed to connect to Redis after {max_retries} attempts.")
    return None

def enqueue_job(queue_name, job_data):
    """Enqueue a job into the Redis queue."""
    r.lpush(queue_name, json.dumps(job_data))

# Connect to Redis
redis_host = os.getenv('REDIS_SERVICE_HOST', 'localhost')
redis_port = os.getenv('REDIS_SERVICE_PORT', 6379)
r = connect_to_redis_with_retry(redis_host, redis_port)

# Example usage
for i in range(0,100):
    param = random.random()
    enqueue_job('exampleQueue', {'ID': str(i), 'parameters': str(param)})
    print("Queued job ID: " + str(i))