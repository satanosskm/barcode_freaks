"""
Barcode Freaks - Profil
Écran de gestion du profil utilisateur
"""
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import logging
from utils import get_profiles_dir
from screens.base import Screen
from gen_ligue import generate_ligue
from creatures import creatures

class ProfileScreen(Screen):
    """Écran de gestion du profil"""
    
    def setup(self):
        """Configure l'écran du profil avec le nouveau design 'Paramètres épurés'"""
        self.root.title("Gestion du Profil - Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Conteneur principal centré
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- CARTE DE PROFIL ---
        card = tk.Frame(main_container, bg=self.CARD_BG, padx=40, pady=40, highlightthickness=1, highlightbackground="#1A1C1E")
        card.pack()

        # Titre
        tk.Label(card, text="PROFIL JOUEUR", font=self.FONT_TITLE, bg=self.CARD_BG, fg=self.PRIMARY).pack(pady=(0, 10))
        
        self.title_label = tk.Label(
            card, 
            text=f"NOM : {self.app.profile_name.upper() if self.app.profile_name else 'AUCUN'}", 
            font=self.FONT_SUBTITLE, 
            bg=self.CARD_BG,
            fg=self.ACCENT
        )
        self.title_label.pack(pady=(0, 40))
        
        # Bouton frame
        btn_container = tk.Frame(card, bg=self.CARD_BG)
        btn_container.pack()
        
        # Définition des actions
        self.create_button(btn_container, "CHANGER DE PROFIL", self.on_change_profile, color=self.SECONDARY).pack(pady=10, fill="x")
        self.create_button(btn_container, "NOUVEAU JOUEUR", self.on_create_profile, color=self.SUCCESS).pack(pady=10, fill="x")
        
        tk.Frame(card, height=1, bg="#1A1C1E").pack(fill="x", pady=20) # Séparateur

        self.create_button(card, "RETOUR AU MENU", self.back_to_menu, color=self.SECONDARY).pack(fill="x")
            
    def on_change_profile(self):
        """Ouvre un sélecteur de fichiers pour changer de profil"""
        profiles_dir = get_profiles_dir()
        file_path = filedialog.askopenfilename(
            initialdir=profiles_dir, 
            title="Sélectionnez un profil",
            filetypes=(("Fichiers texte", "*.txt"),)
        )
        
        if file_path:
            profile_name = os.path.splitext(os.path.basename(file_path))[0]
            if profile_name == "last_profile":
                messagebox.showerror("Erreur", "Veuillez sélectionner un fichier de profil de joueur.")
                return
                
            self.app.change_profile(profile_name)
            self.title_label.config(text=f"Profil Actuel : {profile_name}")
            messagebox.showinfo("Succès", f"Profil chargé : {profile_name}")
            
    def on_create_profile(self):
        """Demande un nom et crée un nouveau profil complet"""
        name = simpledialog.askstring("Nouveau joueur", "Entrez votre nom :", parent=self.root)
        if not name:
            return
            
        profiles_dir = get_profiles_dir()
        profile_path = os.path.join(profiles_dir, f"{name}.txt")
        
        if os.path.exists(profile_path):
            messagebox.showerror("Erreur", "Un profil avec ce nom existe déjà.")
            return

        try:
            # Générer ligue et freakopedia
            adversaires = generate_ligue()
            freakopedia = {f["name"]: {"decouvert": False, "nombre de points": 0} for f in creatures}

            # Écriture du fichier
            with open(profile_path, "w", encoding="utf-8") as file:
                file.write("freaks=[]\n")
                file.write("current_freak=None\n")
                file.write(f"freakopedia={freakopedia}\n")
                file.write("barcode_scanned=[]\n")
                file.write("ligue_level=01\n")
                file.write("league={\n")
                for i, adv in enumerate(adversaires, start=1):
                    key = f"adversaire{i:02d}"
                    file.write(f"  {key}={adv['name']}|{adv['type']}|{adv['stats']['attack']}|{adv['stats']['defense']}|{adv['stats']['pv']}\n")
                file.write("}\n")
            
            # Application du profil
            self.app.change_profile(name)
            self.title_label.config(text=f"Profil : {name}")
            messagebox.showinfo("Profil créé", f"Profil '{name}' créé avec succès !")
            
        except Exception as e:
            logging.error(f"Erreur création profil: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création du profil : {e}")
