import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import logging
import subprocess

# Configuration du logging pour déboguer
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

PROFILS_DIR = "profils"
current_profile = open(os.path.join(PROFILS_DIR, "last_profile.txt")).read().strip()
profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")

def load_freak_details(freak_id):
    """Charge les détails d'un freak à partir du profil."""
    logging.debug(f"Recherche des détails pour l'ID : {freak_id}")
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("freaks=["):
                    # Extraire le contenu entre les crochets
                    content = line[8:].strip()  # Supprime "freaks=[" et les espaces
                    if content.endswith("]"):
                        content = content[:-1]  # Supprime la dernière parenthèse
                    freak_lines = content.split(",")  # Sépare les freaks par des virgules
                    for freak_line in freak_lines:
                        freak_line = freak_line.strip()
                        if freak_line.startswith(freak_id):
                            parts = freak_line.split("|")
                            if len(parts) == 7:  # Vérifie que la ligne contient bien 7 éléments
                                level = parts[6].split("_")[1]  # Extraire le niveau (yy) de lv_yy
                                logging.debug(f"Détails trouvés pour l'ID {freak_id} : {parts}")
                                return {
                                    "id": parts[0],
                                    "name": parts[1],
                                    "type": parts[2],
                                    "attack": int(parts[3]),
                                    "defense": int(parts[4]),
                                    "pv": int(parts[5]),
                                    "level": level  # Ajouter le niveau
                                }
    logging.warning(f"Aucun détail trouvé pour l'ID : {freak_id}")
    return None

def set_as_current_freak(freak_id):
    """Définit la créature actuelle dans le fichier de profil."""
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith("current_freak="):
                lines[i] = f"current_freak={freak_id}\n"
                break

        with open(profile_path, "w") as file:
            file.writelines(lines)

        print(f"Créature {freak_id} définie comme actuelle.")

def return_to_stockage():
    """Retourne à l'interface de stockage."""
    root.destroy()
    subprocess.run(["python", "stockage.py"])

# Création de la fenêtre principale
root = tk.Tk()
root.title("Détails de la créature")
root.state("zoomed")  # Démarrer en mode maximisé
root.configure(bg="lightblue")

# Charger les détails de la créature
freak_id = sys.argv[1]  # ID complet passé depuis stockage.py
freak = load_freak_details(freak_id)

if not freak:
    # Gérer le cas où la créature n'est pas trouvée
    error_label = tk.Label(root, text="Erreur : Créature introuvable.", font=("Arial", 16), fg="red", bg="lightblue")
    error_label.pack(pady=20)
    back_button = tk.Button(root, text="Retour au stockage", font=("Arial", 14), bg="lightcoral",
                            command=return_to_stockage)
    back_button.pack(pady=20)
    root.mainloop()
    sys.exit()

# Extraire le nom de l'espèce à partir de l'ID (avant le "_")
species_name = freak['id'].split("_")[0]

# Charger l'image de l'espèce
image_path = os.path.join("images", f"{species_name}.png")
if os.path.exists(image_path):
    img = Image.open(image_path).resize((600, 600))
    img_tk = ImageTk.PhotoImage(img)
else:
    logging.warning(f"Image introuvable pour l'espèce : {species_name}")
    img_tk = None

# Afficher l'image
image_label = tk.Label(root, image=img_tk, bg="lightblue")
image_label.image = img_tk
image_label.pack(pady=10)

# Afficher les détails
details_frame = tk.Frame(root, bg="lightblue")
details_frame.pack(pady=10)

name_label = tk.Label(details_frame, text=f"Nom : {freak['name']}", font=("Arial", 16), bg="lightblue")
name_label.pack(pady=5)

type_label = tk.Label(details_frame, text=f"Type : {freak['type']}", font=("Arial", 16), bg="lightblue")
type_label.pack(pady=5)

stats_label = tk.Label(details_frame, text=f"Stats : Attack={freak['attack']}, Defense={freak['defense']}, PV={freak['pv']}", font=("Arial", 16), bg="lightblue")
stats_label.pack(pady=5)

level_label = tk.Label(details_frame, text=f"Niveau {freak['level']}", font=("Arial", 16), bg="lightblue")
level_label.pack(pady=5)

# Bouton pour revenir au stockage
back_button = tk.Button(root, text="Retour au stockage", font=("Arial", 14), bg="lightcoral",
                        command=return_to_stockage)
back_button.pack(pady=20)

# Ajouter un bouton pour définir comme freak actuel
set_current_button = tk.Button(root, text="Définir comme freak actuel", font=("Arial", 14), bg="lightgreen",
                                command=lambda: set_as_current_freak(freak["id"]))
set_current_button.pack(pady=20)

# Lancer la boucle principale
root.mainloop()
