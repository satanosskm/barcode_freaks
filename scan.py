import tkinter as tk
from tkinter import PhotoImage, StringVar, Label, Menu, Button, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw  # Nécessaire pour gérer les formats d'image comme JPG
from pyzbar.pyzbar import decode
import os
from creatures import creatures
import hashlib
import random
import subprocess

# Ajout de la variable pour le profil actif
PROFILS_DIR = "profils"
with open(os.path.join(PROFILS_DIR, "last_profile.txt"), "r") as file:
    current_profile = file.read().strip()

def generate_placeholder(type_: str, size=(100, 100)):
    """Génère un placeholder avec une forme spécifique pour le type."""
    image = Image.new("RGB", size, color="gray")
    draw = ImageDraw.Draw(image)
    if type_ == "ciel":
        draw.ellipse([10, 10, size[0] - 10, size[1] - 10], fill="skyblue")  # Cercle bleu ciel
    elif type_ == "feu":
        draw.polygon([(size[0] // 2, 10), (10, size[1] - 10), (size[0] - 10, size[1] - 10)], fill="orange")  # Triangle orange
    elif type_ == "aqua":
        draw.rectangle([10, 10, size[0] - 10, size[1] - 10], fill="blue")  # Rectangle bleu
    elif type_ == "poison":
        draw.ellipse([10, 10, size[0] - 10, size[1] - 10], fill="purple")  # Cercle violet
        draw.text((size[0] // 4, size[1] // 2 - 10), "☠", fill="white", align="center")  # Symbole poison
    elif type_ == "mineral":
        draw.rectangle([10, 10, size[0] - 10, size[1] - 10], fill="darkgray")  # Rectangle gris
        draw.line([(10, 10), (size[0] - 10, size[1] - 10)], fill="white", width=3)  # Ligne diagonale
        draw.line([(10, size[1] - 10), (size[0] - 10, 10)], fill="white", width=3)  # Ligne diagonale inverse
    elif type_ == "plante":
        draw.rectangle([10, 10, size[0] - 10, size[1] - 10], fill="green")  # Rectangle vert
        draw.line([(size[0] // 2, 10), (size[0] // 2, size[1] - 10)], fill="darkgreen", width=3)  # Tige
        draw.ellipse([size[0] // 2 - 10, 10, size[0] // 2 + 10, 30], fill="darkgreen")  # Feuille
    elif type_ == "tech":
        draw.rectangle([10, 10, size[0] - 10, size[1] - 10], fill="silver")  # Rectangle argenté
        draw.rectangle([30, 30, size[0] - 30, size[1] - 30], fill="black")  # Écran noir
        draw.line([(30, 30), (size[0] - 30, size[1] - 30)], fill="red", width=2)  # Ligne rouge diagonale
    else:
        draw.text((10, size[1] // 2 - 10), "No Image", fill="white")
    return image

def get_creature_data(barcode: str):
    """Détermine les données de la créature (nom, type, stats) en fonction du code-barres."""
    hash_value = hashlib.sha256(barcode.encode()).hexdigest()
    creature_index = int(hash_value[:8], 16) % len(creatures)  # Sélection équitable
    selected_creature = creatures[creature_index]

    stats = {
        "attack": int(hash_value[8:16], 16) % 20 + 1,  # Entre 1 et 20
        "defense": int(hash_value[16:24], 16) % 20 + 1,  # Entre 1 et 20
        "PV": int(hash_value[24:32], 16) % 21 + 20  # Entre 20 et 40
    }

    return selected_creature["name"], selected_creature["type"], stats

def on_paste(event=None):
    """Permet de coller du texte dans le champ d'entrée via clic droit."""
    try:
        clipboard = root.clipboard_get()
        barcode_var.set(clipboard)
    except Exception as e:
        print(f"Erreur lors du collage : {e}")

def on_enter(event=None):
    """Valide la génération de la créature avec la touche Entrée."""
    generate_creature()

def save_freak_to_profile(creature_name, creature_type, creature_stats):
    """Ajoute une créature au profil du joueur et réinitialise l'interface."""
    profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")
    if not os.path.exists(profile_path):
        print("Profil introuvable.")
        return

    # Lire le fichier de profil
    with open(profile_path, "r") as file:
        lines = file.readlines()

    # Trouver la section freaks=[]
    for i, line in enumerate(lines):
        if line.startswith("freaks=["):
            # Extraire les freaks existants
            content = line[8:].strip()  # Supprime "freaks=[" et les espaces
            if content.endswith("]"):
                content = content[:-1]  # Supprime la dernière parenthèse
            freak_lines = content.split(",") if content else []
            freak_lines = [f.strip() for f in freak_lines if f.strip()]  # Nettoyer les lignes

            # Générer un identifiant unique pour la nouvelle créature
            base_id = f"{creature_name.lower()}_"
            counter = 1
            while any(f.startswith(f"{base_id}{counter:04d}|") for f in freak_lines):
                counter += 1
            creature_id = f"{base_id}{counter:04d}"

            # Ajouter la nouvelle créature avec l'attribut lv_yy
            new_freak = f"{creature_id}|{creature_name}|{creature_type}|{creature_stats['attack']}|{creature_stats['defense']}|{creature_stats['PV']}|lv_01"
            freak_lines.append(new_freak)

            # Réécrire la ligne freaks=[]
            lines[i] = f"freaks=[{', '.join(freak_lines)}]\n"

            # Vérifier et définir la créature actuelle si aucune n'est définie
            for j, line in enumerate(lines):
                if line.startswith("current_freak="):
                    if line.strip() == "current_freak=None":
                        lines[j] = f"current_freak={creature_id}\n"
                    break
            break

    # Mettre à jour l'attribut "decouvert" dans freakopedia
    for i, line in enumerate(lines):
        if line.startswith("freakopedia="):
            freakopedia = eval(line.split("=")[1].strip())
            if creature_name in freakopedia and not freakopedia[creature_name]["decouvert"]:
                freakopedia[creature_name]["decouvert"] = True
                lines[i] = f"freakopedia={freakopedia}\n"
            break

    # Écrire les modifications dans le fichier
    with open(profile_path, "w") as file:
        file.writelines(lines)

    print(f"Créature {creature_name} ajoutée au profil avec l'ID {creature_id}.")
    # Réinitialiser l'interface
    reset_interface()

def reset_interface():
    """Réinitialise l'interface pour entrer un nouveau code-barre."""
    barcode_var.set("")
    name_label.config(text="Nom :")
    type_label.config(text="Type :")
    stats_label.config(text="Stats :")
    image_label.config(image=default_image_tk)
    image_label.image = default_image_tk
    adopt_button.config(state="disabled")
    reset_button.config(state="normal")
    message_label.config(text="")  # Réinitialiser le message

def return_to_main_menu():
    """Retourne au menu principal."""
    root.destroy()
    subprocess.run(["python", "barcodefreaks.py"])


def is_valid_ean(barcode):
    """Vérifie si un code-barres EAN-13 ou EAN-8 est valide."""
    if not barcode.isdigit():
        return False
    if len(barcode) == 13:
        checksum = sum(int(barcode[i]) * (3 if i % 2 else 1) for i in range(12))
        check_digit = (10 - (checksum % 10)) % 10
        return check_digit == int(barcode[-1])
    elif len(barcode) == 8:
        # EAN-8: impairs (0,2,4,6) *3, pairs (1,3,5) *1
        checksum = sum(int(barcode[i]) * (3 if i % 2 == 0 else 1) for i in range(7))
        check_digit = (10 - (checksum % 10)) % 10
        return check_digit == int(barcode[-1])
    else:
        return False

def generate_creature():
    """Génère une bestiole et met à jour l'image et les informations."""
    # Réinitialiser le message
    message_label.config(text="")

    barcode = barcode_var.get()


    # Vérifier si le code-barres est valide (EAN-13 ou EAN-8)
    if not is_valid_ean(barcode):
        message_label.config(text="Code-barre non valide !", fg="red")
        return

    creature_name, creature_type, creature_stats = get_creature_data(barcode)

    # Vérifier si le code-barres est déjà scanné
    profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            lines = file.readlines()

        # Charger la section barcode_scanned
        barcode_scanned = []
        for line in lines:
            if line.startswith("barcode_scanned="):
                barcode_scanned = eval(line.split("=")[1].strip())
                break

        if barcode not in barcode_scanned:
            # Ajouter le code-barres à barcode_scanned
            barcode_scanned.append(barcode)

            # Incrémenter les points de l'espèce correspondante
            for i, line in enumerate(lines):
                if line.startswith("freakopedia="):
                    freakopedia = eval(line.split("=")[1].strip())
                    if creature_name in freakopedia:
                        freakopedia[creature_name]["nombre de points"] += 5  # Gagner 5 points
                        message_label.config(text=f"Tu as gagné 5 points {creature_name} !")  # Mettre à jour le message dans l'interface
                    lines[i] = f"freakopedia={freakopedia}\n"
                    break

            # Mettre à jour barcode_scanned dans le fichier
            for i, line in enumerate(lines):
                if line.startswith("barcode_scanned="):
                    lines[i] = f"barcode_scanned={barcode_scanned}\n"
                    break

            with open(profile_path, "w") as file:
                file.writelines(lines)

    try:
        # Chargement de l'image spécifique si disponible
        image_path = os.path.join(os.path.dirname(__file__), "images", f"{creature_name.lower()}.png")
        if os.path.exists(image_path):  # Vérifie si le fichier existe
            image = Image.open(image_path)
            image = image.resize((600, 600))  # Redimensionnez à 600x600 pixels
        else:
            raise FileNotFoundError  # Lève une exception si le fichier n'existe pas
    except FileNotFoundError:
        # Génération d'un placeholder spécifique si l'image est introuvable
        print(f"Image introuvable pour '{creature_name}', génération d'un placeholder pour '{creature_type}'.")
        image = generate_placeholder(creature_type, size=(600, 600))
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        image = generate_placeholder("error", size=(600, 600))

    # Mise à jour de l'image dans l'interface
    updated_image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=updated_image_tk)
    image_label.image = updated_image_tk  # Nécessaire pour éviter que l'image soit supprimée par le garbage collector

    # Mise à jour des informations de la bestiole
    name_label.config(text=f"Nom : {creature_name}")
    type_label.config(text=f"Type : {creature_type.capitalize()}")
    stats_label.config(text=f"Stats : Attack={creature_stats['attack']}, Defense={creature_stats['defense']}, PV={creature_stats['PV']}")

    # Activer les boutons
    adopt_button.config(state="normal")
    reset_button.config(state="normal")

def select_image_and_get_ean():
    """Ouvre une boîte de dialogue pour sélectionner une image et lit le code-barres EAN-13 ou EAN-8."""
    file_path = filedialog.askopenfilename(
        title="Sélectionnez une image",
        filetypes=[("Images PNG et JPEG", "*.png;*.jpg;*.jpeg")]
    )
    if not file_path:
        return None

    try:
        # Charger l'image et décoder le code-barres
        image = Image.open(file_path)
        decoded_objects = decode(image)

        if not decoded_objects:
            messagebox.showerror("Erreur", "Aucun code-barres détecté dans l'image.")
            return None

        # Extraire le premier code-barres EAN-13 ou EAN-8 trouvé
        for obj in decoded_objects:
            if obj.type in ("EAN13", "EAN8"):
                return obj.data.decode("utf-8")

        messagebox.showerror("Erreur", "Aucun code-barres EAN-13 ou EAN-8 trouvé dans l'image.")
        return None
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire l'image : {e}")
        return None

def scan_barcode_image():
    """Scanne une image pour lire un code-barres EAN-13 ou EAN-8 et valide automatiquement."""
    code = select_image_and_get_ean()
    if code:
        barcode_var.set(code)  # Ajoute le code à l'entrée
        generate_creature()  # Valide automatiquement

# Création de la fenêtre principale
root = tk.Tk()
root.title("Jeu des Bestioles")
root.state("zoomed")  # Démarrer en mode maximisé
root.configure(bg="lightblue")

# Placeholder par défaut
try:
    default_image_path = os.path.join(os.path.dirname(__file__), "images", "logo_BF.png")  # Charger logo_BF.png
    default_image = Image.open(default_image_path).resize((600, 600))  # Chargement de logo_BF.png
    default_image_tk = ImageTk.PhotoImage(default_image)
except FileNotFoundError:
    print("Image logo_BF.png introuvable, génération d'un placeholder par défaut.")
    default_image = generate_placeholder(type_="default", size=(600, 600))
    default_image_tk = ImageTk.PhotoImage(default_image)

# Image de la créature
image_label = Label(root, image=default_image_tk, bg="lightblue")
image_label.grid(row=1, column=0, columnspan=3, pady=(10, 20), sticky="nsew")  # Ajout de marge inférieure

# Ajustement des colonnes pour centrer les éléments
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Champs et bouton pour générer une bestiole
barcode_label = tk.Label(root, text="Entrez un code-barres EAN-13 ou EAN-8 :", font=("Arial", 14))
barcode_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

barcode_var = StringVar()
barcode_entry = tk.Entry(root, textvariable=barcode_var, font=("Arial", 14), width=20)
barcode_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

generate_button = tk.Button(root, text="Générer Bestiole", command=generate_creature, font=("Arial", 14), bg="lightgreen")
generate_button.grid(row=0, column=2, padx=5, pady=5)

# Labels pour afficher les informations de la bestiole
info_frame = tk.Frame(root)
info_frame.grid(row=2, column=0, columnspan=3, pady=(10, 20))  # Ajout de marge inférieure

name_label = Label(info_frame, text="Nom :", font=("Arial", 16), anchor="w", width=30)
name_label.grid(row=0, column=0, padx=5, pady=2)

type_label = Label(info_frame, text="Type :", font=("Arial", 16), anchor="w", width=30)
type_label.grid(row=1, column=0, padx=5, pady=2)

stats_label = Label(info_frame, text="Stats :", font=("Arial", 16), anchor="w", width=30)
stats_label.grid(row=2, column=0, padx=5, pady=2)

# Boutons pour adopter et réinitialiser
button_frame = tk.Frame(root, bg="lightblue")  # Fond bleu clair pour le cadre
button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 20))  # Ajout de marge inférieure

adopt_button = Button(button_frame, text="Adopter ce freak", font=("Arial", 14), state="disabled", bg="lightgreen", command=lambda: save_freak_to_profile(
    name_label.cget("text").split(": ")[1],
    type_label.cget("text").split(": ")[1],
    {
        "attack": int(stats_label.cget("text").split(", ")[0].split("=")[1]),
        "defense": int(stats_label.cget("text").split(", ")[1].split("=")[1]),
        "PV": int(stats_label.cget("text").split(", ")[2].split("=")[1])
    }
))
adopt_button.grid(row=0, column=0, padx=10)

reset_button = Button(button_frame, text="Scanner une image de code-barre", font=("Arial", 14), bg="lightyellow", command=scan_barcode_image)
reset_button.grid(row=0, column=1, padx=10)

# Bouton pour revenir au menu principal
main_menu_button = Button(root, text="Revenir au menu principal", font=("Arial", 14), bg="lightcoral",
                          command=return_to_main_menu)
main_menu_button.grid(row=4, column=0, columnspan=3, pady=(10, 10))  # Ajustement de la marge inférieure

# Ajout du menu contextuel pour clic droit
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Coller", command=lambda: barcode_var.set(root.clipboard_get()))

barcode_entry.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))  # Associe le clic droit au menu contextuel
barcode_entry.bind("<Return>", lambda event: generate_creature())  # Associe la touche Entrée à la validation

# Création d'un label pour afficher les messages
message_label = Label(root, text="", font=("Arial", 14), bg="lightblue", fg="green")
message_label.grid(row=5, column=0, columnspan=3, pady=10)

# Lancer la boucle principale de l'interface
root.mainloop()