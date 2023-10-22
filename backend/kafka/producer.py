from confluent_kafka import (
    Producer, KafkaError
)
import json
from dotenv import load_dotenv
import os

load_dotenv()

conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = Producer(conf)

def publish_customer_event(event_type, data):
    '''
    Publish a customer event
    '''
    try:
        message = {
            'event': event_type,
            'data': data,
            'source': 'fastapi-customer',
        }
        producer.produce('customer', json.dumps(message).encode('utf-8'))
        producer.flush()
    except Exception as e:
        raise e

def publish_customer_created(customer):
    '''
    Publish a customer created event
    '''
    data = {
        'id': customer['id'],
        'name': customer['name'],
        'email': customer['email'],
        'created_at': customer['created_at'],
        'updated_at': customer['updated_at']
    }
    publish_customer_event('customer_created', data)

def publish_customer_updated(customer):
    '''
    Publish a customer updated event
    '''
    data = {
        'id': customer['id'],
        'name': customer['name'],
        'email': customer['email'],
        'created_at': customer['created_at'],
        'updated_at': customer['updated_at']
    }
    publish_customer_event('customer_updated', data)

def publish_customer_deleted(customer_id):
    '''
    Publish a customer deleted event
    '''
    data = customer_id
    publish_customer_event('customer_deleted', data)
