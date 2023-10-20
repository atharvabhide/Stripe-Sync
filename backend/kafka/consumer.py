from confluent_kafka import Consumer, KafkaError
import json
import stripe
from dotenv import load_dotenv
import os
load_dotenv()

stripe.api_key = os.getenv('STRIPE_API_KEY')

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'customer-group',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['customer'])

while True:
    message = consumer.poll(1.0)

    if message is None:
        continue
    if message.error():
        if message.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of topic/partition.')
        else:
            print('Error while consuming: {}'.format(message.error()))
    else:
        print('Received message: {}'.format(message.value().decode('utf-8')))

        # Based on the message, perform customer creation or deletion or update
        message_data = json.loads(message.value())
        event_type = message_data['event']
        data = message_data['data']

        if event_type == 'customer_created':
            try:
                customer = stripe.Customer.create(
                    id=data['id'],
                    name=data['name'],
                    email=data['email'],
                    metadata={
                        'created_at': data['created_at'],
                        'updated_at': data['updated_at']
                    }
                )
                print("Customer created", customer)
            except stripe.error.StripeError as e:
                print("Error creating customer", str(e))

        elif event_type == 'customer_updated':
            try:
                stripe_customer = stripe.Customer.retrieve(data['id'])
                stripe_customer.name = data['name']
                stripe_customer.email = data['email']
                stripe_customer.metadata = {
                    'created_at': data['created_at'],
                    'updated_at': data['updated_at']
                }
                stripe_customer.save()
                print("Customer updated", stripe_customer)
            except stripe.error.StripeError as e:
                print("Error updating customer", str(e))

        elif event_type == 'customer_deleted':
            try:
                stripe_customer = stripe.Customer.retrieve(data['id']['id'])
                stripe_customer.delete()
                print("Customer deleted", stripe_customer)
            except stripe.error.StripeError as e:
                print("Error deleting customer", str(e))