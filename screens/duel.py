"""
Barcode Freaks - Duel
Écran de combat contre la ligue
"""
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import random
import os
import logging
from utils import get_image_path
from screens.base import Screen
from table import calculate_damage, is_effective

class DuelScreen(Screen):
    """Écran de combat 1v1"""
    
    def __init__(self, root, app, adversaire_key=None):
        self.adversaire_key = adversaire_key
        self.auto_attack_job = None
        super().__init__(root, app)
        
    def setup(self):
        """Configure le duel avec le nouveau design 'Arène moderne'"""
        self.root.title("Combat 1v1 - Barcode Freaks")
        self.root.configure(bg=self.BG_COLOR)
        self.root.state("zoomed")
        
        try:
            self.profile_path = self.app.get_profile_path()
            self.profile_name = self.app.profile_name
            
            # Charger les données
            self.load_combatants()
            
            # Variables Tkinter
            self.player_health_var = tk.StringVar(value=str(self.player_freak['stats']['pv']))
            self.opponent_health_var = tk.StringVar(value=str(self.opponent_freak['stats']['pv']))
            self.combat_log = tk.StringVar(value="LE COMBAT COMMENCE !")
            self.advantage_label_var = tk.StringVar(value="")
            self.turn = "player"
            
            self.create_widgets()
            self.start_combat()
            
        except Exception as e:
            logging.error(f"Erreur initialisation duel: {e}")
            self.back_to_league()
            
    def load_combatants(self):
        """Charge les stats du joueur et de l'adversaire"""
        # Adversaire
        league = self.load_league()
        if self.adversaire_key not in league:
            raise ValueError(f"Adversaire {self.adversaire_key} introuvable")
            
        adv_parts = league[self.adversaire_key].split("|")
        self.opponent_freak = {
            "name": adv_parts[0],
            "type": adv_parts[1],
            "stats": {
                "attack": int(adv_parts[2]),
                "defense": int(adv_parts[3]),
                "pv": int(adv_parts[4]),
                "max_pv": int(adv_parts[4])
            }
        }
        
        # Joueur
        current_id = self.load_current_id()
        if not current_id:
            raise ValueError("Aucun freak actuel")
            
        self.player_freak = self.load_freak_details(current_id)
        if self.player_freak:
            self.player_freak["stats"]["max_pv"] = self.player_freak["stats"]["pv"]
        
    def load_league(self):
        """Charge la ligue depuis le profil"""
        league = {}
        with open(self.profile_path, "r", encoding="utf-8") as file:
            in_section = False
            for line in file:
                line = line.strip()
                if line == "league={": in_section = True
                elif in_section:
                    if line == "}": break
                    if "=" in line:
                        k, v = line.split("=", 1)
                        league[k.strip()] = v.strip()
        return league
        
    def load_current_id(self):
        """Charge l'ID du freak actuel"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("current_freak="):
                    return line.strip().split("=")[1]
        return None
        
    def load_freak_details(self, freak_id):
        """Charge les détails du freak"""
        with open(self.profile_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("freaks=["):
                    content = line[8:].strip("[]\n ")
                    freaks = content.split(",")
                    for f in freaks:
                        if f.strip().startswith(freak_id):
                            p = f.strip().split("|")
                            if len(p) == 7:
                                return {
                                    "id": p[0],
                                    "name": p[1],
                                    "type": p[2],
                                    "stats": {
                                        "attack": int(p[3]),
                                        "defense": int(p[4]),
                                        "pv": int(p[5]),
                                    },
                                    "level_str": p[6]
                                }
        return None

    def load_freak_image(self, name, size=350):
        """Charge l'image d'un freak avec fond blanc forcé"""
        path = get_image_path(f"{name.lower()}.png")
        if os.path.exists(path):
            img = Image.open(path).convert("RGBA")
            # Créer un fond blanc pour le PNG transparent
            white_bg = Image.new("RGBA", img.size, "WHITE")
            white_bg.paste(img, (0, 0), img)
            img = white_bg.convert("RGB").resize((size, size), Image.LANCZOS)
        else:
            img = Image.new("RGB", (size, size), "#FFFFFF")
        return ImageTk.PhotoImage(img)

    def create_widgets(self):
        """Crée l'interface de combat moderne avec cartes face à face"""
        # --- ARENE (CENTERED) ---
        arena_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        arena_frame.place(relx=0.5, rely=0.45, anchor="center")
        
        # PLAYER CARD
        p_card = tk.Frame(arena_frame, bg="#FFFFFF", padx=30, pady=30, highlightthickness=1, highlightbackground="#1A1C1E")
        p_card.grid(row=0, column=0, padx=40)
        
        tk.Label(p_card, text=self.player_freak["name"].upper(), font=self.FONT_SUBTITLE, bg="#FFFFFF", fg=self.BG_COLOR).pack()
        tk.Label(p_card, text=f"LV. {self.player_freak['level_str'].split('_')[1]}", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg=self.ACCENT).pack()
        
        self.p_img_tk = self.load_freak_image(self.player_freak['name'])
        tk.Label(p_card, image=self.p_img_tk, bg="#FFFFFF").pack(pady=10)
        
        # Health Bar Simulation
        pv_frame_p = tk.Frame(p_card, bg="#FFFFFF", height=30)
        pv_frame_p.pack(fill="x", pady=10)
        tk.Label(pv_frame_p, text="PV", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg=self.BG_COLOR).pack(side="left", padx=10)
        tk.Label(pv_frame_p, textvariable=self.player_health_var, font=("Segoe UI", 16, "bold"), bg="#FFFFFF", fg=self.SUCCESS).pack(side="right", padx=10)

        # VS LABEL
        tk.Label(arena_frame, text="VS", font=("Segoe UI", 60, "italic", "bold"), bg=self.BG_COLOR, fg="#546E7A").grid(row=0, column=1)

        # OPPONENT CARD
        o_card = tk.Frame(arena_frame, bg="#FFFFFF", padx=30, pady=30, highlightthickness=1, highlightbackground="#1A1C1E")
        o_card.grid(row=0, column=2, padx=40)
        
        tk.Label(o_card, text=self.opponent_freak["name"].upper(), font=self.FONT_SUBTITLE, bg="#FFFFFF", fg=self.BG_COLOR).pack()
        tk.Label(o_card, text=f"RANG {self.adversaire_key[-2:]}", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg=self.DANGER).pack()
        
        self.o_img_tk = self.load_freak_image(self.opponent_freak['name'])
        tk.Label(o_card, image=self.o_img_tk, bg="#FFFFFF").pack(pady=10)
        
        pv_frame_o = tk.Frame(o_card, bg="#FFFFFF", height=30)
        pv_frame_o.pack(fill="x", pady=10)
        tk.Label(pv_frame_o, text="PV", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg=self.BG_COLOR).pack(side="left", padx=10)
        tk.Label(pv_frame_o, textvariable=self.opponent_health_var, font=("Segoe UI", 16, "bold"), bg="#FFFFFF", fg=self.DANGER).pack(side="right", padx=10)

        # --- COMBAT LOG & ADVANTAGE ---
        log_container = tk.Frame(self.root, bg=self.BG_COLOR)
        log_container.place(relx=0.5, rely=0.82, anchor="center")

        self.advantage_label_widget = tk.Label(log_container, textvariable=self.advantage_label_var, font=("Segoe UI", 12, "bold"), bg=self.BG_COLOR, fg=self.ACCENT)
        self.advantage_label_widget.pack(pady=5)
        tk.Label(log_container, textvariable=self.combat_log, font=("Segoe UI", 18, "bold"), bg=self.BG_COLOR, fg=self.PRIMARY, wraplength=900).pack()
        
        # --- UI BUTTONS (BOTTOM) ---
        self.btns_container = tk.Frame(self.root, bg=self.BG_COLOR, pady=40)
        self.btns_container.pack(side="bottom", fill="x")
        
        btn_center = tk.Frame(self.btns_container, bg=self.BG_COLOR)
        btn_center.pack()

        self.quick_btn_frame = self.create_button(btn_center, "COMBAT RAPIDE", None, color=self.ACCENT)
        self.quick_btn_frame.pack(side="left", padx=10)
        self.quick_btn = self.quick_btn_frame.button
        
        self.action_btn_frame = self.create_button(btn_center, "ATTAQUER", self.attack, color=self.SUCCESS)
        self.action_btn_frame.pack(side="left", padx=10)
        self.action_btn = self.action_btn_frame.button
        if self.quick_btn:
            self.quick_btn.bind('<ButtonPress-1>', self.start_auto_attack)
            self.quick_btn.bind('<ButtonRelease-1>', self.stop_auto_attack)
            
        self.create_button(btn_center, "QUITTER", self.on_quit, color=self.DANGER).pack(side="left", padx=10)

    def start_combat(self):
        """Détermine qui commence"""
        self.turn = random.choice(["player", "opponent"])
        self.update_button_text()
        if self.turn == "player":
            self.combat_log.set("C'EST VOTRE TOUR !")
        else:
            self.combat_log.set("L'ADVERSAIRE ATTAQUE !")

    def update_button_text(self):
        """Met à jour le texte du bouton"""
        pass

    def update_health(self):
        """Met à jour l'affichage des PV"""
        self.player_health_var.set(f"PV: {int(max(0, self.player_freak['stats']['pv']))}")
        self.opponent_health_var.set(f"PV: {int(max(0, self.opponent_freak['stats']['pv']))}")

    def attack(self):
        """Gère un tour d'attaque"""
        if self.player_freak["stats"]["pv"] <= 0 or self.opponent_freak["stats"]["pv"] <= 0:
            return

        if self.turn == "player":
            base = self.player_freak["stats"]["attack"] - self.opponent_freak["stats"]["defense"] + 1
            dmg = calculate_damage(base, self.player_freak["type"], self.opponent_freak["type"])
            self.opponent_freak["stats"]["pv"] -= dmg
            self.combat_log.set(f"Vous infligez {dmg} dégâts à {self.opponent_freak['name']}!")
            
            if is_effective(self.player_freak["type"], self.opponent_freak["type"]):
                self.advantage_label_var.set(f"Votre {self.player_freak['name']} est avantagé !")
            else:
                self.advantage_label_var.set("")
                
            if self.opponent_freak["stats"]["pv"] <= 0:
                self.combat_log.set(f"VICTOIRE ! Vous avez vaincu {self.opponent_freak['name']}!")
                self.action_btn.config(state="disabled")
                self.stop_auto_attack()
                self.update_ligue_progression()
            self.turn = "opponent"
        else:
            base = self.opponent_freak["stats"]["attack"] - self.player_freak["stats"]["defense"] + 1
            dmg = calculate_damage(base, self.opponent_freak["type"], self.player_freak["type"])
            self.player_freak["stats"]["pv"] -= dmg
            self.combat_log.set(f"{self.opponent_freak['name']} inflige {dmg} dégâts à {self.player_freak['name']}!")
            
            if is_effective(self.opponent_freak["type"], self.player_freak["type"]):
                self.advantage_label_var.set(f"Votre {self.player_freak['name']} est désavantagé !")
                # Changer la couleur du label de désavantage en rouge - FIX DIRECT
                if hasattr(self, 'advantage_label_widget'):
                    self.advantage_label_widget.config(fg=self.DANGER)
            else:
                self.advantage_label_var.set("")
                # Reset couleur par défaut (si nécessaire pour le futur)
                if hasattr(self, 'advantage_label_widget'):
                    self.advantage_label_widget.config(fg=self.ACCENT)
                
            if self.player_freak["stats"]["pv"] <= 0:
                self.combat_log.set(f"DÉFAITE... Vous avez été vaincu par {self.opponent_freak['name']}.")
                self.action_btn.config(state="disabled")
                self.stop_auto_attack()
            self.turn = "player"
            
        self.update_health()
        self.update_button_text()

    def start_auto_attack(self, event=None):
        """Lance l'auto-attaque"""
        self.auto_attack()
        
    def stop_auto_attack(self, event=None):
        """Arrête l'auto-attaque"""
        if self.auto_attack_job:
            self.root.after_cancel(self.auto_attack_job)
            self.auto_attack_job = None
            
    def auto_attack(self):
        """Boucle d'auto-attaque"""
        if self.action_btn and self.action_btn['state'] == 'normal':
            self.attack()
            self.auto_attack_job = self.root.after(100, self.auto_attack)
        else:
            self.auto_attack_job = None

    def update_ligue_progression(self):
        """Met à jour le niveau de ligue dans le profil"""
        try:
            with open(self.profile_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                
            lvl = 0
            idx = -1
            for i, line in enumerate(lines):
                if line.startswith("ligue_level="):
                    lvl = int(line.split("=")[1].strip())
                    idx = i
                    break
                    
            adv_num = int(self.adversaire_key.replace("adversaire", ""))
            if adv_num >= lvl:
                lines[idx] = f"ligue_level={lvl + 1:02d}\n"
                with open(self.profile_path, "w", encoding="utf-8") as file:
                    file.writelines(lines)
                logging.info(f"Ligue level up: {lvl+1}")
        except Exception as e:
            logging.error(f"Erreur update ligue: {e}")

    def on_quit(self):
        """Quitte le combat"""
        self.stop_auto_attack()
        self.back_to_league()
        
    def back_to_league(self):
        """Retourne à la ligue"""
        from screens.league import LeagueScreen
        self.app.show_screen(LeagueScreen)
