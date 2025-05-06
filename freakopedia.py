import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

PROFILS_DIR = "profils"
LAST_PROFILE_FILE = os.path.join(PROFILS_DIR, "last_profile.txt")

def load_current_profile():
    """Charge le profil actuel à partir du fichier last_profile.txt."""
    if os.path.exists(LAST_PROFILE_FILE):
        with open(LAST_PROFILE_FILE, "r") as file:
            return file.read().strip()
    return None

def fix_encoding_issues(data):
    """Corrige les problèmes d'encodage dans les données."""
    if isinstance(data, dict):
        return {key: fix_encoding_issues(value) for key, value in data.items()}
    if isinstance(data, str):
        return data.replace("d�couvert", "découvert")
    return data

def load_discovered_freaks(profile_name):
    """Charge les freaks découverts depuis le profil."""
    profile_path = os.path.join(PROFILS_DIR, f"{profile_name}.txt")
    if not os.path.exists(profile_path):
        return []

    with open(profile_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("freakopedia="):
            freakopedia = eval(line.split("=", 1)[1].strip())
            discovered = [name for name, data in freakopedia.items() if data.get("decouvert")]
            return sorted(discovered)  # Trier par ordre alphabétique
    return []

def open_fiche(selected_freak):
    """Ouvre la fiche de l'espèce sélectionnée."""
    if not selected_freak:
        messagebox.showerror("Erreur", "Veuillez sélectionner une espèce.")
        return
    root.destroy()
    os.system(f"python visu_pedia.py {selected_freak}")  # Passer le nom du freak sélectionné

def return_to_main_menu():
    """Retourne au menu principal."""
    root.destroy()
    subprocess.run(["python", "barcodefreaks.py"])

# Création de l'interface principale
root = tk.Tk()
root.title("Freakopedia")
root.state("zoomed")  # Démarrer maximisé
root.configure(bg="lightblue")

# Charger le profil actuel
profile_name = load_current_profile()
if not profile_name:
    messagebox.showerror("Erreur", "Aucun profil actuel trouvé.")
    root.destroy()
    exit()

# Charger les freaks découverts
discovered_freaks = load_discovered_freaks(profile_name)
if not discovered_freaks:
    messagebox.showinfo("Information", "Aucun freak découvert pour l'instant.")
    root.destroy()
    exit()

# Titre
title_label = tk.Label(root, text=f"Freakopedia - Profil : {profile_name}", font=("Arial", 16), bg="lightblue")
title_label.pack(pady=10)

# Menu déroulant pour sélectionner un freak
freak_var = tk.StringVar(value=discovered_freaks[0])  # Premier freak découvert par défaut
freak_menu = ttk.Combobox(root, textvariable=freak_var, values=discovered_freaks, state="readonly", font=("Arial", 12))
freak_menu.pack(pady=10)

# Bouton pour accéder à la fiche
fiche_button = tk.Button(root, text="Accéder à la fiche", font=("Arial", 14), bg="lightgreen", command=lambda: open_fiche(freak_var.get()))
fiche_button.pack(pady=20)

# Bouton pour revenir au menu principal
main_menu_button = tk.Button(root, text="Revenir au menu principal", font=("Arial", 14), bg="lightcoral",
                             command=return_to_main_menu)
main_menu_button.pack(pady=10)

# Lancer la boucle principale
root.mainloop()
