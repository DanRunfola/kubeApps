import pika
import os

print("Script initialized.")

def callback(ch, method, properties, body):
    print(" [x] Received " + str(body))
    print("Deleting message with tag: " + str(method.delivery_tag))
    ch.basic_ack(delivery_tag=method.delivery_tag) #Delete the message from the queue after processing is complete.

print("Retrieving Environmental Variables.")
# Replace with your RabbitMQ service name and port.  
# These are environmental variables defined in the yml.
rabbitmq_service = os.getenv('RABBITMQ_SERVICE')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
print(rabbitmq_service)
print(rabbitmq_port)

print("Establishing Pika Connection")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_service, port=rabbitmq_port))
channel = connection.channel()

print("Declaring Queue")

channel.queue_declare(queue='exampleMessageQueue')


print("Defining Consumption Strategy")
channel.basic_consume(queue='exampleMessageQueue',
                      auto_ack=False, #Disables automatic acknowledgement (removal from queue). 
                                      #Note only one node can check out a queue item at any given time.
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()