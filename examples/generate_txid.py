# generate_txid.py

import random
import string


def generate_txid():
    """Generates txid code for testing purposes."""
    length = random.randint(26, 35)
    characters = string.ascii_letters + string.digits
    txid = "".join(random.choice(characters) for _ in range(length))
    return txid


for i in range(5):
    txid_string = generate_txid()
    print(f"\t{i+1}. {txid_string}")
