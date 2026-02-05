import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import logging
from utils import get_image_path
from screens.base import Screen
from creatures import creatures

class VisualizerScreen(Screen):
    """Écran du visualisateur de freak (Fiche détaillée)"""
    
    def __init__(self, root, app, freak_id=None):
        self.freak_id = freak_id
        self.current_message = ""
        super().__init__(root, app)
    
    def setup(self):
        """Configure l'écran du visualisateur avec le nouveau design 'Carte de Collection'"""
        self.root.title("Visualizer - Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Charger les données du freak
        self.freak_data = self.load_freak_data()
        if not self.freak_data:
            messagebox.showerror("Erreur", "Données du freak introuvables.")
            self.back_to_storage()
            return

        # Conteneur principal centré
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- CARTE DU FREAK ---
        card = tk.Frame(main_container, bg=self.CARD_BG, padx=40, pady=40, highlightthickness=1, highlightbackground="#1A1C1E")
        card.pack()

        # En-tête de la carte (Nom et Niveau)
        header_frame = tk.Frame(card, bg=self.CARD_BG)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text=self.freak_data['name'].upper(), font=self.FONT_TITLE, bg=self.CARD_BG, fg=self.PRIMARY).pack(side="left")
        tk.Label(header_frame, text=f"LV. {self.freak_data['level']}", font=self.FONT_SUBTITLE, bg=self.CARD_BG, fg=self.ACCENT).pack(side="right")

        # Corps de la carte (Image et Stats)
        body_frame = tk.Frame(card, bg=self.CARD_BG)
        body_frame.pack()

        # Image à gauche
        image_name = self.freak_data['name'].lower()
        image_path = get_image_path(f"{image_name}.png")
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path).convert("RGBA")
                # Créer un fond blanc pour le PNG transparent
                white_bg = Image.new("RGBA", img.size, "WHITE")
                white_bg.paste(img, (0, 0), img)
                img = white_bg.convert("RGB").resize((400, 400), Image.LANCZOS)
            else:
                img = Image.new("RGB", (400, 400), "#FFFFFF")
            self.photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(body_frame, image=self.photo, bg="#FFFFFF")
            img_label.pack(side="left", padx=(0, 40))
        except Exception as e:
            logging.error(f"Erreur image: {e}")

        # Zone d'infos à droite
        info_column = tk.Frame(body_frame, bg=self.CARD_BG)
        info_column.pack(side="left", fill="both", expand=True)

        # Type
        t_type = self.freak_data['type'].capitalize()
        bg_color = self.TYPE_COLORS.get(t_type, self.ACCENT)
        fg_color = "black" if t_type in ["Tech", "Normal"] else "white"

        type_frame = tk.Frame(info_column, bg=bg_color, padx=15, pady=5)
        type_frame.pack(anchor="w", pady=(0, 20))
        tk.Label(type_frame, text=t_type.upper(), font=("Segoe UI", 10, "bold"), bg=bg_color, fg=fg_color).pack()

        # Stats (Grille propre)
        stats_box = tk.Frame(info_column, bg="#0F1113", padx=20, pady=20, highlightthickness=1, highlightbackground="#1A1C1E")
        stats_box.pack(fill="x", pady=(0, 20))
        
        stat_items = [("ATTAQUE", self.freak_data['attack']), 
                      ("DÉFENSE", self.freak_data['defense']), 
                      ("POINTS DE VIE", self.freak_data['pv'])]
                      
        for label, val in stat_items:
            row = tk.Frame(stats_box, bg="#0F1113")
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, font=("Segoe UI", 10, "bold"), bg="#0F1113", fg=self.SECONDARY).pack(side="left")
            tk.Label(row, text=str(val), font=("Segoe UI", 12, "bold"), bg="#0F1113", fg=self.PRIMARY).pack(side="right")

        # Description
        desc_label = tk.Label(info_column, text=self.freak_data.get('description', ''), 
                                font=("Segoe UI", 11, "italic"), bg=self.CARD_BG, fg=self.PRIMARY, 
                                wraplength=400, justify="left")
        desc_label.pack(fill="x", pady=10)

        # --- ACTIONS BAS ---
        actions_frame = tk.Frame(main_container, bg=self.BG_COLOR, pady=30)
        actions_frame.pack(fill="x")

        # Vérifier si c'est le freak actif
        p_id = self.load_current_freak_id()
        is_active = (str(p_id).strip() == str(self.freak_id).strip())
        
        if not is_active:
            self.create_button(actions_frame, "DÉFINIR COMME ACTIF", self.set_active, color=self.SUCCESS, width=None).pack(side="left", padx=10)
        else:
            # Badge "FREAK ACTIF" stylisé (Bouton désactivé)
            active_badge = self.create_button(actions_frame, "★ FREAK ACTIF ★", None, color=self.SUCCESS, width=None)
            active_badge.pack(side="left", padx=10)
            active_badge.button.config(state="disabled", disabledforeground="white")

        self.create_button(actions_frame, "RETOUR À MES FREAKS", self.back_to_storage, color=self.SECONDARY, width=None).pack(side="right", padx=10)

        # Message de succès temporaire
        if self.current_message:
            tk.Label(main_container, text=self.current_message, font=self.FONT_NORMAL, bg=self.BG_COLOR, fg=self.SUCCESS).pack(pady=10)
            self.current_message = ""

    def load_freak_data(self):
        """Charge les détails du freak depuis le profil"""
        profile_path = self.app.get_profile_path()
        if not profile_path or not os.path.exists(profile_path): return None
        
        with open(profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("freaks=["):
                    content = line[8:].strip("[]\n ")
                    freaks = content.split(",")
                    for f in freaks:
                        if f.strip().startswith(self.freak_id):
                            p = f.strip().split("|")
                            if len(p) == 7:
                                return {
                                    "id": p[0], "name": p[1], "type": p[2],
                                    "attack": p[3], "defense": p[4], "pv": p[5],
                                    "level": p[6].split("_")[1],
                                    "description": next((c["description"] for c in creatures if c["name"] == p[1]), "Pas de description.")
                                }
        return None

    def load_current_freak_id(self):
        profile_path = self.app.get_profile_path()
        with open(profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("current_freak="):
                    return line.strip().split("=")[1]
        return None

    def set_active(self):
        """Définit ce freak comme le freak actuel"""
        profile_path = self.app.get_profile_path()
        with open(profile_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        for i, line in enumerate(lines):
            if line.startswith("current_freak="):
                lines[i] = f"current_freak={self.freak_id}\n"
                break
        
        with open(profile_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
        
        self.current_message = f"{self.freak_data['name']} est maintenant votre freak actif !"
        self.clear_window() # Effacer l'ancien contenu avant de reconstruire
        self.setup() # Rafraîchir l'écran

    def back_to_storage(self):
        from screens.storage import StorageScreen
        self.app.show_screen(StorageScreen)
