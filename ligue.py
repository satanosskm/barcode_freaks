import tkinter as tk
from tkinter import ttk, messagebox
import os
from dictionnaire import adversaire_dict  # Importer le dictionnaire des noms d'adversaires
from dueltest import generate_opponent  # Importer les fonctions nécessaires
from gen_ligue import generate_freak_from_ean13  # Pour générer les adversaires si besoin
from utils import get_profiles_dir  # Import des utilitaires

PROFILS_DIR = get_profiles_dir()
LAST_PROFILE_FILE = os.path.join(PROFILS_DIR, "last_profile.txt")

def load_current_freak():
    """Charge le freak actuel du joueur à partir du profil."""
    try:
        with open(LAST_PROFILE_FILE, "r") as file:
            current_profile = file.read().strip()
        profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")
        if os.path.exists(profile_path):
            with open(profile_path, "r") as file:
                for line in file:
                    if line.startswith("current_freak="):
                        current_freak = line.strip().split("=")[1]
                        if current_freak != "None":
                            return current_freak
        print("Aucun freak actuel trouvé dans le profil.")
    except Exception as e:
        print(f"Erreur lors du chargement du freak actuel : {e}")
    return None

def get_freak_details(freak_id):
    """
    Récupère les détails d'un freak à partir de son ID.
    """
    try:
        with open(LAST_PROFILE_FILE, "r") as file:
            current_profile = file.read().strip()
        profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")
        if os.path.exists(profile_path):
            with open(profile_path, "r") as file:
                for line in file:
                    if line.startswith("freaks=["):
                        freaks = line[8:].strip("[]").split(", ")
                        for freak in freaks:
                            freak = freak.strip()  # Nettoyer les espaces ou caractères inutiles
                            if freak.startswith(freak_id):
                                parts = freak.split("|")
                                if len(parts) == 7:  # Inclure lv_yy
                                    return {
                                        "id": parts[0],
                                        "name": parts[1],
                                        "type": parts[2],
                                        "attack": int(parts[3].strip()),
                                        "defense": int(parts[4].strip()),
                                        "pv": int(parts[5].strip()),
                                        "level": parts[6].strip()  # Ajouter le niveau
                                    }
        print(f"Freak ID {freak_id} introuvable dans le profil.")
    except Exception as e:
        print(f"Erreur lors de la récupération des détails du freak : {e}")
    return None

def load_current_profile():
    """Charge le profil actuel à partir du fichier last_profile.txt."""
    if os.path.exists(LAST_PROFILE_FILE):
        with open(LAST_PROFILE_FILE, "r") as file:
            return file.read().strip()
    return None

def load_league(profile_name):
    """Charge les adversaires de la ligue à partir du fichier de profil."""
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    league = {}
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            lines = file.readlines()
            in_league_section = False
            for line in lines:
                if line.strip() == "league={":
                    in_league_section = True
                elif in_league_section:
                    if line.strip() == "}":
                        break
                    key, value = line.strip().split("=")
                    league[key] = value
    return league

def setup_league(profile_name):
    """
    Configure la ligue en chargeant les adversaires débloqués depuis le profil.
    """
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    ligue_level = 0
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("ligue_level="):
                    ligue_level = int(line.split("=")[1].strip())
                    break

    if ligue_level > 50:  # Si le niveau de ligue dépasse 50
        message_label.config(
            text="Félicitations ! Tu es le grand maître de la ligue Barcode Freaks ! "
                 "Tu peux essayer de finir la ligue à nouveau avec un autre freak ou bien démarrer un nouveau profil ! Bravo !",
            fg="green"
        )
        ligue_level = 50  # Rester sur adversaire50

    adversaries = [adversaire_dict[f"adversaire{i:02d}"] for i in range(1, ligue_level + 1)]
    return adversaries

def update_ligue_level(profile_name, adversaire_key):
    """
    Met à jour la valeur de ligue_level dans le fichier de profil si nécessaire.
    :param profile_name: Nom du profil actuel.
    :param adversaire_key: Clé de l'adversaire battu (ex: 'adversaire02').
    """
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    if not os.path.exists(profile_path):
        print(f"[DEBUG] Fichier de profil introuvable : {profile_path}")
        return

    with open(profile_path, "r") as file:
        lines = file.readlines()

    ligue_level = 0
    for i, line in enumerate(lines):
        if line.startswith("ligue_level="):
            ligue_level = int(line.split("=")[1].strip())
            break

    # Extraire le numéro de l'adversaire battu
    adversaire_num = int(adversaire_key.replace("adversaire", ""))
    print(f"[DEBUG] ligue_level actuel : {ligue_level}, adversaire battu : {adversaire_num}")

    # Incrémenter ligue_level si l'adversaire battu a un numéro >= ligue_level
    if adversaire_num >= ligue_level:
        new_ligue_level = ligue_level + 1
        lines[i] = f"ligue_level={new_ligue_level:02d}\n"
        print(f"[DEBUG] ligue_level mis à jour : {new_ligue_level}")

        with open(profile_path, "w") as file:
            file.writelines(lines)
    else:
        print(f"[DEBUG] Aucun changement : adversaire_num < ligue_level")

