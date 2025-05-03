import socket
import hashlib

def calculate_operation(op, op1, op2=None):
    op1 = int(op1, 2)
    if op2:
        op2 = int(op2, 2)

    operations = {
        "AND": op1 & op2,
        "OR": op1 | op2,
        "XOR": op1 ^ op2,
        "LS": op1 << op2,
        "RS": op1 >> op2,
        "INVERT": ~op1,
    }

    result = operations.get(op.upper(), "Invalid operation")
    if isinstance(result, int):
        return bin(result) if result >= 0 else f"-0b{bin(abs(result))[2:]}"
    return result

def verify_checksum(data: str) -> tuple[bool, str]:
    try:
        payload, received_checksum = data.rsplit(",", 1)
        calculated_checksum = hashlib.md5(payload.encode("utf-8")).hexdigest()
        return calculated_checksum == received_checksum, payload
    except:
        return False, ""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((socket.gethostname(), 1234))
print("✅ Server ready on port 1234")

while True:
    try:
        raw_data, addr = server_socket.recvfrom(1024)
        raw_data = raw_data.decode("utf-8")

        is_valid, payload = verify_checksum(raw_data)
        if not is_valid:
            server_socket.sendto("ERROR: Corrupted data".encode("utf-8"), addr)
            continue

        parts = payload.split(",")
        if len(parts) != 4:
            raise ValueError("Invalid format, expected 4 fields")

        op, op1, op2, _ = parts
        op2 = op2 if op2 != "" else None
        result = calculate_operation(op, op1, op2)
        response = f"{op},{op1},{op2},{result}"
        server_socket.sendto(response.encode("utf-8"), addr)

    except Exception as e:
        server_socket.sendto(f"ERROR: {e}".encode("utf-8"), addr)