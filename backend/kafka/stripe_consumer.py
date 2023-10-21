from confluent_kafka import (
    Consumer, KafkaError
)
import json
import stripe
import requests
from dotenv import load_dotenv
import os
load_dotenv()

stripe.api_key = os.getenv('STRIPE_API_KEY')

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'stripe-consumer-group',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['stripe-events'])

def get_existing_customer(customer_email: str):
    '''
    Get existing customer from the local system

    Parameters:
    ----------
    customer_email : str
        Customer email

    Returns:
    -------
    str
        Customer ID
    '''
    try:
        response = requests.get(f"http://127.0.0.1:8080/get_id/{customer_email}", headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            customer_id = response.json()['id']
        else:
            customer_id = None
        return customer_id
    except Exception as e:
        return None

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
        source = message_data['source']

        if event_type == 'customer.created':
            try:
                if source == 'stripe-customer':
                    customer_data = {
                        'id': data['object']['id'],
                        'name': data['object']['name'],
                        'email': data['object']['email']
                    }
                    customer_id = get_existing_customer(data['object']['email'])
                    if customer_id:
                        print("Customer already exists in the local system")
                    else:
                        response = requests.post('http://127.0.0.1:8080/customers/', json=customer_data, headers={'Content-Type': 'application/json'})
                        if response.status_code == 201:
                            print("Customer created in the local system")
            except Exception as e:
                print("Error creating customer in the local system", e)

        elif event_type == 'customer.updated':
            try:
                if source == 'stripe-customer':
                    customer_data = {
                        'name': data['object']['name'],
                        'email': data['object']['email']
                    }
                    customer_email = data['object']['email']
                    customer_id = data['object']['id']
                    response = requests.put(f'http://127.0.0.1:8080/customers/{customer_id}', json=customer_data, headers={'Content-Type': 'application/json'})
                    if response.status_code == 200:
                        print("Customer updated in the local system")
                    else:
                        print("Error updating customer in the local system", response.json())
            except Exception as e:
                print("Error updating customer in the local system", str(e))

        elif event_type == 'customer.deleted':
            try:
                if source == 'stripe-customer':
                    customer_email = data['object']['email']
                    customer_id = get_existing_customer(customer_email)
                    if not customer_id:
                        print("Customer does not exist in the local system")
                    else:
                        response = requests.delete(f'http://127.0.0.1:8080/customers/{customer_id}', headers={'Content-Type': 'application/json'})
                        if response.status_code == 204:
                            print("Customer deleted from the local system")
                        else:
                            print("Error deleting customer from the local system")
            except Exception as e:
                print("Error deleting customer from the local system", str(e))