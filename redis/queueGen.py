import redis
import json
import os
import random
# Connect to Redis
redis_host = os.getenv('REDIS_SERVICE_HOST', 'localhost')
redis_port = os.getenv('REDIS_SERVICE_PORT', 6379)
r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def enqueue_job(queue_name, job_data):
    """Enqueue a job into the Redis queue."""
    r.lpush(queue_name, json.dumps(job_data))

# Example usage
for i in range(0,100):
    param = random.random()
    enqueue_job('exampleQueue', {'ID': str(i), 'parameters': str(param)})
    print("Queued job ID: " + str(i))