def start_combat(adversaire_key, league, profile_name):
    """
    Lance l'interface de combat pour l'adversaire sélectionné.
    """
    if adversaire_key not in league:
        messagebox.showerror("Erreur", f"L'adversaire {adversaire_key} n'existe pas.")
        return

    # Charger les détails de l'adversaire
    adversaire_data = league[adversaire_key].split("|")
    adversaire = {
        "name": adversaire_data[0],
        "type": adversaire_data[1],
        "stats": {
            "attack": int(adversaire_data[2]),
            "defense": int(adversaire_data[3]),
            "pv": int(adversaire_data[4]),
        },
    }
    print(f"[DEBUG] Adversaire chargé : {adversaire}")

    # Charger le freak actuel du joueur
    current_freak_id = load_current_freak()
    if not current_freak_id:
        messagebox.showerror("Erreur", "Aucun freak actuel trouvé.")
        return

    player_freak = get_freak_details(current_freak_id)
    if not player_freak:
        messagebox.showerror("Erreur", "Impossible de charger les détails du freak actuel.")
        return

    # Lancer l'interface de combat
    root.destroy()  # Fermer l'interface actuelle
    os.system(f"python dueltest.py {profile_name} {adversaire_key}")  # Passer les arguments nécessaires

def normalize_key(key):
    """
    Normalise une clé d'adversaire pour qu'elle soit toujours au format 'adversaire01'.
    """
    if key.startswith("adversaire") and len(key) == 11:
        return key  # Déjà normalisé
    if key.startswith("adversaire") and len(key) == 10:
        return key[:10] + "0" + key[10:]  # Ajouter un zéro pour normaliser
    return key

# Création de l'interface principale
root = tk.Tk()
root.title("Ligue Barcode Freaks")
root.state("zoomed")  # Démarrer maximisé
root.configure(bg="lightblue")

# Ajouter un label pour afficher les messages sous les boutons
message_label = tk.Label(root, text="", font=("Arial", 14), bg="lightblue", fg="darkred", wraplength=600, justify="center")

# Charger le profil actuel
profile_name = load_current_profile()
if not profile_name:
    messagebox.showerror("Erreur", "Aucun profil actuel trouvé.")
    root.destroy()
    exit()

# Charger les adversaires de la ligue
league = load_league(profile_name)
available_adversaries = setup_league(profile_name)
if not available_adversaries:
    messagebox.showerror("Erreur", "Aucun adversaire trouvé dans la ligue.")
    root.destroy()
    exit()

# Titre
title_label = tk.Label(root, text=f"Ligue - Profil : {profile_name}", font=("Arial", 16), bg="lightblue")
title_label.pack(pady=10)

# Menu déroulant pour sélectionner un adversaire
adversaire_var = tk.StringVar(value=available_adversaries[-1])  # Dernier adversaire débloqué
adversaire_menu = ttk.Combobox(root, textvariable=adversaire_var, values=available_adversaries, state="readonly", font=("Arial", 12))
adversaire_menu.pack(pady=10)

# Bouton pour lancer le combat
def on_combat_button_click():
    """
    Lance le combat pour l'adversaire sélectionné.
    """
    selected_display_name = adversaire_var.get()  # Par exemple, "Adversaire N°01"
    print(f"[DEBUG] Nom affiché sélectionné : {selected_display_name}")  # Debug
    try:
        # Convertir le nom affiché en clé interne
        selected_key = next(key for key, value in adversaire_dict.items() if value == selected_display_name)
        normalized_key = normalize_key(selected_key)  # Normaliser la clé
        print(f"[DEBUG] Clé interne normalisée : {normalized_key}")  # Debug
        print(f"[DEBUG] Contenu de league : {league}")  # Debug
        start_combat(normalized_key, league, profile_name)
    except StopIteration:
        messagebox.showerror("Erreur", f"Impossible de trouver l'adversaire correspondant à {selected_display_name}.")
    except KeyError:
        messagebox.showerror("Erreur", f"L'adversaire {selected_key} n'existe pas dans la ligue.")

combat_button = tk.Button(root, text="Combattre", font=("Arial", 14), bg="lightgreen", command=on_combat_button_click)
combat_button.pack(pady=20)

# Bouton pour revenir au menu principal
def return_to_main_menu():
    """
    Ferme la fenêtre actuelle et retourne au menu principal.
    """
    root.destroy()  # Fermer la fenêtre actuelle
    os.system("python barcodefreaks.py")  # Relancer le menu principal

main_menu_button = tk.Button(root, text="Revenir au menu principal", font=("Arial", 14), bg="lightcoral", command=return_to_main_menu)
main_menu_button.pack(pady=10)

# Afficher le message sous les boutons
message_label.pack(pady=20)

# Lancer la boucle principale
root.mainloop()
