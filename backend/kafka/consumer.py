from confluent_kafka import Consumer, KafkaError

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
