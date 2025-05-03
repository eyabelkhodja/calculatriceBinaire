import customtkinter as ctk
from tkinter import messagebox

class BinaryOperationApp(ctk.CTk):  # Application pour les opérations binaires
    def __init__(self):
        super().__init__()
        self.title("Messagerie Client-Serveur")
        self.geometry("800x350")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.build_interface()

    def build_interface(self):
        # Espacement au-dessus du titre
        ctk.CTkLabel(self, text="").pack(pady=10)

        # Titre centré en haut
        self.title_label = ctk.CTkLabel(self, text="Messagerie Client-Serveur", font=("Arial", 25, "bold"))
        self.title_label.pack(pady=10)

        # Espacement en dessous du titre
        ctk.CTkLabel(self, text="").pack(pady=10)

        # Cadre pour les entrées horizontales, centré
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10)

        self.op1_entry = ctk.CTkEntry(input_frame, placeholder_text="Opérande 1 (8 bits)", width=150)
        self.op1_entry.grid(row=0, column=0, padx=10)

        self.operation_menu = ctk.CTkOptionMenu(input_frame, values=["AND", "OR", "XOR", "NAND", "NOR", "XNOR"], width=80)
        self.operation_menu.grid(row=0, column=1, padx=10)

        self.op2_entry = ctk.CTkEntry(input_frame, placeholder_text="Opérande 2 (8 bits)", width=150)
        self.op2_entry.grid(row=0, column=2, padx=10)

        # Bouton Envoyer dans le même cadre
        self.send_button = ctk.CTkButton(input_frame, text="Envoyer", fg_color="green", hover_color="#007f00", command=self.send_data)
        self.send_button.grid(row=0, column=3, padx=10)

        # Réponse dans un cadre séparé, centré
        response_frame = ctk.CTkFrame(self)
        response_frame.pack(pady=20)

        self.response_label = ctk.CTkLabel(response_frame, text="Réponse :", font=("Arial", 15))
        self.response_label.grid(row=0, column=0, padx=10)

        self.response_entry = ctk.CTkEntry(response_frame, state="readonly", width=400)
        self.response_entry.grid(row=0, column=1, padx=10)

    def send_data(self):
        op1 = self.op1_entry.get()
        op2 = self.op2_entry.get()
        operation = self.operation_menu.get()

        # Vérification de l'opérande 1 (doit être un binaire de 8 bits)
        if not (len(op1) == 8 and set(op1) <= {"0", "1"}):
            messagebox.showerror("Erreur d'entrée", "L'opérande 1 doit être un binaire de 8 bits.")
            return

        # Vérification de l'opérande 2 (doit être un binaire de 8 bits)
        if not (len(op2) == 8 and set(op2) <= {"0", "1"}):
            messagebox.showerror("Erreur d'entrée", "L'opérande 2 doit être un binaire de 8 bits.")
            return

        # Réponse simulée (à remplacer par la logique de socket)
        simulated_response = f"{op1} {operation} {op2}"

        self.response_entry.configure(state="normal")
        self.response_entry.delete(0, "end")
        self.response_entry.insert(0, simulated_response)
        self.response_entry.configure(state="readonly")

if __name__ == "__main__":
    app = BinaryOperationApp()
    app.mainloop()
