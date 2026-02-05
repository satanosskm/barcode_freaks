import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import subprocess
from utils import get_profiles_dir, get_image_path  # Import des utilitaires

PROFILS_DIR = get_profiles_dir()
LAST_PROFILE_FILE = os.path.join(PROFILS_DIR, "last_profile.txt")
IMAGES_DIR = "images"  # Conservé pour compatibilité

# Charger le profil actif
def load_current_profile():
    """Charge le nom du profil actif à partir de last_profile.txt."""
    if os.path.exists(LAST_PROFILE_FILE):
        with open(LAST_PROFILE_FILE, "r") as file:
            return file.read().strip()
    raise FileNotFoundError("Le fichier last_profile.txt est introuvable.")

# Charger les données du profil actif
def load_profile_data(profile_name):
    """Charge les données du profil actif."""
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Le fichier de profil {profile_name}.txt est introuvable.")
    
    profile_data = {}
    with open(profile_path, "r") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                profile_data[key] = value
    return profile_data

# Charger les détails d'un freak à partir du profil
def load_freak_details(freak_id):
    """Charge les détails d'un freak à partir du profil."""
    profile_name = load_current_profile()
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Le fichier de profil {profile_name}.txt est introuvable.")

    with open(profile_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("freaks=["):
                content = line[8:].strip("[]\n")  # Nettoyer les crochets et les sauts de ligne
                freak_lines = content.split(", ")
                for freak_line in freak_lines:
                    if freak_line.startswith(freak_id):
                        parts = freak_line.split("|")
                        if len(parts) == 7:  # Vérifie que la ligne contient bien 7 éléments
                            level = parts[6].split("_")[1]  # Extraire correctement le niveau
                            return {
                                "id": parts[0],
                                "name": parts[1],
                                "type": parts[2],
                                "attack": int(parts[3]),
                                "defense": int(parts[4]),
                                "pv": int(parts[5]),
                                "level": level
                            }
    raise ValueError(f"Aucun détail trouvé pour le freak ID {freak_id}.")

# Charger les points de l'espèce depuis freakopedia
def load_species_points(species_name, profile_path):
    """Charge le nombre de points de l'espèce depuis la section freakopedia du profil."""
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            for line in file:
                if line.startswith("freakopedia="):
                    freakopedia = eval(line.split("=", 1)[1].strip())
                    if species_name in freakopedia:
                        return freakopedia[species_name].get("nombre de points", 0)
    return 0

# Charger le niveau maximum (ligue_level) depuis le profil
def load_league_level(profile_path):
    """Charge le niveau maximum (ligue_level) depuis le profil."""
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            for line in file:
                if line.startswith("ligue_level="):
                    return line.strip().split("=")[1]
    return "01"  # Valeur par défaut si non trouvée

# Vérifier si le freak peut être entraîné
def can_train_freak(freak_level, league_level, species_points):
    """Vérifie si le freak peut être entraîné."""
    return int(freak_level) < int(league_level) and int(freak_level) < int(species_points)

def update_freak_stats(profile_path, freak_id, stat_to_update, increment):
    """Met à jour les statistiques du freak actuel dans le fichier de profil."""
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith("freaks=["):
                content = line[8:].strip("[]\n")  # Nettoyer les crochets et les sauts de ligne
                freak_lines = content.split(", ")
                for j, freak_line in enumerate(freak_lines):
                    if freak_line.startswith(freak_id):  # Trouver le freak correspondant à l'ID
                        parts = freak_line.split("|")
                        if stat_to_update == "attack":
                            parts[3] = str(int(parts[3]) + increment)  # Incrémenter l'attaque
                        elif stat_to_update == "defense":
                            parts[4] = str(int(parts[4]) + increment)  # Incrémenter la défense
                        elif stat_to_update == "pv":
                            parts[5] = str(int(parts[5]) + increment)  # Incrémenter les PV
                        # Incrémenter le niveau
                        current_level = int(parts[6].split("_")[1])  # Extraire le niveau actuel
                        parts[6] = f"lv_{current_level + 1:02}"  # Mettre à jour le niveau
                        freak_lines[j] = "|".join(parts)  # Réassembler la ligne
                        break
                lines[i] = f"freaks=[{', '.join(freak_lines)}]\n"
                break

        with open(profile_path, "w") as file:
            file.writelines(lines)

def train_freak(stat_to_update):
    """Logique d'entraînement pour un freak."""
    global can_train  # Rendre can_train accessible globalement
    global stats_label, level_label, gain_label, result_label  # Rendre les labels accessibles
    if not can_train:
        result_label.config(text="Vous ne pouvez plus entraîner ce freak.")
        return

    roll = random.randint(1, 3)  # Lancer 1D3
    increment = roll if stat_to_update != "pv" else roll * 2
    message = {
        1: "Entraînement faible !",
        2: "Entraînement moyen !",
        3: "Super entraînement !"
    }[roll]

    # Mettre à jour les statistiques dans le fichier de profil
    update_freak_stats(profile_path, current_freak_id, stat_to_update, increment)

    # Recalculer les conditions d'entraînement
    freak_details = load_freak_details(current_freak_id)
    can_train = can_train_freak(freak_details['level'], league_level, species_points)

    # Désactiver les boutons si les conditions ne sont plus remplies
    if not can_train:
        for button in training_buttons:
            button.config(state="disabled")

    # Mettre à jour les informations visuelles des stats et du niveau
    stats_label.config(text=f"Stats : Attaque {freak_details['attack']}, Défense {freak_details['defense']}, PV {freak_details['pv']}")
    level_label.config(text=f"Niveau : {freak_details['level']}")

    # Afficher les messages dans l'interface
    gain_message = f"+ {increment} {stat_to_update.capitalize()} !" if stat_to_update != "pv" else f"+ {increment} PV !"
    gain_label.config(text=gain_message)
    result_label.config(text=f"{message}\nVotre freak a gagné un niveau !")

def return_to_main_menu():
    """Retourne au menu principal."""
    global root  # Ensure root is accessible
    root.destroy()
    subprocess.run(["python", "barcodefreaks.py"])

# Fonction principale
def main():
    global root  # Declare root as global
    global result_label, can_train, training_buttons, league_level, species_points, stats_label, level_label, gain_label  # Ajouter les variables globales nécessaires

    try:
        profile_name = load_current_profile()
        global profile_path  # Définir profile_path
        profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
        with open(profile_path, "r") as file:
            lines = file.readlines()
            global current_freak_id  # Définir current_freak_id
            current_freak_id = None
            for line in lines:
                if line.startswith("current_freak="):
                    current_freak_id = line.strip().split("=")[1]
                    break
            if not current_freak_id:
                raise ValueError("Aucun freak actuel défini dans le profil.")

        freak_details = load_freak_details(current_freak_id)
        species_points = load_species_points(freak_details['name'], profile_path)  # Charger les points de l'espèce
        league_level = load_league_level(profile_path)  # Charger le niveau maximum
        can_train = can_train_freak(freak_details['level'], league_level, species_points)  # Vérifier si le freak peut être entraîné
    except Exception as e:
        print(f"Erreur : {e}")
        return

    # Création de la fenêtre principale
    root = tk.Tk()  # Define root here
    root.title("Training")
    root.state("zoomed")  # Maximiser la fenêtre
    root.configure(bg="lightblue")  # Couleur de fond harmonieuse

    # Chargement de l'image après l'initialisation de Tkinter
    image_path = get_image_path(f"{freak_details['id'].split('_')[0]}.png")
    freak_image = None
    if os.path.exists(image_path):
        image = Image.open(image_path).resize((500, 500))  # Taille ajustée à 500x500
        freak_image = ImageTk.PhotoImage(image)

    # Ajout de "Freak actuel :" tout en haut
    tk.Label(root, text="Freak actuel :", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=5)

    # Cadre principal pour tout centrer verticalement
    main_frame = tk.Frame(root, bg="lightblue")
    main_frame.pack(expand=True, fill="both", pady=10)

    # Cadre pour les informations (points et niveau maximum) au-dessus de l'image
    info_above_image_frame = tk.Frame(main_frame, bg="lightblue")
    info_above_image_frame.pack(pady=5)
    tk.Label(info_above_image_frame, text=f"Points : {species_points}", font=("Arial", 16), bg="lightblue").pack(pady=2)
    tk.Label(info_above_image_frame, text=f"Niveau maximum : {league_level}", font=("Arial", 16), bg="lightblue").pack(pady=2)

    # Affichage de l'image
    if freak_image:
        image_label = tk.Label(main_frame, image=freak_image, bg="lightblue")
        image_label.image = freak_image
        image_label.pack(pady=10)

    # Affichage des informations du freak
    info_frame = tk.Frame(main_frame, bg="lightblue")
    info_frame.pack(pady=5)
    tk.Label(info_frame, text=f"Nom : {freak_details['name']}", font=("Arial", 16), bg="lightblue").pack()
    tk.Label(info_frame, text=f"Type : {freak_details['type']}", font=("Arial", 16), bg="lightblue").pack()
    level_label = tk.Label(info_frame, text=f"Niveau : {freak_details['level']}", font=("Arial", 16), bg="lightblue")
    level_label.pack()
    stats_label = tk.Label(info_frame, text=f"Stats : Attaque {freak_details['attack']}, Défense {freak_details['defense']}, PV {freak_details['pv']}", font=("Arial", 16), bg="lightblue")
    stats_label.pack()

    # Boutons pour augmenter les stats
    button_frame = tk.Frame(main_frame, bg="lightblue")
    button_frame.pack(pady=10)
    training_buttons = [
        tk.Button(button_frame, text="Augmenter force", command=lambda: train_freak("attack"), font=("Arial", 12), bg="lightgreen", state="normal" if can_train else "disabled"),
        tk.Button(button_frame, text="Augmenter défense", command=lambda: train_freak("defense"), font=("Arial", 12), bg="lightyellow", state="normal" if can_train else "disabled"),
        tk.Button(button_frame, text="Augmenter PV", command=lambda: train_freak("pv"), font=("Arial", 12), bg="lightpink", state="normal" if can_train else "disabled")
    ]
    for button in training_buttons:
        button.pack(side="left", padx=5)

    # Label pour afficher les résultats de l'entraînement
    result_label = tk.Label(main_frame, text="", font=("Arial", 14), bg="lightblue", fg="darkblue", justify="center")
    result_label.pack(pady=10)

    # Label pour afficher les gains de stats
    gain_label = tk.Label(main_frame, text="", font=("Arial", 14), bg="lightblue", fg="green", justify="center")
    gain_label.pack(pady=5)

    # Bouton retour au menu principal
    tk.Button(main_frame, text="Retour au menu principal", command=return_to_main_menu,
              font=("Arial", 12), bg="lightcoral").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
