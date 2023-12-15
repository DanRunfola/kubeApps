import pika
import os

def lo(message):
    with open("/kube/home/test", "a") as f:
        f.write(message + "\n")



lo("Script initialized.")

def callback(ch, method, properties, body):
    lo(" [x] Received " + str(body))
    lo("Deleting message with tag: " + str(method.delivery_tag))
    ch.basic_ack(delivery_tag=method.delivery_tag) #Delete the message from the queue after processing is complete.

lo("Retrieving Environmental Variables.")
# Replace with your RabbitMQ service name and port.  
# These are environmental variables defined in the yml.
rabbitmq_service = os.getenv('RABBITMQ_SERVICE')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
lo(rabbitmq_service)
lo(rabbitmq_port)

lo("Establishing Pika Connection")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_service, port=rabbitmq_port))
channel = connection.channel()

lo("Declaring Queue")

channel.queue_declare(queue='exampleMessageQueue', durable=True) #Indicate we're working with a durable queue


lo("Defining Consumption Strategy")
channel.basic_consume(queue='exampleMessageQueue',
                      auto_ack=False, #Disables automatic acknowledgement (removal from queue). 
                                      #Note only one node can check out a queue item at any given time.
                      on_message_callback=callback)

lo(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()