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

        self.build_interface()

    def build_interface(self):
        ctk.CTkLabel(self, text="").pack(pady=10)

        self.title_label = ctk.CTkLabel(self, text="Messagerie Client-Serveur", font=("Arial", 25, "bold"))
        self.title_label.pack(pady=10)

        ctk.CTkLabel(self, text="").pack(pady=10)
        texte_frame = ctk.CTkFrame(self)
        texte_frame.pack(pady=10)

        self.op1_texte = ctk.CTkLabel(texte_frame, text="Opérande 1 (8 bits)", font=("Arial", 15),width=220)
        self.op1_texte.grid(row=0, column=0, padx=10)

        self.operation_menu_texte = ctk.CTkLabel(texte_frame, text="Opération", font=("Arial", 15),width=80)
        self.operation_menu_texte.grid(row=0, column=1, padx=10)

        self.op2_texte = ctk.CTkLabel(texte_frame, text="Opérande 2 (8 bits)", font=("Arial", 15),width=220)
        self.op2_texte.grid(row=0, column=2, padx=10)

        self.op1_entry = ctk.CTkEntry(texte_frame, placeholder_text="exp:10101010", width=220)
        self.op1_entry.grid(row=1, column=0, padx=10)

        self.operation_menu_texte = ctk.CTkOptionMenu(texte_frame, values=["AND", "OR", "XOR", "LS", "RS", "INVERT"], width=80)
        self.operation_menu_texte.grid(row=1, column=1, padx=10)

        self.op2_entry = ctk.CTkEntry(texte_frame, placeholder_text="exp:10101010", width=220)
        self.op2_entry.grid(row=1, column=2, padx=10)

        self.send_button = ctk.CTkButton(texte_frame, text="Envoyer", fg_color="green", hover_color="#007f00", command=self.send_data)
        self.send_button.grid(row=1, column=3, padx=10)

        response_frame = ctk.CTkFrame(self)
        response_frame.pack(pady=20)

        self.response_label = ctk.CTkLabel(response_frame, text="Réponse :", font=("Arial", 15))
        self.response_label.grid(row=0, column=0, padx=10)

        self.response_entry = ctk.CTkEntry(response_frame, state="readonly", width=400)
        self.response_entry.grid(row=0, column=1, padx=10)

    def send_data(self):
        op1 = self.op1_entry.get()
        op2 = self.op2_entry.get()
        operation = self.operation_menu_texte.get()

        if not (len(op1) == 8 and set(op1) <= {"0", "1"}):
            messagebox.showerror("Erreur d'entrée", "L'opérande 1 doit être un binaire de 8 bits.")
            return

        if not (len(op2) == 8 and set(op2) <= {"0", "1"}):
            messagebox.showerror("Erreur d'entrée", "L'opérande 2 doit être un binaire de 8 bits.")
            return

        op1 = "0b" + op1
        op2 = "0b" + op2
        operation = operation.upper()

        response = self.send_to_server(operation, op1, op2)

        self.response_entry.configure(state="normal")
        self.response_entry.delete(0, "end")
        self.response_entry.insert(0, response)
        self.response_entry.configure(state="readonly")

    def send_to_server(self, op, op1, op2, result=""):
        server_addr = (socket.gethostname(), 1234)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            payload = f"{op},{op1},{op2},{result}"
            checksum = hashlib.md5(payload.encode("utf-8")).hexdigest()
            full_data = f"{payload},{checksum}"

            s.sendto(full_data.encode("utf-8"), server_addr)
            response, _ = s.recvfrom(1024)
            return response.decode("utf-8").split(",")[3][2:]
        except Exception as e:
            return f"Erreur réseau: {e}"
        finally:
            s.close()

if __name__ == "__main__":
    # Launch server.py in the background
    subprocess.Popen(["python", "server.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
    app = BinaryOperationApp()
    app.mainloop()
