import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageDraw
import os
import logging
import functools  # Importer partial pour corriger la gestion des clics
import subprocess
from utils import get_profiles_dir, get_image_path  # Import des utilitaires

# Configuration du logging pour déboguer
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

PROFILS_DIR = get_profiles_dir()
current_profile = open(os.path.join(PROFILS_DIR, "last_profile.txt")).read().strip()
profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")

def load_freaks():
    """Charge les freaks du profil du joueur."""
    freaks = []
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
                        if "|" in freak_line:
                            parts = freak_line.split("|")
                            if len(parts) == 7:  # Vérifie que la ligne contient bien 7 éléments
                                level = parts[6].split("_")[1]  # Extraire le niveau (yy) de lv_yy
                                freaks.append({
                                    "id": parts[0],
                                    "name": parts[1],
                                    "type": parts[2],
                                    "attack": parts[3],
                                    "defense": parts[4],
                                    "pv": parts[5],
                                    "level": level  # Ajouter le niveau
                                })
    return freaks

def load_current_freak():
    """Charge l'ID de la créature actuelle depuis le profil."""
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            for line in file:
                if line.startswith("current_freak="):
                    return line.strip().split("=")[1]
    return None

def open_visualizer(event, freak_id):
    """Ouvre l'interface visualizer pour afficher les détails d'un freak."""
    root.destroy()
    subprocess.Popen(["python", "visualizer.py", freak_id])

def return_to_main_menu():
    """Retourne au menu principal."""
    root.destroy()
    subprocess.Popen(["python", "barcodefreaks.py"])

def generate_placeholder(name, size=(120, 120)):
    """Génère un placeholder avec le nom de la créature."""
    img = Image.new("RGB", size, "gray")
    draw = ImageDraw.Draw(img)
    draw.text((10, size[1] // 2 - 10), name[:5], fill="white")  # Affiche les 5 premières lettres du nom
    return img

current_page = 1  # Page actuelle
freaks_per_page = 12  # Nombre de freaks par page

def display_freaks(freaks):
    """Affiche les freaks dans une grille paginée."""
    global current_page
    current_freak_id = load_current_freak()

    # Calculer les indices pour la pagination
    start_index = (current_page - 1) * freaks_per_page
    end_index = start_index + freaks_per_page
    paginated_freaks = freaks[start_index:end_index]

    # Nettoyer les widgets existants
    for widget in freaks_frame.winfo_children():
        widget.destroy()

    image_refs = []  # Liste pour conserver les références aux images
    row, col = 0, 0
    for freak in paginated_freaks:
        frame = tk.Frame(freaks_frame, width=200, height=200)
        frame.grid(row=row, column=col, padx=10, pady=10)

        # Charger l'image de la créature
        image_path = get_image_path(f"{freak['name'].lower()}.png")
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((120, 120))
                img_tk = ImageTk.PhotoImage(img)
            else:
                img = generate_placeholder(freak['name'])
                img_tk = ImageTk.PhotoImage(img)
        except Exception as e:
            logging.error(f"Erreur lors du chargement de l'image : {e}")
            img = generate_placeholder("Error")
            img_tk = ImageTk.PhotoImage(img)

        # Ajouter l'image de la créature
        img_label = tk.Label(frame, image=img_tk, cursor="hand2")
        img_label.image = img_tk
        img_label.pack()
        # Utiliser functools.partial pour transmettre correctement l'ID
        img_label.bind("<Button-1>", lambda event, freak_id=freak['id']: open_visualizer(event, freak_id))

        # Ajouter le texte (nom, type et niveau)
        name_color = "red" if freak["id"] == current_freak_id else "black"
        name_label = tk.Label(frame, text=f"{freak['name']} ({freak['type']}) {freak['level']}", font=("Arial", 12), fg=name_color)
        name_label.pack()

        image_refs.append(img_tk)

        col += 1
        if col == 4:  # Passer à la ligne suivante après 4 colonnes
            col = 0
            row += 1

    # Mettre à jour l'indicateur de page
    total_pages = (len(freaks) + freaks_per_page - 1) // freaks_per_page
    page_label.config(text=f"Page {current_page} sur {total_pages}")

def next_page():
    """Passe à la page suivante."""
    global current_page
    total_pages = (len(freaks) + freaks_per_page - 1) // freaks_per_page
    if current_page < total_pages:
        current_page += 1
        display_freaks(freaks)

def previous_page():
    """Revient à la page précédente."""
    global current_page
    if current_page > 1:
        current_page -= 1
        display_freaks(freaks)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Mes Freaks")
root.state("zoomed")  # Démarrer en mode maximisé
root.configure(bg="lightblue")

# Création d'un cadre pour les freaks
freaks_frame = tk.Frame(root)
freaks_frame.pack(pady=20)

# Indicateur de page
page_label = tk.Label(root, text="", font=("Arial", 14))
page_label.pack()

# Boutons de pagination
pagination_frame = tk.Frame(root)
pagination_frame.pack(pady=10)

prev_button = tk.Button(pagination_frame, text="← Page précédente", font=("Arial", 12), command=previous_page)
prev_button.grid(row=0, column=0, padx=10)

next_button = tk.Button(pagination_frame, text="Page suivante →", font=("Arial", 12), command=next_page)
next_button.grid(row=0, column=1, padx=10)

# Charger et afficher les freaks
freaks = load_freaks()
logging.debug(f"Freaks chargés : {freaks}")
display_freaks(freaks)

# Bouton pour revenir au menu principal
main_menu_button = tk.Button(root, text="Revenir au menu principal", font=("Arial", 14), bg="lightcoral",
                             command=return_to_main_menu)
main_menu_button.pack(pady=20)

# Lancer la boucle principale
root.mainloop()
