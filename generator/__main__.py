from faker import Faker

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

if __name__ == "__main__":
    transaction = generate_transaction()
    print(transaction)