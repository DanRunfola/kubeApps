import pika
import os
import random

# Replace with your RabbitMQ service name and port
rabbitmq_service = os.getenv('RABBITMQ_SERVICE')
rabbitmq_port = os.getenv('RABBITMQ_PORT')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_service, port=rabbitmq_port))
channel = connection.channel()
channel.confirm_delivery()

channel.queue_declare(queue='exampleMessageQueue', durable=True)

for i in range(0, 100):
    parameter = str(random.random())
    runID = str(i)
    try:
        channel.basic_publish(
            exchange='',
            routing_key='exampleMessageQueue',
            body='RUNID_' + runID + ":" + parameter,
            properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
            mandatory=True  # message must be routed to a queue
        )
        print(f"RUNID {runID}: Message published successfully")
    except pika.exceptions.UnroutableError:
        print(f"RUNID {runID}: Message could not be routed to any queue")
    except pika.exceptions.ChannelClosedByBroker:
        print(f"RUNID {runID}: Channel closed by broker")
    except Exception as e:
        print(f"RUNID {runID}: An error occurred: {e}")

connection.close()