from faker import Faker
import time
fake = Faker()

def generate_transaction():
    return {
        "card_number": fake.credit_card_number(),
        "amount": fake.pydecimal(positive=True, min_value=1, max_value=1000, right_digits=2),
        "timestamp": fake.date_time(),  # adjust datetime format as required
        "location": {
            "city": fake.city(),
            "state": fake.state_abbr()
        },
        "merchant": fake.company(),
        "currency": fake.currency_code(),
        "device_type": fake.random_element(elements=("mobile", "desktop", "tablet"))
    }

from kafka import KafkaProducer

import json

KAFKA_TOPIC = 'test'
producer = None
producer = KafkaProducer(bootstrap_servers=f'localhost:{9092}')
producer.send(KAFKA_TOPIC, json.dumps(data).encode('utf-8'))

while True:

    transaction = generate_transaction()

    producer.send("credit_card_transactions", json.dumps(transaction).encode("utf-8"))

    producer.flush()

    time.sleep(1)  # Adjust interval as needed