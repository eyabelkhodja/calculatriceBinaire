import socket
import hashlib
from simulate_network import simulate_network


# Nettoie les entrées utilisateur
# Cette fonction supprime les espaces et les crochets des entrées utilisateur.
def clean_input(L):
    return [x.strip().replace("[", "").replace("]", "") for x in L]


# Lit et valide l'entrée utilisateur
# Cette fonction demande à l'utilisateur d'entrer les données et les valide.
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

# Menu d'opérations
# Affiche les options disponibles pour l'utilisateur.
def menu():
    print("\n=== Menu Calculatrice Binaire ===")
    print("l'operande doit etre sous la forme alphabetique (exemple: OR...)")
    print("1. BITWISE OR       |")
    print("2. BITWISE AND      &&")
    print("3. BITWISE XOR      ^")
    print("4. BITWISE LEFT     <<")
    print("5. BITWISE RIGHT    >>")
    print("6. BITWISE INVERT   ~ (utilise uniquement l'opérande 1)")
    print("7. EXIT")

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

        corrupted_data = simulate_network(full_data, error_probability=0.0)  #changer error_probability pour tester les erreurs
        print(f"Sending: {corrupted_data}")
        s.sendto(corrupted_data.encode("utf-8"), server_addr)

        response, _ = s.recvfrom(1024)
        print("Reponse du Serveur:", response.decode("utf-8"))
    except Exception as e:
        print("Erreur Client:", e)

s.close()
