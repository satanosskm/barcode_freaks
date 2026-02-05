"""
Barcode Freaks - Ligue
Écran de sélection des adversaires de la ligue
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import logging
from utils import get_profiles_dir
from screens.base import Screen
from dictionnaire import adversaire_dict

class LeagueScreen(Screen):
    """Écran de la ligue"""
    
    def setup(self):
        """Configure l'écran de la ligue avec le nouveau design"""
        self.root.title("Ligue Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        try:
            self.profile_path = self.app.get_profile_path()
            if not self.profile_path or not os.path.exists(self.profile_path):
                raise FileNotFoundError("Profil introuvable")
                
            self.league_data = self.load_league()
            self.ligue_level = self.load_ligue_level()
            
            self.create_widgets()
        except Exception as e:
            logging.error(f"Erreur initialisation ligue: {e}")
            self.back_to_menu()
            
    def load_league(self):
        """Charge les adversaires de la ligue depuis le profil"""
        league = {}
        with open(self.profile_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            in_section = False
            for line in lines:
                line = line.strip()
                if line == "league={":
                    in_section = True
                elif in_section:
                    if line == "}":
                        break
                    if "=" in line:
                        key, value = line.split("=", 1)
                        league[key.strip()] = value.strip()
        return league
        
    def load_ligue_level(self):
        """Charge le niveau de ligue débloqué"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("ligue_level="):
                    return int(line.split("=")[1].strip())
        return 1
        
    def create_widgets(self):
        """Crée l'interface utilisateur moderne avec le design 'Soft Dark'"""
        # Conteneur principal
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- CARTE DE TOURNOI ---
        league_card = tk.Frame(main_container, bg=self.CARD_BG, padx=50, pady=40, highlightthickness=1, highlightbackground="#1A1C1E")
        league_card.pack()

        # Titre
        tk.Label(
            league_card, 
            text="LIGUE BARCODE FREAKS", 
            font=self.FONT_TITLE, 
            bg=self.CARD_BG,
            fg=self.PRIMARY
        ).pack(pady=(0, 10))
        
        tk.Label(
            league_card, 
            text=f"PROFIL : {self.app.profile_name.upper()}", 
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.ACCENT
        ).pack(pady=(0, 30))

        # Progression
        if self.ligue_level > 50:
            msg = "🏆 MAÎTRE DE LA LIGUE 🏆"
            tk.Label(league_card, text=msg, font=self.FONT_SUBTITLE, bg=self.CARD_BG, fg=self.SUCCESS).pack(pady=10)
            display_level = 50
        else:
            display_level = self.ligue_level
            tk.Label(league_card, text=f"RANG ACTUEL : {display_level} / 50", font=self.FONT_SUBTITLE, bg=self.CARD_BG, fg=self.PRIMARY).pack(pady=10)
            
        # Sélection de l'adversaire
        tk.Label(league_card, text="CHOISISSEZ VOTRE ADVERSAIRE :", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.SECONDARY).pack(pady=(20, 10))
        
        available_adversaries = [adversaire_dict[f"adversaire{i:02d}"] for i in range(1, display_level + 1)]
        self.adversaire_var = tk.StringVar(value=available_adversaries[-1])
        
        # Style pour la combobox (Sombre)
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style persistant pour la Combobox
        style.configure("TCombobox", 
                        fieldbackground="#000000",
                        background="#34495E", 
                        foreground="white",
                        arrowcolor="white",
                        font=("Segoe UI", 12))
        
        # Forcer le texte en blanc même lors de la sélection/focus
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#000000"), ("focus", "#000000")],
                  foreground=[("readonly", "white"), ("focus", "white")],
                  selectbackground=[("readonly", "#000000")],
                  selectforeground=[("readonly", "white")])
        
        self.adversaire_menu = ttk.Combobox(
            league_card, 
            textvariable=self.adversaire_var, 
            values=available_adversaries, 
            state="readonly", 
            width=30
        )
        self.adversaire_menu.pack(pady=10)
        
        # Bouton combat
        self.create_button(league_card, "⚔️ LANCER LE DUEL", self.on_combat_click, color=self.SUCCESS).pack(pady=30)
        
        # Actions bas
        actions_frame = tk.Frame(main_container, bg=self.BG_COLOR, pady=20)
        actions_frame.pack(fill="x")
        
        self.message_label = tk.Label(actions_frame, text="", font=self.FONT_NORMAL, bg=self.BG_COLOR, fg=self.DANGER)
        self.message_label.pack(pady=10)
        
        self.create_button(actions_frame, "RETOUR AU MENU", self.back_to_menu, color=self.DANGER).pack()
        
    def on_combat_click(self):
        """Gère le clic sur le bouton combat"""
        selected_display_name = self.adversaire_var.get()
        try:
            # Trouver la clé interne
            selected_key = next(key for key, value in adversaire_dict.items() if value == selected_display_name)
            
            # Normaliser format (adversaire01)
            if "_" in selected_key:
                # Si c'était déjà au bon format on ne touche pas, sinon on normalise
                pass
            
            if selected_key not in self.league_data:
                messagebox.showerror("Erreur", f"Données de l'adversaire {selected_key} introuvables.")
                return
                
            # Lancer le duel
            from screens.duel import DuelScreen
            self.app.show_screen(DuelScreen, adversaire_key=selected_key)
            
        except StopIteration:
            messagebox.showerror("Erreur", "Adversaire non reconnu.")
