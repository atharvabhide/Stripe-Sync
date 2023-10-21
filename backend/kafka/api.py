from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Query
from pydantic import BaseModel
from confluent_kafka import Producer
import stripe
import uvicorn
import json
from dotenv import load_dotenv
import os
load_dotenv()

stripe.api_key = os.getenv('STRIPE_API_KEY')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

producer_conf = {
    'bootstrap.servers': os.getenv('KAFKA_HOST'),
    'client.id': 'stripe-customer',
}
producer = Producer(producer_conf)

class StripeEvent(BaseModel):
    type: str
    data: dict

@app.post("/stripe-webhook", status_code=status.HTTP_200_OK)
def stripe_webhook(event: StripeEvent):
    '''
    Stripe webhook endpoint
    This endpoint receives events from Stripe and publishes them to Kafka

    Parameters:
        event (StripeEvent): The Stripe event

    Returns:
        dict: A JSON response with a status message
    '''
    try:
        event_type = event.type
        event_data = event.data

        message = {
            'event': event_type,
            'data': event_data,
            'source': 'stripe-customer',
        }
        producer.produce('stripe-events', value=json.dumps(message).encode('utf-8'))
        producer.flush()

        return {"status": "Webhook received and processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)