import socket
import hashlib

# Fonction pour effectuer des opérations binaires
# Cette fonction prend une opération et deux opérandes en format binaire, effectue l'opération spécifiée et retourne le résultat en format binaire.
def calculate_operation(op, op1, op2=None):
    # Convertit les opérandes binaires en entiers
    op1 = int(op1, 2)
    if op2:
        op2 = int(op2, 2)
# Dictionnaire des opérations possibles
# Les clés représentent les noms des opérations et les valeurs sont les résultats des opérations correspondantes.
    operations = {
        "AND": op1 & op2,
        "OR": op1 | op2,
        "XOR": op1 ^ op2,
        "LS": op1 << op2,
        "RS": op1 >> op2,
        "INVERT": ~op1,
    }
 # Conversion du résultat en binaire avec gestion du signe
 # Récupère le résultat de l'opération ou retourne une erreur si l'opération est invalide
    result = operations.get(op.upper(), "Operation Invalide")
    if isinstance(result, int):
        return bin(result) if result >= 0 else f"-0b{bin(abs(result))[2:]}"
    return result

# Fonction pour vérifier l'intégrité des données reçues
# Cette fonction utilise un checksum pour vérifier si les données ont été corrompues.
def verify_checksum(data: str) -> tuple[bool, str]:
    try:
        payload, received_checksum = data.rsplit(",", 1)
        calculated_checksum = hashlib.md5(payload.encode("utf-8")).hexdigest()
        return calculated_checksum == received_checksum, payload
    except:
        return False, ""
# Création et configuration du socket serveur
# Configuration pour utiliser UDP (SOCK_DGRAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((socket.gethostname(), 1234))
print("Serveur opérationnel, en attente de messages sur le port 1234...")

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
            raise ValueError("Format Invalide, on doit avoir 4 valeurs")

        op, op1, op2, _ = parts
        op2 = op2 if op2 != "" else None
        result = calculate_operation(op, op1, op2)
        response = f"{op},{op1},{op2},{result}"
        server_socket.sendto(response.encode("utf-8"), addr)

    except Exception as e:
        server_socket.sendto(f"ERROR: {e}".encode("utf-8"), addr)