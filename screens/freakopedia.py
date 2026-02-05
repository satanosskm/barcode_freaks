import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import logging
import functools
from utils import get_image_path
from screens.base import Screen
from creatures import creatures

class FreakopediaScreen(Screen):
    """Écran de la Freakopedia (Grille Centrée, Thème Soft Dark, 8 Colonnes)"""
    
    def setup(self):
        """Configure la Freakopedia avec le nouveau design 'Encyclopédie Premium'"""
        self.root.title("Freakopedia - Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Charger données
        self.freakopedia_data = self.load_freakopedia_data()
        
        # --- HEADER / TITRE ---
        header = tk.Frame(self.root, bg=self.BG_COLOR, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="FREAKOPÉDIA", font=self.FONT_TITLE, bg=self.BG_COLOR, fg=self.PRIMARY).pack()
        
        # --- BOUTON RETOUR (FIXE EN BAS) ---
        bottom_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=20)
        bottom_frame.pack(side="bottom", fill="x")
        self.create_button(bottom_frame, "RETOUR AU MENU", self.back_to_menu, color=self.DANGER).pack()

        # --- GRID SCROLLABLE ---
        container = tk.Frame(self.root, bg=self.BG_COLOR)
        container.pack(expand=True, fill="both", padx=40)

        self.canvas = tk.Canvas(container, bg=self.BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview, width=15)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BG_COLOR)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.image_refs = []
        self.display_grid()

    def _on_canvas_configure(self, event):
        """Gère le centrage du contenu lors du scroll"""
        width = event.width
        self.canvas.itemconfig(self.canvas_window, width=width)
        self.canvas.coords(self.canvas_window, width // 2, 0)

    def load_freakopedia_data(self):
        """Charge les données de découverte depuis le profil"""
        profile_path = self.app.get_profile_path()
        if not profile_path or not os.path.exists(profile_path): return {}
        try:
            with open(profile_path, "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("freakopedia="):
                        return eval(line.split("=", 1)[1].strip())
        except Exception as e:
            logging.error(f"Erreur Freakopedia: {e}")
        return {}

    def display_grid(self):
        """Affiche la grille des freaks avec un look premium (8 colonnes)"""
        for w in self.scrollable_frame.winfo_children(): w.destroy()
        self.image_refs = []
        
        row, col = 0, 0
        max_cols = 8 # Plus dense
        card_w, card_h = 170, 230
        img_size = 120
        
        for i in range(max_cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

        for creature in creatures:
            name = creature["name"]
            data = self.freakopedia_data.get(name, {"decouvert": False, "nombre de points": 0})
            is_disc = data.get("decouvert", False)
            
            # Conteneur de la carte (Design Soft Dark)
            card_bg = "#FFFFFF" if is_disc else self.BG_COLOR
            card = tk.Frame(
                self.scrollable_frame, 
                width=card_w, 
                height=card_h, 
                bg=card_bg, 
                highlightthickness=1, 
                highlightbackground="#34495E" if is_disc else "#1A1C1E",
                cursor="hand2" if is_disc else ""
            )
            card.grid(row=row, column=col, padx=8, pady=12)
            card.grid_propagate(False)

            try:
                if is_disc:
                    path = get_image_path(f"{name.lower()}.png")
                    if os.path.exists(path):
                        img = Image.open(path).convert("RGBA")
                        white_bg = Image.new("RGBA", img.size, "WHITE")
                        white_bg.paste(img, (0, 0), img)
                        img = white_bg.convert("RGB").resize((img_size, img_size), Image.LANCZOS)
                    else:
                        img = Image.new("RGB", (img_size, img_size), "#FFFFFF")
                else:
                    img = Image.new("RGB", (img_size, img_size), "#0F1113")
                
                photo = ImageTk.PhotoImage(img)
                self.image_refs.append(photo)
                tk.Label(card, image=photo, bg=card_bg).pack(pady=0, anchor="n")
            except: pass
            
            # Nom et Points
            label_text = name.upper() if is_disc else "??????"
            label_color = self.BG_COLOR if is_disc else "#2C3E50"
            tk.Label(card, text=label_text, font=("Segoe UI", 10, "bold"), bg=card_bg, fg=label_color).pack()
            
            if is_disc:
                tk.Label(card, text=f"{data.get('nombre de points', 0)} PTS", font=("Segoe UI", 8, "bold"), bg=card_bg, fg=self.SUCCESS).pack(pady=2)
                # Click events
                for widget in [card] + list(card.winfo_children()):
                    widget.bind("<Button-1>", functools.partial(self.open_fiche, name=name))
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def open_fiche(self, event, name):
        """Ouvre la fiche détaillée d'un freak découvert"""
        from screens.pedia_visu import PediaVisualizerScreen
        self.app.show_screen(PediaVisualizerScreen, creature_name=name)
