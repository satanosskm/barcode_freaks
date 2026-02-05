import tkinter as tk
from PIL import Image, ImageTk
import os
import logging
from utils import get_image_path
from screens.base import Screen
from creatures import creatures

class PediaVisualizerScreen(Screen):
    """Écran de détails d'une espèce de la Freakopedia"""
    
    def __init__(self, root, app, creature_name=None):
        self.creature_name = creature_name
        super().__init__(root, app)
        
    def setup(self):
        """Configure la fiche Freakopedia avec le nouveau design 'Carte de Collection'"""
        self.root.title(f"Fiche - {self.creature_name}")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Charger les données
        creature_info = next((c for c in creatures if c["name"] == self.creature_name), None)
        pedia_data = self.load_pedia_data()
        points = pedia_data.get(self.creature_name, {}).get("nombre de points", 0)
        
        if not creature_info:
            self.back_to_pedia()
            return

        # Conteneur principal centré
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- CARTE DU FREAK ---
        card = tk.Frame(main_container, bg=self.CARD_BG, padx=40, pady=40, highlightthickness=1, highlightbackground="#1A1C1E")
        card.pack()

        # En-tête
        header = tk.Frame(card, bg=self.CARD_BG)
        header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text=self.creature_name.upper(), font=self.FONT_TITLE, bg=self.CARD_BG, fg=self.PRIMARY).pack(side="left")
        tk.Label(header, text=f"{points} POINTS", font=self.FONT_SUBTITLE, bg=self.CARD_BG, fg=self.SUCCESS).pack(side="right")

        # Corps
        body = tk.Frame(card, bg=self.CARD_BG)
        body.pack()

        # Image
        image_path = get_image_path(f"{self.creature_name.lower()}.png")
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path).convert("RGBA")
                # Créer un fond blanc pour le PNG transparent
                white_bg = Image.new("RGBA", img.size, "WHITE")
                white_bg.paste(img, (0, 0), img)
                img = white_bg.convert("RGB").resize((400, 400), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(body, image=self.photo, bg="#FFFFFF").pack(side="left", padx=(0, 40))
        except Exception as e:
            logging.error(f"Erreur image pedia: {e}")

        # Infos
        info_col = tk.Frame(body, bg=self.CARD_BG)
        info_col.pack(side="left", fill="both", expand=True)

        # Type Badge
        t_type = creature_info['type'].capitalize()
        bg_color = self.TYPE_COLORS.get(t_type, self.ACCENT)
        fg_color = "black" if t_type in ["Tech", "Normal"] else "white"
        
        type_badge = tk.Frame(info_col, bg=bg_color, padx=15, pady=5)
        type_badge.pack(anchor="w", pady=(0, 20))
        tk.Label(type_badge, text=t_type.upper(), font=("Segoe UI", 10, "bold"), bg=bg_color, fg=fg_color).pack()

        desc_text = creature_info.get("description", "Aucune description disponible.")
        tk.Label(info_col, text=desc_text, font=("Segoe UI", 11, "italic"), bg=self.CARD_BG, fg=self.PRIMARY, 
                 wraplength=400, justify="left").pack(anchor="w", pady=(5, 30))

        # --- ACTION ---
        self.create_button(card, "RETOUR À FREAKOPEDIA", self.back_to_pedia, color=self.SECONDARY, width=None).pack(pady=(40, 0))

    def load_pedia_data(self):
        profile_path = self.app.get_profile_path()
        if not os.path.exists(profile_path): return {}
        with open(profile_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("freakopedia="):
                    return eval(line.split("=", 1)[1].strip())
        return {}

    def back_to_pedia(self):
        from screens.freakopedia import FreakopediaScreen
        self.app.show_screen(FreakopediaScreen)
