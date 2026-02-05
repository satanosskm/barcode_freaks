import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import logging
import functools
from utils import get_image_path
from screens.base import Screen

class StorageScreen(Screen):
    """Écran de stockage des freaks (Grille Centrée, Sans Titre, Bouton Fixe, Scrollable)"""
    
    def setup(self):
        """Configure l'écran de stockage avec le nouveau design"""
        self.root.title("Mes Freaks - Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Données
        self.freaks = self.load_freaks()
        self.current_freak_id = self.load_current_freak_id()
        
        # --- HEADER / TITRE ---
        header = tk.Frame(self.root, bg=self.BG_COLOR, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="MES FREAKS", font=self.FONT_TITLE, bg=self.BG_COLOR, fg=self.PRIMARY).pack()
        
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
        self.display_freaks()

    def _on_canvas_configure(self, event):
        """Gère le centrage du contenu lors du scroll"""
        width = event.width
        self.canvas.itemconfig(self.canvas_window, width=width)
        self.canvas.coords(self.canvas_window, width // 2, 0)

    def load_freaks(self):
        """Charge les freaks depuis le profil"""
        profile_path = self.app.get_profile_path()
        if not os.path.exists(profile_path): return []
        freaks = []
        with open(profile_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("freaks="):
                    content = line[8:].strip("[]\n ")
                    if not content: break
                    items = [it.strip() for it in content.split(",") if it.strip()]
                    for it in items:
                        p = it.split("|")
                        if len(p) >= 7:
                            freaks.append({
                                "id": p[0], "name": p[1], "type": p[2],
                                "attack": p[3], "defense": p[4], "pv": p[5], "level": p[6].replace("lv_", "")
                            })
        return freaks

    def load_current_freak_id(self):
        """Récupère l'ID du freak actif"""
        profile_path = self.app.get_profile_path()
        if not os.path.exists(profile_path): return None
        with open(profile_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("current_freak="):
                    return line.split("=")[1].strip()
        return None

    def display_freaks(self):
        """Affiche les freaks sous forme de cartes modernes (8 colonnes)"""
        for w in self.scrollable_frame.winfo_children(): w.destroy()
        self.image_refs = []
        
        row, col = 0, 0
        max_cols = 8  # Plus dense
        card_w, card_h = 170, 240
        img_size = 120
        
        for i in range(max_cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

        for freak in self.freaks:
            is_curr = str(freak['id']) == str(self.current_freak_id)
            
            # Conteneur de la carte
            card = tk.Frame(
                self.scrollable_frame, 
                width=card_w, 
                height=card_h, 
                bg="#FFFFFF", 
                highlightthickness=2 if is_curr else 1, 
                highlightbackground=self.ACCENT if is_curr else "#34495E", 
                cursor="hand2"
            )
            card.grid(row=row, column=col, padx=8, pady=12)
            card.grid_propagate(False)
            
            # Image
            try:
                path = get_image_path(f"{freak['name'].lower()}.png")
                if os.path.exists(path):
                    img = Image.open(path).convert("RGBA")
                    # Créer un fond blanc pour le PNG transparent
                    white_bg = Image.new("RGBA", img.size, "WHITE")
                    white_bg.paste(img, (0, 0), img)
                    img = white_bg.convert("RGB").resize((img_size, img_size), Image.LANCZOS)
                else:
                    img = Image.new("RGB", (img_size, img_size), "#FFFFFF")
                
                photo = ImageTk.PhotoImage(img)
                self.image_refs.append(photo)
                tk.Label(card, image=photo, bg="#FFFFFF").pack(pady=0, anchor="n")
            except: pass
            
            # Infos
            tk.Label(card, text=freak['name'].upper(), font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg=self.BG_COLOR).pack()
            tk.Label(card, text=f"LV. {freak['level']}", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg=self.ACCENT).pack()
            
            stats_txt = f"ATK:{freak['attack']} DEF:{freak['defense']} PV:{freak['pv']}"
            tk.Label(card, text=stats_txt, font=("Segoe UI", 8), bg="#FFFFFF", fg="#7F8C8D").pack(pady=2)
            
            if is_curr:
                tk.Label(card, text="★ ACTIF ★", font=("Segoe UI", 8, "bold"), bg=self.ACCENT, fg="white").pack(side="bottom", fill="x")
            
            # Bind click event to card and all its children
            click_handler = functools.partial(self.open_visualizer, freak_id=freak['id'])
            card.bind("<Button-1>", click_handler)
            for widget in card.winfo_children():
                widget.bind("<Button-1>", click_handler)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def open_visualizer(self, event, freak_id):
        """Ouvre le visualisateur pour le freak sélectionné"""
        from screens.visualizer import VisualizerScreen
        self.app.show_screen(VisualizerScreen, freak_id=freak_id)
