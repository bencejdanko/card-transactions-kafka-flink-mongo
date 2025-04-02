from kafka import KafkaConsumer
from pymongo import MongoClient
import json

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "flagged_transactions"
GROUP_ID = "flagged_transactions_consumer"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id=GROUP_ID,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "transaction_db"
COLLECTION_NAME = "flagged_transactions"

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

print(f"Listening for new messages on topic: {KAFKA_TOPIC}")

try:
    for message in consumer:
        message_value = message.value
        print(f"Received message: {message_value}")

        # Insert into MongoDB
        insert_result = collection.insert_one(message_value)
        if insert_result.acknowledged:
            print("Message stored in MongoDB with ID:", insert_result.inserted_id)
        else:
            print("Insert failed!")
        print("Message stored in MongoDB.")

except KeyboardInterrupt:
    print("Shutting down consumer...")
finally:
    consumer.close()
    mongo_client.close()
