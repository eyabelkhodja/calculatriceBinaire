import socket
import hashlib
from simulate_network import simulate_network

def clean_input(L):
    return [x.strip().replace("[", "").replace("]", "") for x in L]

def read_input():
    while True:
        try:
            L = input("Entrez l'opération [operation, operand1, operand2, result]: ").split(",")
            if len(L) != 4:
                raise ValueError("4 éléments attendus.")
            if not L[1].startswith("0b"):
                raise ValueError("Opérande 1 doit être en binaire.")
            if L[2] and not L[2].startswith("0b"):
                raise ValueError("Opérande 2 doit être en binaire ou vide.")
            return clean_input(L)
        except ValueError as e:
            print(e)

def menu():
    print("\n--- Menu ---")
    print("OR | AND | XOR | LS | RS | INVERT (~ uses only operand1)")
    print("Type EXIT to quit.\n")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (socket.gethostname(), 1234)

while True:
    menu()
    L = read_input()
    if L[0].upper() == "EXIT":
        break

    try:
        payload = ",".join(L)
        checksum = hashlib.md5(payload.encode("utf-8")).hexdigest()
        full_data = f"{payload},{checksum}"

        corrupted_data = simulate_network(full_data, error_probability=1)  # Set to 0.1 to test errors
        print(f"Sending: {corrupted_data}")
        s.sendto(corrupted_data.encode("utf-8"), server_addr)

        response, _ = s.recvfrom(1024)
        print("🛰️  Server response:", response.decode("utf-8"))
    except Exception as e:
        print("❌ Client error:", e)

s.close()
