import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import random
import os
import sys
import subprocess
from creatures import creatures
from table import calculate_damage, is_effective  # Ensure is_effective is imported

PROFILS_DIR = "profils"
LAST_PROFILE_FILE = os.path.join(PROFILS_DIR, "last_profile.txt")
IMAGES_DIR = "images"

def load_current_freak():
    """Charge l'ID du freak actuel depuis le profil."""
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
    Récupère les détails d'un freak à partir de son ID, y compris lv_xx.
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
                            freak = freak.strip()
                            if freak.startswith(freak_id):
                                parts = freak.split("|")
                                if len(parts) == 7:  # Inclure lv_xx
                                    return {
                                        "id": parts[0],
                                        "name": parts[1],
                                        "type": parts[2],
                                        "attack": int(parts[3].strip()),
                                        "defense": int(parts[4].strip()),
                                        "pv": int(parts[5].strip()),
                                        "lv_xx": parts[6]  # Retourner lv_xx directement
                                    }
        print(f"Freak ID {freak_id} introuvable dans le profil.")
    except Exception as e:
        print(f"Erreur lors de la récupération des détails du freak : {e}")
    return None

def get_freak_level_from_profile():
    """
    Charge l'ID du freak actuel depuis `current_freak=` et extrait `lv_xx` depuis la section `freaks=`.
    """
    try:
        with open(LAST_PROFILE_FILE, "r") as file:
            current_profile = file.read().strip()
        profile_path = os.path.join(PROFILS_DIR, f"{current_profile}.txt")
        if os.path.exists(profile_path):
            current_freak_id = None
            freaks_section = None

            # Lire le fichier pour trouver `current_freak=` et `freaks=`
            with open(profile_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("current_freak="):
                        current_freak_id = line.strip().split("=")[1]
                    elif line.startswith("freaks=["):
                        freaks_section = line[8:].strip("[]").split(", ")

            # Vérifier si l'ID du freak actuel et la section `freaks=` existent
            if not current_freak_id or not freaks_section:
                print("Erreur : Impossible de trouver `current_freak` ou `freaks` dans le profil.")
                return None

            # Rechercher l'ID dans la section `freaks=`
            for freak in freaks_section:
                parts = freak.strip().split("|")
                if parts[0] == current_freak_id and len(parts) == 7:
                    return parts[6].split("_")[1]  # Extraire `xx` de `lv_xx`

        print("Erreur : Fichier de profil introuvable ou mal formaté.")
    except Exception as e:
        print(f"Erreur lors de la récupération du niveau du freak : {e}")
    return None

def load_league(profile_name):
    """
    Load the league section from the profile file.
    """
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
                    league[key.strip()] = value.strip()
    return league

def generate_opponent(barcode):
    """Generate an opponent freak based on a barcode."""
    try:
        hash_value = hash(barcode)
        creature_index = hash_value % len(creatures)
        selected_creature = creatures[creature_index]
        stats = {
            "attack": (hash_value >> 8) % 20 + 1,
            "defense": (hash_value >> 16) % 20 + 1,
            "pv": (hash_value >> 24) % 21 + 20
        }
        return {
            "name": selected_creature["name"],
            "type": selected_creature["type"],
            "attack": stats["attack"],
            "defense": stats["defense"],
            "pv": stats["pv"]
        }
    except Exception as e:
        print(f"Error generating opponent: {e}")
    return None

def load_freak_image(freak_name):
    """Load the image for a freak by its name."""
    image_path = os.path.join(IMAGES_DIR, f"{freak_name.lower()}.png")
    if os.path.exists(image_path):
        img = Image.open(image_path).resize((300, 300))  # Adjusted image size
        return ImageTk.PhotoImage(img)
    else:
        print(f"Image not found for {freak_name}. Using placeholder.")
        placeholder = Image.new("RGB", (300, 300), "gray")  # Adjusted placeholder size
        return ImageTk.PhotoImage(placeholder)

def start_combat():
    """Determine who attacks first and update the combat log."""
    global turn
    turn = random.choice(["player", "opponent"])
    update_button_text()
    if turn == "player":
        combat_log.set("Vous attaquez en premier.")
    else:
        combat_log.set("L'adversaire attaque en premier.")

def update_button_text():
    """Update the button text based on the current turn."""
    if turn == "player":
        action_button.config(text="Attaquer")
    else:
        action_button.config(text="Défendre")

def update_health_labels():
    """Update the health labels for both freaks."""
    player_health.set(f"PV: {max(0, int(player_freak['stats']['pv']))}")  # Ensure PV is an integer
    opponent_health.set(f"PV: {max(0, int(opponent_freak['stats']['pv']))}")  # Ensure PV is an integer

def debug_combat(freak1, freak2, damage, attacker_type, defender_type):
    """
    Debug function to display detailed combat stats and damage calculation step by step.
    :param freak1: Attacking freak (dict)
    :param freak2: Defending freak (dict)
    :param damage: Calculated damage (int)
    :param attacker_type: Type of the attacker (str)
    :param defender_type: Type of the defender (str)
    """
    print("=== DEBUG COMBAT ===")
    print(f"Attacker: {freak1['name']} (Type: {attacker_type.capitalize()}, Attack: {freak1['stats']['attack']})")  # Correction ici
    print(f"Defender: {freak2['name']} (Type: {defender_type.capitalize()}, Defense: {freak2['stats']['defense']}, PV: {freak2['stats']['pv']})")  # Correction ici
    
    # Step 1: Calculate base damage
    base_damage = freak1["stats"]["attack"] - freak2["stats"]["defense"] + 1  # Correction ici
    print(f"Step 1 - Base Damage (Attack - Defense + 1): {freak1['stats']['attack']} - {freak2['stats']['defense']} + 1 = {base_damage}")
    
    # Step 2: Ensure minimum damage is 1
    adjusted_base_damage = max(1, base_damage)
    print(f"Step 2 - Adjusted Base Damage (max 1): max(1, {base_damage}) = {adjusted_base_damage}")
    
    # Step 3: Check type effectiveness
    is_advantage = is_effective(attacker_type, defender_type)
    print(f"Step 3 - Type Effectiveness: {'Effective' if is_advantage else 'Not Effective'}")
    
    # Step 4: Apply type multiplier if effective
    if is_advantage:
        final_damage = -(-adjusted_base_damage * 1.5 // 1)  # Round up
        print(f"Step 4 - Final Damage with Type Advantage (ceil(Base * 1.5)): ceil({adjusted_base_damage} * 1.5) = {final_damage}")
    else:
        final_damage = adjusted_base_damage
        print(f"Step 4 - Final Damage without Type Advantage: {final_damage}")
    
    # Final result
    print(f"Calculated Damage: {damage} (Expected: {final_damage})")
    print("====================")

def attack():
    """Handle the attack logic."""
    global player_freak, opponent_freak, turn
    if turn == "player":
        base_damage = player_freak["stats"]["attack"] - opponent_freak["stats"]["defense"] + 1
        damage = calculate_damage(base_damage, player_freak["type"].capitalize(), opponent_freak["type"].capitalize())
        debug_combat(player_freak, opponent_freak, damage, player_freak["type"], opponent_freak["type"])  # Debug
        opponent_freak["stats"]["pv"] -= damage
        combat_log.set(f"Vous infligez {int(damage)} dégâts à {opponent_freak['name']}!")  # Affichage clair
        if is_effective(player_freak["type"], opponent_freak["type"]):
            advantage_label.set(f"Votre {player_freak['name']} est avantagé !")
        else:
            advantage_label.set("")  # Clear the label if no advantage
        if opponent_freak["stats"]["pv"] <= 0:
            combat_log.set(f"Vous avez vaincu {opponent_freak['name']}!")
            action_button.config(state="disabled")
        turn = "opponent"
    else:
        base_damage = opponent_freak["stats"]["attack"] - player_freak["stats"]["defense"] + 1
        damage = calculate_damage(base_damage, opponent_freak["type"].capitalize(), player_freak["type"].capitalize())
        debug_combat(opponent_freak, player_freak, damage, opponent_freak["type"], player_freak["type"])  # Debug
        player_freak["stats"]["pv"] -= damage
        combat_log.set(f"{opponent_freak['name']} inflige {int(damage)} dégâts à {player_freak['name']}!")  # Affichage clair
        if is_effective(opponent_freak["type"], player_freak["type"]):
            advantage_label.set(f"Votre {player_freak['name']} est désavantagé !")
        else:
            advantage_label.set("")  # Clear the label if no disadvantage
        if player_freak["stats"]["pv"] <= 0:
            combat_log.set(f"Vous avez été vaincu par {opponent_freak['name']}!")
            action_button.config(state="disabled")
        turn = "player"
    update_health_labels()
    update_button_text()

def debug_league(profile_name):
    """
    Affiche l'état de la ligue pour le profil donné.
    """
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    if not os.path.exists(profile_path):
        print(f"[DEBUG] Fichier de profil introuvable : {profile_path}")
        return

    with open(profile_path, "r") as file:
        lines = file.readlines()

    league_section = False
    print("[DEBUG] État actuel de la ligue :")
    for line in lines:
        if line.strip() == "league={":
            league_section = True
        elif league_section:
            if line.strip() == "}":
                league_section = False
                break
            print(line.strip())

def surrender():
    """
    Retourne à l'interface de la ligue après avoir vérifié l'état du combat.
    """
    global player_freak, opponent_freak, profile_name, adversaire_key

    # Vérifier si les données des freaks sont valides
    if "stats" not in player_freak or "stats" not in opponent_freak:
        print("[DEBUG] Données des freaks invalides ou incomplètes.")
        debug_league(profile_name)  # Afficher l'état de la ligue
        return_to_ligue()
        return

    # Vérifier si le joueur a gagné
    if player_freak["stats"]["pv"] > 0 and opponent_freak["stats"]["pv"] <= 0:
        print(f"[DEBUG] Combat gagné contre {adversaire_key}")
        update_ligue_level(profile_name, adversaire_key)  # Mettre à jour ligue_level
    else:
        print(f"[DEBUG] Combat perdu ou non terminé contre {adversaire_key}")

    # Afficher l'état de la ligue avant de quitter
    debug_league(profile_name)

    # Retourner à la ligue
    return_to_ligue()

def return_to_ligue():
    """
    Ferme l'interface actuelle et retourne à la ligue.
    """
    root.destroy()
    subprocess.run(["python", "ligue.py"])

def update_ligue_level(profile_name, adversaire_key):
    """
    Met à jour la valeur de ligue_level dans le fichier de profil si nécessaire.
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

        # Réécrire le fichier sans toucher à la section league
        with open(profile_path, "w") as file:
            file.writelines(lines)
    else:
        print(f"[DEBUG] Aucun changement : adversaire_num < ligue_level")

def normalize_key(key):
    """
    Normalise une clé d'adversaire pour qu'elle soit toujours au format 'adversaire01'.
    """
    if key.startswith("adversaire") and len(key) == 11:
        return key  # Déjà normalisé
    if key.startswith("adversaire") and len(key) == 10:
        return key[:10] + "0" + key[10:]  # Ajouter un zéro pour normaliser
    return key

if __name__ == "__main__":
    # Charger les arguments
    if len(sys.argv) < 3:
        print("Usage: python dueltest.py <profile_name> <adversaire_key>")
        exit()
    profile_name = sys.argv[1]
    adversaire_key = normalize_key(sys.argv[2])  # Normaliser la clé
    print(f"[DEBUG] Clé interne normalisée : {adversaire_key}")  # Debug

    # Charger le profil et l'adversaire
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    league = load_league(profile_name)
    if adversaire_key not in league:
        print(f"Erreur : L'adversaire {adversaire_key} n'existe pas.")
        exit()
    adversaire_data = league[adversaire_key].split("|")
    opponent_freak = {
        "name": adversaire_data[0],
        "type": adversaire_data[1],
        "stats": {
            "attack": int(adversaire_data[2]),
            "defense": int(adversaire_data[3]),
            "pv": int(adversaire_data[4]),
        },
    }
    print(f"[DEBUG] Opponent freak initialisé : {opponent_freak}")  # Debug

    # Charger le freak actuel du joueur
    current_freak_id = load_current_freak()
    if not current_freak_id:
        print("Erreur : Aucun freak actuel trouvé.")
        exit()
    player_freak = get_freak_details(current_freak_id)
    if not player_freak:
        print("Erreur : Impossible de charger les détails du freak actuel.")
        exit()

    # Vérifier et structurer correctement player_freak
    if "stats" not in player_freak:
        player_freak = {
            "name": player_freak["name"],
            "type": player_freak["type"],
            "stats": {
                "attack": player_freak["attack"],
                "defense": player_freak["defense"],
                "pv": player_freak["pv"],
            },
        }
    print(f"[DEBUG] Player freak structuré : {player_freak}")  # Debug

    # Charger le niveau du freak actuel
    player_freak_level = get_freak_level_from_profile()
    if not player_freak_level:
        print("Erreur : Impossible de charger le niveau du freak actuel.")
        exit()

    # Create the main window
    root = tk.Tk()
    root.title("Combat 1v1")
    root.state("zoomed")  # Start maximized
    root.configure(bg="lightblue")

    # Main frame to hold both freaks and center them
    main_frame = tk.Frame(root, bg="lightblue")
    main_frame.place(relx=0.5, rely=0.4, anchor="center")  # Centered vertically and horizontally

    # Player's freak display
    player_frame = tk.Frame(main_frame, bg="lightblue")
    player_frame.grid(row=0, column=0, padx=60)
    tk.Label(player_frame, text=player_freak["name"], font=("Arial", 22), bg="lightblue").pack()
    tk.Label(player_frame, text=f"Niveau {player_freak_level.replace(']', '')}", font=("Arial", 18), bg="lightblue").pack()  # Retirer "]" esthétiquement
    tk.Label(player_frame, text=f"Type: {player_freak['type']}", font=("Arial", 18), bg="lightblue").pack()
    player_health = tk.StringVar(value=f"PV: {player_freak['stats']['pv']}")
    tk.Label(player_frame, textvariable=player_health, font=("Arial", 18), bg="lightblue").pack()
    player_image = load_freak_image(player_freak["name"])
    tk.Label(player_frame, image=player_image, bg="lightblue").pack()

    # Opponent's freak display
    opponent_frame = tk.Frame(main_frame, bg="lightblue")
    opponent_frame.grid(row=0, column=1, padx=60)
    tk.Label(opponent_frame, text=opponent_freak["name"], font=("Arial", 22), bg="lightblue").pack()
    tk.Label(opponent_frame, text=f"Niveau {adversaire_key[-2:].replace(']', '')}", font=("Arial", 18), bg="lightblue").pack()  # Retirer "]" esthétiquement
    tk.Label(opponent_frame, text=f"Type: {opponent_freak['type']}", font=("Arial", 18), bg="lightblue").pack()
    opponent_health = tk.StringVar(value=f"PV: {opponent_freak['stats']['pv']}")
    tk.Label(opponent_frame, textvariable=opponent_health, font=("Arial", 18), bg="lightblue").pack()
    opponent_image = load_freak_image(opponent_freak["name"])
    tk.Label(opponent_frame, image=opponent_image, bg="lightblue").pack()

    # Combat log
    combat_log = tk.StringVar(value="Le combat commence!")
    tk.Label(root, textvariable=combat_log, font=("Arial", 18), bg="lightblue", wraplength=1000).place(relx=0.5, rely=0.7, anchor="center")  # Centered below the freaks

    # Advantage/Disadvantage label
    advantage_label = tk.StringVar(value="")
    tk.Label(root, textvariable=advantage_label, font=("Arial", 16), bg="lightblue", fg="darkred").place(relx=0.5, rely=0.75, anchor="center")

    # Buttons
    button_frame = tk.Frame(root, bg="lightblue")
    button_frame.place(relx=0.5, rely=0.85, anchor="center")  # Centered at the bottom


    # --- Bouton Combat rapide ---
    auto_attack_job = None
    def start_auto_attack(event=None):
        auto_attack()
    def stop_auto_attack(event=None):
        global auto_attack_job
        if auto_attack_job:
            root.after_cancel(auto_attack_job)
            auto_attack_job = None
    def auto_attack():
        global auto_attack_job
        if action_button['state'] == 'normal':
            attack()
            auto_attack_job = root.after(80, auto_attack)  # 80ms entre chaque attaque
        else:
            auto_attack_job = None

    quick_button = Button(button_frame, text="Combat rapide", font=("Arial", 16), bg="#ff9900", fg="white", width=14)
    quick_button.grid(row=0, column=0, padx=(0, 10))
    quick_button.bind('<ButtonPress-1>', start_auto_attack)
    quick_button.bind('<ButtonRelease-1>', stop_auto_attack)

    action_button = Button(button_frame, text="Attaquer", font=("Arial", 16), command=attack, width=12)
    action_button.grid(row=0, column=1, padx=10)

    # Bouton "Retourner à la ligue"
    return_button = tk.Button(button_frame, text="Retourner à la ligue", font=("Arial", 16), bg="lightcoral", command=surrender, width=20)
    return_button.grid(row=0, column=2, padx=10)

    # Start the combat
    start_combat()

    # Run the main loop
    root.mainloop()
