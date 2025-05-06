# Ce fichier affichera la fiche détaillée d'une espèce sélectionnée dans Freakopedia.

import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import subprocess
from creatures import creatures  # Importer la liste des créatures

PROFILS_DIR = "profils"
LAST_PROFILE_FILE = os.path.join(PROFILS_DIR, "last_profile.txt")

def load_freak_details(freak_name):
    """Charge les détails d'un freak à partir de creatures.py et du profil."""
    # Charger les informations depuis creatures.py
    creature_info = next((creature for creature in creatures if creature["name"] == freak_name), None)
    if not creature_info:
        return None

    # Charger les informations depuis la section freakopedia du profil
    with open(LAST_PROFILE_FILE, "r") as file:
        current_profile = file.read().strip()
    profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")

    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("freakopedia="):
                    freakopedia = eval(line.split("=", 1)[1].strip())
                    if freak_name in freakopedia:
                        return {
                            "name": creature_info["name"],
                            "type": creature_info["type"],
                            "description": creature_info["description"],
                            "points": freakopedia[freak_name]["nombre de points"]
                        }
    return None

def return_to_freakopedia():
    """Retourne à l'interface de la Freakopedia."""
    root.destroy()
    subprocess.run(["python", "freakopedia.py"])

# Création de la fenêtre principale
root = tk.Tk()
root.title("Fiche du Freak")
root.state("zoomed")  # Démarrer en mode maximisé
root.configure(bg="lightblue")

# Charger les détails du freak
freak_name = sys.argv[1]  # Nom du freak passé depuis freakopedia.py
freak = load_freak_details(freak_name)

if not freak:
    # Gérer le cas où le freak n'est pas trouvé
    error_label = tk.Label(root, text="Erreur : Freak introuvable.", font=("Arial", 16), fg="red", bg="lightblue")
    error_label.pack(pady=20)
    back_button = tk.Button(root, text="Retour à la Freakopedia", font=("Arial", 14), bg="lightcoral", command=return_to_freakopedia)
    back_button.pack(pady=20)
    root.mainloop()
    sys.exit()

# Cadre principal pour centrer tout le contenu
main_frame = tk.Frame(root, bg="lightblue")
main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le cadre principal

# Charger l'image du freak
image_path = os.path.join("images", f"{freak_name.lower()}.png")
if os.path.exists(image_path):
    img = Image.open(image_path).resize((600, 600))
    img_tk = ImageTk.PhotoImage(img)
else:
    img_tk = None

# Afficher l'image
image_label = tk.Label(main_frame, image=img_tk, bg="lightblue")
image_label.image = img_tk
image_label.pack(pady=10)

# Afficher les détails
details_frame = tk.Frame(main_frame, bg="lightblue")
details_frame.pack(pady=10)

name_label = tk.Label(details_frame, text=f"Nom : {freak['name']}", font=("Arial", 16), bg="lightblue")
name_label.pack(pady=5)

type_label = tk.Label(details_frame, text=f"Type : {freak['type']}", font=("Arial", 16), bg="lightblue")
type_label.pack(pady=5)

points_label = tk.Label(details_frame, text=f"Nombre de points : {freak['points']}", font=("Arial", 16), bg="lightblue")
points_label.pack(pady=5)

description_label = tk.Label(details_frame, text=f"Description : {freak['description']}", font=("Arial", 16), bg="lightblue", wraplength=800, justify="center")
description_label.pack(pady=5)

# Bouton pour revenir à la Freakopedia
back_button = tk.Button(main_frame, text="Retour à la Freakopedia", font=("Arial", 14), bg="lightcoral", command=return_to_freakopedia)
back_button.pack(pady=20)

# Lancer la boucle principale
root.mainloop()
