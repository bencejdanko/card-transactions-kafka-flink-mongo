from faker import Faker
import time
import random
import datetime
from kafka import KafkaProducer
import json

fake = Faker()
KAFKA_TOPIC = "credit_card_transactions"
producer = KafkaProducer(bootstrap_servers=f"localhost:9092")

stored_card_numbers = [fake.credit_card_number() for _ in range(10)]
stored_merchants = [fake.company() for _ in range(10)]

def generate_transaction():
    base_time = datetime.datetime.now()  
    jitter = datetime.timedelta(seconds=random.uniform(0, 2))

    return {
        "card_number": random.choice(stored_card_numbers) if random.random() < 0.5 else fake.credit_card_number(),
        "amount": str(fake.pydecimal(positive=True, min_value=1, max_value=1000, right_digits=2)),
        "event_time": (base_time + jitter).isoformat(timespec='milliseconds'),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "merchant": random.choice(stored_merchants) if random.random() < 0.5 else fake.company(),
        "currency": fake.currency_code(),
        "device_type": fake.random_element(elements=("mobile", "desktop", "tablet"))
    }

while True:
    transaction = generate_transaction()
    print(transaction)

    producer.send(KAFKA_TOPIC, json.dumps(transaction).encode("utf-8"))
    producer.flush()

    time.sleep(1)
