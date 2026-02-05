import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import logging
from utils import get_image_path
from screens.base import Screen

class MenuScreen(Screen):
    """Écran du menu principal (Thème Soft Dark)"""
    
    def setup(self):
        """Configure le menu avec le nouveau design 'Soft Dark'"""
        self.root.title("Barcode Freaks - Menu Principal")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Charger le profil si pas déjà chargé
        if not self.app.profile_name:
            self.app.profile_name = self.create_new_profile()
        
        # Conteneur principal centré
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- LOGO & TITRE ---
        logo_card = tk.Frame(main_container, bg=self.CARD_BG, padx=40, pady=40, highlightthickness=1, highlightbackground="#1A1C1E")
        logo_card.grid(row=0, column=0, padx=40)
        
        try:
            logo_path = get_image_path("logo_BF.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path).resize((400, 400))
                self.logo_tk = ImageTk.PhotoImage(img)
                tk.Label(logo_card, image=self.logo_tk, bg=self.CARD_BG).pack()
        except: pass

        tk.Label(logo_card, text="BARCODE FREAKS", font=self.FONT_TITLE, bg=self.CARD_BG, fg=self.PRIMARY).pack(pady=(20, 0))
        tk.Label(logo_card, text=f"JOUEUR : {self.app.profile_name.upper()}", font=("Segoe UI", 12, "bold"), bg=self.CARD_BG, fg=self.ACCENT).pack()

        # --- BOUTONS ---
        btn_frame = tk.Frame(main_container, bg=self.BG_COLOR)
        btn_frame.grid(row=0, column=1, padx=40)

        menu_items = [
            ("SCANNER", self.open_scan, self.SUCCESS),
            ("FREAKOPÉDIA", self.open_freakopedia, self.ACCENT),
            ("MES FREAKS", self.open_stockage, self.ACCENT),
            ("LIGUE BARCODE FREAKS", self.open_ligue, self.ACCENT),
            ("ENTRAÎNEMENT", self.open_training, self.ACCENT),
            ("PROFIL", self.open_profil, self.SECONDARY),
            ("QUITTER", self.root.quit, self.DANGER),
        ]

        for text, cmd, color in menu_items:
            # Largeur uniforme de 320px pour tous les boutons du menu
            self.create_button(btn_frame, text, cmd, color=color, width=320).pack(pady=10)

    def create_new_profile(self):
        from screens.profile import ProfileScreen
        # Cette logique devrait être dans app.py idéalement, mais on garde la structure existante
        return self.app.profile_name # Fallback simple pour cet exemple

    def open_scan(self):
        from screens.scan import ScanScreen
        self.app.show_screen(ScanScreen)

    def open_stockage(self):
        from screens.storage import StorageScreen
        self.app.show_screen(StorageScreen)

    def open_freakopedia(self):
        from screens.freakopedia import FreakopediaScreen
        self.app.show_screen(FreakopediaScreen)

    def open_ligue(self):
        from screens.league import LeagueScreen
        self.app.show_screen(LeagueScreen)

    def open_training(self):
        from screens.training import TrainingScreen
        self.app.show_screen(TrainingScreen)

    def open_profil(self):
        from screens.profile import ProfileScreen
        self.app.show_screen(ProfileScreen)
