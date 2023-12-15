import pika
import os
import random

def on_delivery_confirmation(method_frame):
    confirmation_type = method_frame.method.NAME.split('.')[1].lower()
    print(f"Received {confirmation_type} for delivery tag: {method_frame.method.delivery_tag}")
    if confirmation_type == 'ack':
        print(f"Message acknowledged by RabbitMQ")
    elif confirmation_type == 'nack':
        print(f"Message not acknowledged by RabbitMQ")

# Replace with your RabbitMQ service name and port
rabbitmq_service = os.getenv('RABBITMQ_SERVICE')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
print(rabbitmq_service)
print(rabbitmq_port)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_service, port=rabbitmq_port))
channel = connection.channel()
channel.confirm_delivery()

#Durable ensures that RMQ retains the message until a worker node has received it,
#even across restarts of the RMQ server.
channel.queue_declare(queue='exampleMessageQueue', durable=True)
channel.add_on_confirmation_callback(on_delivery_confirmation)

#Create 100 messages, each with a different parameter set:
for i in range(0,100):
    parameter = str(random.random())
    runID = str(i)
    channel.basic_publish(
        exchange='',
        routing_key='exampleMessageQueue',
        body='RUNID_'+runID+":"+parameter,
        properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
        mandatory=True  # message must be routed to a queue
    )
        
channel.wait_for_confirms()
connection.close()