import pika
import os

# Replace with your RabbitMQ service name and port
rabbitmq_service = os.getenv('RABBITMQ_SERVICE')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
print(rabbitmq_service)
print(rabbitmq_port)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_service, port=rabbitmq_port))
channel = connection.channel()

#Durable ensures that RMQ retains the message until a worker node has received it,
#even across restarts of the RMQ server.
channel.queue_declare(queue='exampleMessageQueue', durable=True)

channel.basic_publish(
    exchange='',
    routing_key='exampleMessageQueue',
    body='RUNID_01:1,0,10,200,10,20,30',
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))

print(" [x] Sent Message to RMQ Server, into queue exampleMessageQueue.")

connection.close()