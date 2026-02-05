"""
Barcode Freaks - Scanner de codes-barres
Écran pour scanner et générer des freaks à partir de codes-barres
"""
import tkinter as tk
from tkinter import PhotoImage, StringVar, Label, Menu, Button, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
from pyzbar.pyzbar import decode
import os
from creatures import creatures
import hashlib
import random
import logging
import functools
from utils import get_profiles_dir, get_image_path
from screens.base import Screen

class ScanScreen(Screen):
    """Écran de scan de codes-barres (Logique Originale SHA256 Restaurée)"""
    
    def setup(self):
        """Configure l'écran de scan avec le nouveau design"""
        self.root.title("Scanner - Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        # Variables d'instance
        self.barcode_var = StringVar()
        self.default_image_tk = None
        self.last_generated_creature = None
        
        # Créer l'interface
        self.create_widgets()
        
    def create_widgets(self):
        """Crée l'interface avec le look 'Soft Dark'"""
        # Conteneur principal centré
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- SECTION SAISIE ---
        search_card = tk.Frame(main_container, bg=self.CARD_BG, padx=30, pady=20, highlightthickness=1, highlightbackground="#1A1C1E")
        search_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            search_card, 
            text="SCANNER UN CODE-BARRES", 
            font=self.FONT_SUBTITLE, 
            bg=self.CARD_BG, 
            fg=self.PRIMARY
        ).pack(side="left", padx=(0, 20))
        
        self.barcode_entry = tk.Entry(
            search_card, 
            textvariable=self.barcode_var, 
            font=("Segoe UI", 16), 
            bg="#0F1113",
            fg="white",
            insertbackground="white",
            width=20,
            relief="flat",
            borderwidth=0
        )
        self.barcode_entry.pack(side="left", padx=10, pady=10)
        
        self.create_button(search_card, "GÉNÉRER", self.on_manual_generate, color=self.SUCCESS).pack(side="left", padx=10)

        # --- SECTION RÉSULTAT (CARTE CENTRALE) ---
        result_card = tk.Frame(main_container, bg=self.CARD_BG, padx=40, pady=40, highlightthickness=1, highlightbackground="#1A1C1E")
        result_card.pack()
        
        # Image
        try:
            logo_path = get_image_path("logo_BF.png")
            img = Image.open(logo_path).resize((400, 400)) if os.path.exists(logo_path) else Image.new("RGB", (400, 400), "#0F1113")
            self.default_image_tk = ImageTk.PhotoImage(img)
        except Exception:
            self.default_image_tk = ImageTk.PhotoImage(Image.new("RGB", (400, 400), "#0F1113"))
        
        self.image_label = Label(result_card, image=self.default_image_tk, bg=self.CARD_BG)
        self.image_label.pack(side="left", padx=(0, 40))
        
        # Infos Freak
        self.info_container = tk.Frame(result_card, bg=self.CARD_BG)
        self.info_container.pack(side="left", fill="both", expand=True)
        
        self.name_label = Label(self.info_container, text="En attente...", font=self.FONT_TITLE, bg=self.CARD_BG, fg=self.PRIMARY, anchor="w")
        self.name_label.pack(fill="x", pady=(0, 10))
        
        self.type_label = Label(self.info_container, text="TYPE : ---", font=self.FONT_SUBTITLE, bg=self.CARD_BG, fg=self.SECONDARY, anchor="w")
        self.type_label.pack(fill="x", pady=5)
        
        self.stats_label = Label(self.info_container, text="STATS : ---", font=self.FONT_NORMAL, bg=self.CARD_BG, fg=self.SECONDARY, anchor="w")
        self.stats_label.pack(fill="x", pady=(0, 30))
        
        # Bouton Adoption
        self.adopt_button_frame = self.create_button(self.info_container, "ADOPTER CE FREAK", self.adopt_freak, color=self.SUCCESS)
        self.adopt_button_frame.pack(anchor="w")
        # Désactiver le bouton interne
        for child in self.adopt_button_frame.winfo_children():
            if isinstance(child, tk.Button):
                self.adopt_button = child
                self.adopt_button.config(state="disabled")

        # --- SECTION ACTIONS BAS ---
        actions_container = tk.Frame(main_container, bg=self.BG_COLOR)
        actions_container.pack(fill="x", pady=30)
        
        self.create_button(actions_container, "SCANNER IMAGE", self.scan_barcode_image, color=self.ACCENT).pack(side="left", padx=10)
        
        self.message_label = Label(actions_container, text="", font=self.FONT_NORMAL, bg=self.BG_COLOR, fg=self.SUCCESS)
        self.message_label.pack(side="left", padx=40, expand=True)

        self.create_button(actions_container, "RETOUR MENU", self.back_to_menu, color=self.DANGER).pack(side="right", padx=10)
        
        # Binds
        self.root.bind("<Return>", lambda e: self.on_manual_generate())
        self.barcode_entry.bind("<Return>", lambda e: self.on_manual_generate())
        self.barcode_entry.focus_set()

    def validate_ean_checksum(self, barcode):
        """Vérifie la clé de contrôle EAN-13 ou EAN-8 (Logique Originale)"""
        if not barcode or not barcode.isdigit(): return False
        if len(barcode) == 13:
            checksum = sum(int(barcode[i]) * (3 if i % 2 else 1) for i in range(12))
            check_digit = (10 - (checksum % 10)) % 10
            return check_digit == int(barcode[-1])
        elif len(barcode) == 8:
            checksum = sum(int(barcode[i]) * (3 if i % 2 == 0 else 1) for i in range(7))
            check_digit = (10 - (checksum % 10)) % 10
            return check_digit == int(barcode[-1])
        return False

    def _on_canvas_configure(self, event):
        """Recentrer le frame scrollable horizontalement et l'étendre"""
        width = event.width
        self.canvas.itemconfig(self.canvas_window, width=width)
        self.canvas.coords(self.canvas_window, width // 2, 0)

    def on_manual_generate(self):
        barcode = self.barcode_var.get().strip()
        self.on_decode_success(barcode)

    def on_decode_success(self, barcode):
        """Appelé quand un code-barres est détecté"""
        if not (len(barcode) in [8, 13] and self.validate_ean_checksum(barcode)):
            self.message_label.config(text=f"ERREUR : Code-barre non valide ! ({barcode})", fg="red")
            self.reset_display()
            return

        self.message_label.config(text=f"Code-barres détecté : {barcode}", fg="blue")
        self.generate_creature(barcode)

    def generate_creature(self, barcode):
        """Génère une créature à partir du code-barres (Logique sha256 STRICTEMENT originale)"""
        hash_value = hashlib.sha256(barcode.encode()).hexdigest()
        creature_index = int(hash_value[:8], 16) % len(creatures)
        selected_creature = creatures[creature_index]

        name = selected_creature["name"]
        
        stats = {
            "attack": int(hash_value[8:16], 16) % 20 + 1,
            "defense": int(hash_value[16:24], 16) % 20 + 1,
            "pv": int(hash_value[24:32], 16) % 21 + 20
        }
        
        self.last_generated_creature = {
            "name": name,
            "type": selected_creature["type"],
            "attack": stats["attack"],
            "defense": stats["defense"],
            "pv": stats["pv"],
            "barcode": barcode
        }

        # Mise à jour du profil (Points et scan unique)
        profile_path = self.app.get_profile_path()
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Charger barcode_scanned
            scanned = []
            for line in lines:
                if line.startswith("barcode_scanned="):
                    scanned = eval(line.split("=")[1].strip())
                    break
            
            if barcode not in scanned:
                scanned.append(barcode)
                # Gain de points
                for i, line in enumerate(lines):
                    if line.startswith("freakopedia="):
                        data = eval(line.split("=", 1)[1].strip())
                        if name in data:
                            if not data[name]["decouvert"]:
                                data[name]["decouvert"] = True
                            data[name]["nombre de points"] += 5
                            self.message_label.config(text=f"Tu as gagné 5 points {name} !", fg="green")
                        lines[i] = f"freakopedia={data}\n"
                        break
                
                # Mise à jour barcode_scanned dans les lignes
                for i, line in enumerate(lines):
                    if line.startswith("barcode_scanned="):
                        lines[i] = f"barcode_scanned={scanned}\n"
                        break
                
                with open(profile_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            else:
                self.message_label.config(text=f"Déjà scanné : {barcode}", fg="darkred")

        self.show_creature(name, selected_creature["type"], stats)

    def show_creature(self, name, type_label, stats):
        """Affiche les infos de la créature"""
        img_path = get_image_path(f"{name.lower()}.png")
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path).convert("RGBA")
                # Créer un fond blanc pour le PNG transparent
                white_bg = Image.new("RGBA", img.size, "WHITE")
                white_bg.paste(img, (0, 0), img)
                img = white_bg.convert("RGB").resize((400, 400), Image.LANCZOS)
            else:
                img = self.generate_placeholder(type_label, (400, 400))
            self.current_img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_img_tk, bg="#FFFFFF") # Force le BG blanc du label aussi
        except: pass
        
        self.name_label.config(text=f"Nom : {name}")
        self.type_label.config(text=f"Type : {type_label.capitalize()}")
        self.stats_label.config(text=f"Stats : Attack={stats['attack']}, Defense={stats['defense']}, PV={stats['pv']}")
        self.adopt_button.config(state="normal")

    def reset_display(self):
        self.image_label.config(image=self.default_image_tk)
        self.name_label.config(text="Nom :")
        self.type_label.config(text="Type :")
        self.stats_label.config(text="Stats :")
        self.adopt_button.config(state="disabled")

    def adopt_freak(self):
        if not self.last_generated_creature: return
        
        profile_path = self.app.get_profile_path()
        if not os.path.exists(profile_path): return
        
        with open(profile_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        c = self.last_generated_creature
        # ID Unique original-style
        creature_id = f"f_{c['barcode']}_{random.randint(100, 999)}"
        new_entry = f"{creature_id}|{c['name']}|{c['type']}|{c['attack']}|{c['defense']}|{c['pv']}|lv_01"
        
        for i, line in enumerate(lines):
            if line.startswith("freaks=["):
                content = line[8:].strip("[]\n ")
                freaks = [f.strip() for f in content.split(",") if f.strip()]
                freaks.append(new_entry)
                lines[i] = f"freaks=[{', '.join(freaks)}]\n"
                break
        
        for i, line in enumerate(lines):
            if line.startswith("current_freak="):
                if line.split("=")[1].strip() == "None":
                    lines[i] = f"current_freak={creature_id}\n"
                break
                
        with open(profile_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
            
        # Message de succès intégré (pas de popup, pas de redirection)
        self.message_label.config(text=f"Succès ! {c['name']} a rejoint votre équipe.", fg=self.SUCCESS)
        self.adopt_button.config(state="disabled", text="ADOPTÉ !")

    def scan_barcode_image(self):
        """Scanne une image"""
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if not file_path: return
        try:
            img = Image.open(file_path)
            decoded = decode(img)
            if decoded:
                data = decoded[0].data.decode("utf-8")
                self.barcode_var.set(data)
                self.on_decode_success(data)
            else:
                self.message_label.config(text="Aucun code EAN trouvé dans l'image", fg="red")
        except Exception as e:
            logging.error(f"Erreur scan image: {e}")
            self.message_label.config(text="Erreur lors de la lecture de l'image", fg="red")

    def generate_placeholder(self, type_label, size=(100, 100)):
        img = Image.new("RGB", size, "#dddddd")
        draw = ImageDraw.Draw(img)
        draw.text((size[0]//4, size[1]//2), f"IMAGE {type_label.upper()}", fill="black")
        return img
