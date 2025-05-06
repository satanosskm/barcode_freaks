import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
from gen_ligue import generate_ligue  # Importer la génération des adversaires
from creatures import creatures  # Importer la liste des freaks

PROFILS_DIR = "profils"
LAST_PROFILE_FILE = os.path.join(PROFILS_DIR, "last_profile.txt")

def change_profile():
    """Ouvre une fenêtre pour sélectionner un autre profil."""
    profile_path = filedialog.askopenfilename(initialdir=PROFILS_DIR, title="Sélectionnez un profil",
                                              filetypes=(("Fichiers texte", "*.txt"),))
    if profile_path:
        profile_name = os.path.splitext(os.path.basename(profile_path))[0]
        with open(LAST_PROFILE_FILE, "w") as file:
            file.write(profile_name)
        messagebox.showinfo("Profil changé", f"Profil chargé : {profile_name}")
        print("Returning to main menu...")  # Placeholder for window manager logic

def create_new_profile():
    """
    Demande un nom de joueur, crée un nouveau profil et génère les adversaires.
    """
    name = simpledialog.askstring("Nouveau joueur", "Entrez votre nom :", parent=root)
    if not name:
        messagebox.showerror("Erreur", "Le nom du joueur ne peut pas être vide.")
        return

    profile_path = os.path.join(PROFILS_DIR, f"{name}.txt")
    if os.path.exists(profile_path):
        messagebox.showerror("Erreur", "Un profil avec ce nom existe déjà.")
        return

    # Générer les adversaires pour la ligue
    adversaires = generate_ligue()

    # Générer la liste des freaks avec leurs attributs
    freakopedia = {freak["name"]: {"decouvert": False, "nombre de points": 0} for freak in creatures}

    # Sauvegarder le profil avec les adversaires dans une section "league"
    with open(profile_path, "w") as file:
        file.write("freaks=[\n]\n")
        file.write("current_freak=None\n")
        file.write(f"freakopedia={freakopedia}\n")  # Ajouter la freakopedia avec les attributs
        file.write("barcode_scanned=[]\n")  # Ajout de la section barcode_scanned
        file.write("ligue_level=01\n")  # Initialiser à 01
        file.write("league={\n")
        for i, adversaire in enumerate(adversaires, start=1):
            key = f"adversaire{i:02d}"  # Toujours utiliser le format 'adversaire01'
            file.write(f"  {key}={adversaire['name']}|{adversaire['type']}|{adversaire['stats']['attack']}|{adversaire['stats']['defense']}|{adversaire['stats']['pv']}\n")
        file.write("}\n")

    # Mettre à jour le dernier profil utilisé
    with open(LAST_PROFILE_FILE, "w") as file:
        file.write(name)

    messagebox.showinfo("Profil créé", f"Profil {name} créé avec succès.")
    title_label.config(text=f"Profil : {name}")  # Mettre à jour le titre avec le nouveau profil

def return_to_main_menu():
    """Retourne au menu principal."""
    root.destroy()
    subprocess.run(["python", "barcodefreaks.py"])

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion du Profil")
root.state("zoomed")  # Démarrer en mode maximisé
root.configure(bg="lightblue")

# Label pour afficher le titre ou le profil actuel
title_label = tk.Label(root, text="Gestion du Profil", font=("Arial", 16), bg="lightblue")
title_label.pack(pady=10)

# Boutons pour les actions
buttons = [
    ("Changer de profil", change_profile, "lightblue"),
    ("Créer un nouveau joueur", create_new_profile, "lightgreen"),
    ("Retour au menu principal", return_to_main_menu, "lightcoral"),
]

for text, command, color in buttons:
    button = tk.Button(root, text=text, command=command, font=("Arial", 14), bg=color, width=30)
    button.pack(pady=10)

# Lancer la boucle principale
root.mainloop()
