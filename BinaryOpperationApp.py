import subprocess
import os
import customtkinter as ctk
import socket
import hashlib
from tkinter import messagebox


class BinaryOperationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Messagerie Client-Serveur")
        self.geometry("800x350")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        # Variables d'état de la connexion
        self.connection_status_text = ctk.StringVar(value="🔴 Serveur déconnecté")
        self.server_connected = ctk.BooleanVar(value=False)
        self.build_interface() # Construction de l'interface graphique

    def build_interface(self):
        ctk.CTkLabel(self, text="").pack(pady=10)
        # Titre
        self.title_label = ctk.CTkLabel(self, text="Messagerie Client-Serveur", font=("Arial", 25, "bold"))
        self.title_label.pack(pady=10)
        # Bouton pour activer/désactiver la connexion
        self.connection_switch = ctk.CTkSwitch(self,textvariable=self.connection_status_text,font=("Arial", 22),variable=self.server_connected,command=self.toggle_connection,text_color="red")
        self.connection_switch.pack(pady=5)

        # Cadre pour les champs d'entrée
        ctk.CTkLabel(self, text="").pack(pady=10)
        texte_frame = ctk.CTkFrame(self)
        texte_frame.pack(pady=10)
        self.op1_texte = ctk.CTkLabel(texte_frame, text="Opérande 1 (8 bits)", font=("Arial", 15),width=220)
        self.op1_texte.grid(row=0, column=0, padx=10)

        self.operation_menu_texte = ctk.CTkLabel(texte_frame, text="Opération", font=("Arial", 15),width=80)
        self.operation_menu_texte.grid(row=0, column=1, padx=10)

        self.op2_texte = ctk.CTkLabel(texte_frame, text="Opérande 2 (8 bits)", font=("Arial", 15),width=220)
        self.op2_texte.grid(row=0, column=2, padx=10)
        # Champs de saisie pour les opérandes
        self.op1_entry = ctk.CTkEntry(texte_frame, placeholder_text="exp:10101010", width=220)
        self.op1_entry.grid(row=1, column=0, padx=10)
        # Menu déroulant pour choisir l'opération
        self.operation_menu_texte = ctk.CTkOptionMenu(texte_frame, values=["AND", "OR", "XOR", "LS", "RS", "INVERT"], width=80)
        self.operation_menu_texte.grid(row=1, column=1, padx=10)

        self.op2_entry = ctk.CTkEntry(texte_frame, placeholder_text="exp:10101010", width=220)
        self.op2_entry.grid(row=1, column=2, padx=10)
        # Bouton pour envoyer les données
        self.send_button = ctk.CTkButton(texte_frame, text="Envoyer", fg_color="green", hover_color="#007f00", command=self.send_data)
        self.send_button.grid(row=1, column=3, padx=10)

        # Cadre pour afficher la réponse du serveur
        response_frame = ctk.CTkFrame(self)
        response_frame.pack(pady=20)
        self.response_label = ctk.CTkLabel(response_frame, text="Réponse :", font=("Arial", 15))
        self.response_label.grid(row=0, column=0, padx=10)

        self.response_entry = ctk.CTkEntry(response_frame, state="readonly", width=400)
        self.response_entry.grid(row=0, column=1, padx=10)

    # Méthode appelée lorsqu'on clique sur "Envoyer"
    def send_data(self):
        if not self.server_connected.get():
            messagebox.showwarning("Connexion désactivée", "Veuillez activer la connexion au serveur avant d'envoyer.")
            return
        # Récupération des entrées utilisateur
        op1 = self.op1_entry.get()
        op2 = self.op2_entry.get()
        operation = self.operation_menu_texte.get()
        # Vérification que les opérandes sont bien des binaires de 8 bits
        if not (len(op1) == 8 and set(op1) <= {"0", "1"}):
            messagebox.showerror("Erreur d'entrée", "L'opérande 1 doit être un binaire de 8 bits.")
            return
        if not (len(op2) == 8 and set(op2) <= {"0", "1"}):
            messagebox.showerror("Erreur d'entrée", "L'opérande 2 doit être un binaire de 8 bits.")
            return
        # Préparation des données
        op1 = "0b" + op1
        op2 = "0b" + op2
        operation = operation.upper()
        # Envoi au serveur et affichage du résultat
        response = self.send_to_server(operation, op1, op2)
        self.response_entry.configure(state="normal")
        self.response_entry.delete(0, "end")
        self.response_entry.insert(0, response)
        self.response_entry.configure(state="readonly")

    # Envoie les données au serveur via UDP
    def send_to_server(self, op, op1, op2, result=""):
        server_addr = (socket.gethostname(), 1234)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            payload = f"{op},{op1},{op2},{result}"
            checksum = hashlib.md5(payload.encode("utf-8")).hexdigest()
            full_data = f"{payload},{checksum}"
            s.sendto(full_data.encode("utf-8"), server_addr)
            # Attente de la réponse du serveur
            response, _ = s.recvfrom(1024)
            return response.decode("utf-8").split(",")[3][2:]
        except Exception as e:
            return f"Erreur réseau: {e}"
        finally:
            s.close()

    # Active/désactive la connexion au serveur
    def toggle_connection(self):
        if self.server_connected.get():
            self.server_process = subprocess.Popen(["python", "server.py"],cwd=os.path.dirname(os.path.abspath(__file__)))
            self.connection_status_text.set("🟢 Serveur connecté")
            self.connection_switch.configure(text_color="green")
        else:
            if hasattr(self, "server_process"):
                self.server_process.terminate()
            self.connection_status_text.set("🔴 Serveur déconnecté")
            self.connection_switch.configure(text_color="red")


# Point d'entrée de l'application
if __name__ == "__main__":
    app = BinaryOperationApp()
    app.mainloop()
