import random

def simulate_network(data: str, error_probability: float = 0.1) -> str:
    data_bits = list(data)
    for i in range(len(data_bits)):
        if random.random() < error_probability:
            data_bits[i] = chr(ord(data_bits[i]) ^ 1)
    return ''.join(data_bits)
