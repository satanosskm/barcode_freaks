"""
Barcode Freaks - Entraînement
Permet d'entraîner le freak actuel
"""
import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import logging
from utils import get_profiles_dir, get_image_path
from screens.base import Screen

class TrainingScreen(Screen):
    """Écran d'entraînement"""
    
    def setup(self):
        """Configure l'écran d'entraînement avec le nouveau design 'Dojo'"""
        self.root.title("Entraînement - Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Charger les données nécessaires
        try:
            self.profile_path = self.app.get_profile_path()
            if not self.profile_path or not os.path.exists(self.profile_path):
                raise FileNotFoundError("Profil introuvable")
            
            self.current_freak_id = self.load_current_id()
            if not self.current_freak_id or self.current_freak_id == "None":
                self.show_no_freak_message()
                return
                
            self.freak_details = self.load_freak_details(self.current_freak_id)
            self.species_points = self.load_species_points(self.freak_details['name'])
            self.league_level = self.load_league_level()
            self.can_train = self.check_can_train()
            
            self.create_widgets()
        except Exception as e:
            logging.error(f"Erreur initialisation entraînement: {e}")
            self.back_to_menu()
            
    def load_current_id(self):
        """Charge l'ID du freak actuel"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("current_freak="):
                    return line.strip().split("=")[1]
        return None
        
    def load_freak_details(self, freak_id):
        """Charge les détails du freak depuis le profil"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("freaks=["):
                    content = line[8:].strip("[]\n ")
                    if not content: continue
                    freak_lines = content.split(",")
                    for freak_line in freak_lines:
                        freak_line = freak_line.strip()
                        if freak_line.startswith(freak_id):
                            parts = freak_line.split("|")
                            if len(parts) == 7:
                                return {
                                    "id": parts[0],
                                    "name": parts[1],
                                    "type": parts[2],
                                    "attack": int(parts[3]),
                                    "defense": int(parts[4]),
                                    "pv": int(parts[5]),
                                    "level": parts[6].split("_")[1]
                                }
        raise ValueError(f"Détails introuvables pour {freak_id}")
        
    def load_species_points(self, species_name):
        """Charge les points de l'espèce"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("freakopedia="):
                    # Utilisation de eval sécurisée ou parsing manuel si nécessaire
                    # Ici on garde la logique d'origine mais en mode propre
                    try:
                        f_data = eval(line.split("=", 1)[1].strip())
                        if species_name in f_data:
                            return f_data[species_name].get("nombre de points", 0)
                    except: pass
        return 0
        
    def load_league_level(self):
        """Charge le niveau de ligue"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("ligue_level="):
                    return line.strip().split("=")[1]
        return "01"
        
    def check_can_train(self):
        """Vérifie si l'entraînement est possible"""
        return int(self.freak_details['level']) < int(self.league_level) and \
               int(self.freak_details['level']) < int(self.species_points)
               
    def create_widgets(self):
        """Crée l'interface utilisateur moderne avec le design 'Soft Dark'"""
        # Conteneur principal centré
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- CARTE D'ENTRAÎNEMENT ---
        card = tk.Frame(main_container, bg=self.CARD_BG, padx=40, pady=40, highlightthickness=1, highlightbackground="#1A1C1E")
        card.pack()

        # Titre et Infos
        tk.Label(card, text="CENTRE D'ENTRAÎNEMENT", font=self.FONT_TITLE, bg=self.CARD_BG, fg=self.PRIMARY).pack()
        
        info_row = tk.Frame(card, bg=self.CARD_BG)
        info_row.pack(pady=(10, 30))
        tk.Label(info_row, text=f"Points d'espèce : {self.species_points}", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.ACCENT).pack(side="left", padx=10)
        tk.Label(info_row, text=f"Rang Ligue : {self.league_level}", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.SECONDARY).pack(side="left", padx=10)

        # Corps de la carte
        body = tk.Frame(card, bg=self.CARD_BG)
        body.pack()

        # Image
        image_name = self.freak_details['name']
        image_path = get_image_path(f"{image_name.lower()}.png")
        if os.path.exists(image_path):
            img = Image.open(image_path).convert("RGBA")
            # Créer un fond blanc pour le PNG transparent
            white_bg = Image.new("RGBA", img.size, "WHITE")
            white_bg.paste(img, (0, 0), img)
            img = white_bg.convert("RGB").resize((400, 400), Image.LANCZOS)
            self.freak_photo = ImageTk.PhotoImage(img)
            tk.Label(body, image=self.freak_photo, bg="#FFFFFF").pack(side="left", padx=(0, 40))
        else:
            self.freak_photo = None

        # Stats Column
        stats_col = tk.Frame(body, bg=self.CARD_BG)
        stats_col.pack(side="left", fill="both")

        tk.Label(stats_col, text=self.freak_details['name'].upper(), font=self.FONT_SUBTITLE, bg=self.CARD_BG, fg=self.PRIMARY).pack(anchor="w")
        self.level_label = tk.Label(stats_col, text=f"NIVEAU ACTUEL : {self.freak_details['level']}", font=("Segoe UI", 12, "bold"), bg=self.CARD_BG, fg=self.ACCENT)
        self.level_label.pack(anchor="w", pady=(0, 20))

        stats_box = tk.Frame(stats_col, bg="#0F1113", padx=20, pady=20, highlightthickness=1, highlightbackground="#1A1C1E")
        stats_box.pack(fill="x")
        
        self.stats_labels = {}
        for stat in ["attack", "defense", "pv"]:
            row = tk.Frame(stats_box, bg="#0F1113")
            row.pack(fill="x", pady=5)
            tk.Label(row, text=stat.upper() if stat != "pv" else "POINTS DE VIE", font=("Segoe UI", 9, "bold"), bg="#0F1113", fg=self.SECONDARY).pack(side="left")
            label = tk.Label(row, text=str(self.freak_details[stat]), font=("Segoe UI", 12, "bold"), bg="#0F1113", fg=self.PRIMARY)
            label.pack(side="right")
            self.stats_labels[stat] = label

        # Boutons d'entraînement
        tk.Label(card, text="AMÉLIORER UNE CAPACITÉ :", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.SECONDARY).pack(pady=(30, 10))
        
        btn_frame = tk.Frame(card, bg=self.CARD_BG)
        btn_frame.pack()
        
        self.train_buttons = []
        for text, stat in [("FORCE", "attack"), ("DÉFENSE", "defense"), ("ENDURANCE", "pv")]:
            # Déterminer la couleur spécifique pour chaque stat
            if stat == "attack": btn_color = self.DANGER
            elif stat == "defense": btn_color = self.ACCENT
            else: btn_color = self.SUCCESS
            
            # Si pas d'entraînement possible, griser (mais on garde la couleur de base pour l'instant, le disable gère le gris)
            # Note: create_button gère le style, ici on passe la couleur "active" désirée
            
            btn = self.create_button(btn_frame, text, lambda s=stat: self.train_freak(s), color=btn_color)
            btn.pack(side="left", padx=5)
            if not self.can_train: btn.button.config(state="disabled")
            self.train_buttons.append(btn)

        # Feedbacks
        self.result_label = tk.Label(card, text="", font=("Segoe UI", 11, "bold"), bg=self.CARD_BG, fg=self.PRIMARY)
        self.result_label.pack(pady=(20, 0))
        
        self.gain_label = tk.Label(card, text="", font=("Segoe UI", 18, "bold"), bg=self.CARD_BG, fg=self.SUCCESS)
        self.gain_label.pack()

        # --- ACTIONS BAS ---
        actions_frame = tk.Frame(main_container, bg=self.BG_COLOR, pady=30)
        actions_frame.pack(fill="x")
        self.create_button(actions_frame, "RETOUR AU MENU", self.back_to_menu, color=self.SECONDARY).pack()
        
    def train_freak(self, stat_to_update):
        """Exécute l'entraînement"""
        if not self.can_train:
            return
            
        roll = random.randint(1, 3)
        increment = roll if stat_to_update != "pv" else roll * 2
        message = {1: "Entraînement faible !", 2: "Entraînement moyen !", 3: "Super entraînement !"}[roll]
        
        # Mettre à jour fichier
        self.update_profile_file(stat_to_update, increment)
        
        # Recharger data
        self.freak_details = self.load_freak_details(self.current_freak_id)
        self.can_train = self.check_can_train()
        
        # Update UI
        for stat, label in self.stats_labels.items():
            label.config(text=str(self.freak_details[stat]))
            
        self.level_label.config(text=f"NIVEAU ACTUEL : {self.freak_details['level']}")
        
        gain_message = f"+ {increment} {stat_to_update.upper()} !"
        self.gain_label.config(text=gain_message)
        self.result_label.config(text=f"{message}\nVotre freak a progressé !")
        
        if not self.can_train:
            for btn in self.train_buttons:
                btn.button.config(state="disabled")
            self.result_label.config(text=self.result_label.cget("text") + "\nLimite d'entraînement atteinte.")
            
    def update_profile_file(self, stat_to_update, increment):
        """Écrit les nouvelles stats dans le fichier"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        for i, line in enumerate(lines):
            if line.startswith("freaks=["):
                content = line[8:].strip("[]\n ")
                freak_lines = content.split(",")
                for j, freak_line in enumerate(freak_lines):
                    freak_line = freak_line.strip()
                    if freak_line.startswith(self.current_freak_id):
                        parts = freak_line.split("|")
                        if stat_to_update == "attack": parts[3] = str(int(parts[3]) + increment)
                        elif stat_to_update == "defense": parts[4] = str(int(parts[4]) + increment)
                        elif stat_to_update == "pv": parts[5] = str(int(parts[5]) + increment)
                        
                        curr_lvl = int(parts[6].split("_")[1])
                        parts[6] = f"lv_{curr_lvl + 1:02}"
                        freak_lines[j] = "|".join(parts)
                        break
                lines[i] = f"freaks=[{', '.join(freak_lines)}]\n"
                break
                
        with open(self.profile_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
            
    def show_no_freak_message(self):
        """Affiche un message si aucun freak n'est sélectionné"""
        msg_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        msg_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        card = tk.Frame(msg_frame, bg=self.CARD_BG, padx=50, pady=50, highlightthickness=1, highlightbackground="#1A1C1E")
        card.pack()
        
        tk.Label(card, text="AUCUN FREAK SÉLECTIONNÉ", font=self.FONT_SUBTITLE, bg=self.CARD_BG, fg=self.DANGER).pack(pady=(0, 30))
        tk.Label(card, text="Allez dans votre collection pour choisir\nun freak à entraîner.", font=self.FONT_NORMAL, bg=self.CARD_BG, fg=self.PRIMARY).pack(pady=(0, 40))
        
        self.create_button(card, "RETOUR AU MENU", self.back_to_menu, color=self.SECONDARY).pack()
