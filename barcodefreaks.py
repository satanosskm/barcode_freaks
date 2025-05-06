import asyncio
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import subprocess
from PIL import Image, ImageTk  # Importer pour gérer l'image du logo
from gen_ligue import generate_ligue  # Importer la génération des adversaires
from creatures import creatures  # Importer la liste des freaks
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("Démarrage de l'application Barcode Freaks")

PROFILS_DIR = "profils"
LAST_PROFILE_FILE = os.path.join(PROFILS_DIR, "last_profile.txt")

def create_new_profile():
    """Demande un nom de joueur et crée un nouveau profil."""
    name = simpledialog.askstring("Nouveau joueur", "Entrez votre nom :", parent=root)
    if not name:
        messagebox.showerror("Erreur", "Le nom du joueur ne peut pas être vide.")
        return create_new_profile()

    profile_path = os.path.join(PROFILS_DIR, f"{name}.txt")
    if os.path.exists(profile_path):
        messagebox.showerror("Erreur", "Un profil avec ce nom existe déjà.")
        return create_new_profile()

    # Générer les adversaires pour la ligue
    adversaires = generate_ligue()

    # Générer la liste des freaks avec leurs attributs
    freakopedia = {freak["name"]: {"decouvert": False, "nombre de points": 0} for freak in creatures}

    # Sauvegarder le profil avec les adversaires dans une section "league"
    with open(profile_path, "w") as file:
        file.write("freaks=[\n]\n")
        file.write("current_freak=None\n")
        file.write(f"freakopedia={freakopedia}\n")
        file.write("barcode_scanned=[]\n")
        file.write("ligue_level=01\n")
        file.write("league={\n")
        for i, adversaire in enumerate(adversaires, start=1):
            key = f"adversaire{i:02d}"
            file.write(f"  {key}={adversaire['name']}|{adversaire['type']}|{adversaire['stats']['attack']}|{adversaire['stats']['defense']}|{adversaire['stats']['pv']}\n")
        file.write("}\n")

    with open(LAST_PROFILE_FILE, "w") as file:
        file.write(name)

    return name

def load_last_profile():
    """Charge le dernier profil utilisé ou demande un nouveau nom si aucun profil n'existe."""
    if not os.path.exists(PROFILS_DIR):
        os.makedirs(PROFILS_DIR)

    if os.path.exists(LAST_PROFILE_FILE):
        with open(LAST_PROFILE_FILE, "r") as file:
            return file.read().strip()
    else:
        return create_new_profile()  # Créer un nouveau profil si aucun n'existe

def open_scan():
    """
    Ferme la fenêtre actuelle et ouvre l'interface de scan.
    """
    root.destroy()
    subprocess.run(["python", "scan.py"])

def open_freakopedia():
    """
    Ferme la fenêtre actuelle et ouvre l'interface de la Freakopedia.
    """
    root.destroy()
    subprocess.run(["python", "freakopedia.py"])

def open_stockage():
    """
    Ferme la fenêtre actuelle et ouvre l'interface de stockage.
    """
    root.destroy()
    subprocess.run(["python", "stockage.py"])

def open_ligue():
    """
    Ferme la fenêtre actuelle et ouvre l'interface de la ligue.
    """
    root.destroy()  # Fermer la fenêtre actuelle
    subprocess.run(["python", "ligue.py"])

def open_training():
    """
    Ferme la fenêtre actuelle et ouvre l'interface d'entraînement.
    """
    root.destroy()
    subprocess.run(["python", "training.py"])

def open_profil():
    """
    Ferme la fenêtre actuelle et ouvre l'interface de gestion du profil.
    """
    root.destroy()
    subprocess.run(["python", "profil.py"])

# Création de la fenêtre principale
root = tk.Tk()
root.title("Barcode Freaks")
root.state("zoomed")  # Démarrer maximisé
root.configure(bg="lightblue")  # Couleur de fond harmonieuse

# Charger le dernier profil ou en créer un nouveau
current_profile = load_last_profile()
print(f"Profil chargé : {current_profile}")

# Définir les boutons avant d'utiliser leur longueur
buttons = [
    ("Scanner un code-barre", open_scan, "lightgreen"),
    ("Freakopedia", open_freakopedia, "lightyellow"),
    ("Mes Freaks", open_stockage, "lightblue"),
    ("Ligue Barcode Freaks", open_ligue, "lightcoral"),
    ("Entraîner mon Freak", open_training, "lightpink"),
    ("Profil", open_profil, "lightgray"),
]

# Charger et afficher le logo
try:
    logo_path = os.path.join("images", "logo_BF.png")
    logo_image = Image.open(logo_path).resize((600, 600))  # Redimensionner à 600x600
    logo_tk = ImageTk.PhotoImage(logo_image)
except FileNotFoundError:
    logo_tk = None
    print("Logo introuvable : logo_BF.png")

# Création d'un cadre principal pour organiser le logo et les boutons
main_frame = tk.Frame(root, bg="lightblue")
main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le cadre principal

# Ajouter le logo à gauche
if logo_tk:
    logo_label = tk.Label(main_frame, image=logo_tk, bg="lightblue")
    logo_label.grid(row=0, column=0, rowspan=len(buttons) + 1, padx=20, pady=10)

# Ajouter les boutons à droite
button_frame = tk.Frame(main_frame, bg="lightblue")
button_frame.grid(row=0, column=1, sticky="n", padx=20)

# Titre
title_label = tk.Label(button_frame, text=f"Profil : {current_profile}", font=("Arial", 24), bg="lightblue", fg="darkblue")
title_label.pack(pady=20)

# Boutons pour les différents menus
for text, command, color in buttons:
    button = tk.Button(button_frame, text=text, command=command, font=("Arial", 14), bg=color, width=30)
    button.pack(pady=10)

# Bouton pour quitter le jeu
quit_button = tk.Button(button_frame, text="Quitter le jeu", command=root.quit, font=("Arial", 14), bg="red", fg="white", width=30)
quit_button.pack(pady=20)

# Lancer la boucle principale
root.mainloop()
