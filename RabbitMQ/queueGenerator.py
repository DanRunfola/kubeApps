import pika
import os

# Replace with your RabbitMQ service name and port
rabbitmq_service = os.getenv('RABBITMQ_SERVICE', 'rabbitmq')
rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_service, port=rabbitmq_port))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()