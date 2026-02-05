"""
Barcode Freaks - Application principale
Gère la navigation entre les différents écrans du jeu
"""
import tkinter as tk
import os
import logging
from utils import get_profiles_dir

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BarcodeFreaksApp:
    """Classe principale de l'application Barcode Freaks"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.current_screen = None
        self.profiles_dir = get_profiles_dir()
        
        # Charger le dernier profil utilisé
        self.profile_name = self.load_last_profile()
        logging.info(f"Profil chargé : {self.profile_name}")
        
    def show_screen(self, screen_class, **kwargs):
        """Affiche un nouvel écran et détruit l'ancien."""
        if self.current_screen:
            try:
                self.current_screen.destroy()
            except Exception as e:
                logging.error(f"Erreur destruction écran: {e}")
        
        self.current_screen = screen_class(self.root, self, **kwargs)
        self.current_screen.setup()
        
    def run(self):
        """Lance l'application"""
        self.root.mainloop()
        
    def load_last_profile(self):
        """Charge le dernier profil utilisé ou retourne None si aucun profil n'existe."""
        last_profile_file = os.path.join(self.profiles_dir, "last_profile.txt")
        if os.path.exists(last_profile_file):
            try:
                with open(last_profile_file, "r") as f:
                    profile_name = f.read().strip()
                # Vérifier si le fichier du profil existe réellement
                if os.path.exists(os.path.join(self.profiles_dir, f"{profile_name}.txt")):
                    return profile_name
            except Exception as e:
                logging.error(f"Erreur lecture last_profile: {e}")
        
        # Si le dernier profil n'existe pas, on cherche s'il y en a un autre
        if os.path.exists(self.profiles_dir):
            profiles = [f[:-4] for f in os.listdir(self.profiles_dir) if f.endswith(".txt") and f != "last_profile.txt"]
            if profiles:
                return profiles[0]

        return None

    def get_profile_path(self):
        """Retourne le chemin complet du fichier de profil actuel."""
        return os.path.join(self.profiles_dir, f"{self.profile_name}.txt")

    def change_profile(self, new_profile_name):
        """Change le profil actif et met à jour l'application."""
        self.profile_name = new_profile_name
        
        # Mettre à jour last_profile.txt
        last_profile_file = os.path.join(self.profiles_dir, "last_profile.txt")
        with open(last_profile_file, "w") as f:
            f.write(new_profile_name)
            
        logging.info(f"Profil changé pour : {new_profile_name}")
