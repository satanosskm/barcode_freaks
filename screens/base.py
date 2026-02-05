"""
Barcode Freaks - Classe de base pour tous les écrans
"""
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import colorsys

class Screen:
    """
    Classe de base pour tous les écrans du jeu
    Chaque écran hérite de cette classe
    """
    
    # Design System - Thème "SOFT DARK" (élégant et reposant)
    BG_COLOR = "#0F1113"      # Noir profond (fond)
    CARD_BG = "#1A1C1E"       # Gris anthracite (cartes)
    PRIMARY = "#E1E4E8"       # Blanc cassé (titres)
    SECONDARY = "#959BA3"     # Gris bleuté (texte secondaire)
    ACCENT = "#3498DB"        # Bleu moderne
    SUCCESS = "#2ECC71"       # Vert émeraude
    DANGER = "#E74C3C"        # Rouge corail
    
    # Polices
    FONT_TITLE = ("Segoe UI", 26, "bold")
    FONT_SUBTITLE = ("Segoe UI", 18, "bold")
    FONT_NORMAL = ("Segoe UI", 11)
    FONT_BUTTON = ("Segoe UI", 11, "bold")
    
    # Couleurs des types
    TYPE_COLORS = {
        "Ciel": "#2980B9",      # Bleu (Défaut)
        "Plante": "#27AE60",    # Vert Foncé
        "Tech": "#F1C40F",      # Jaune
        "Poison": "#8E44AD",    # Violet
        "Mineral": "#7F8C8D",   # Gris
        "Feu": "#D35400",       # Orange Foncé
        "Normal": "#FFFFFF"     # Blanc
    }

    def __init__(self, root, app):
        """Initialise l'écran avec le thème sombre"""
        self.root = root
        self.app = app
        self.widgets = []
        self.root.configure(bg=self.BG_COLOR)
        self.clear_window()

    def create_pill_image(self, width, height, color):
        """Crée une image de bouton arrondie avec dégradé et effet 3D"""
        # Supersampling pour un anti-aliasing parfait
        scale = 4
        img_w, img_h = max(1, width * scale), max(1, height * scale)
        radius = img_h // 2
        
        img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Extraire RGB
        hex_color = color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Fond dégradé vertical
        for y in range(img_h):
            # Forme pilule
            if y < radius:
                import math
                w_offset = radius - int(math.sqrt(max(0, radius**2 - (radius - y)**2)))
            elif y > img_h - radius:
                import math
                w_offset = radius - int(math.sqrt(max(0, radius**2 - (y - (img_h - radius))**2)))
            else:
                w_offset = 0
            
            # Dégradé de luminosité (1.1x -> 0.9x)
            factor = 1.1 - (0.3 * y / img_h)
            curr_r = min(255, int(r * factor))
            curr_g = min(255, int(g * factor))
            curr_b = min(255, int(b * factor))
            
            draw.line([w_offset, y, img_w - w_offset, y], fill=(curr_r, curr_g, curr_b, 255))

        # Bordure fine (Highlight 3D)
        draw.rounded_rectangle([2, 2, img_w - 3, img_h - 3], radius=radius, outline=(255, 255, 255, 40), width=3)
        
        return img.resize((width, height), Image.LANCZOS)

    def create_button(self, parent, text, command, color=None, width=None):
        """Crée un bouton premium arrondi avec effet 3D (Style Pill)"""
        base_color = color if color else self.ACCENT
        height = 42
        
        # Calcul de la largeur automatique en fonction du texte
        if width is None:
            # Estimation large de la largeur du texte (approx 9px par caractère en gras + padding)
            width = max(190, len(text) * 11 + 60)
        
        # Générer les versions normale et hover
        img_norm = self.create_pill_image(width, height, base_color)
        img_hov = self.create_pill_image(width, height, self.lighten_color(base_color))
        
        photo_norm = ImageTk.PhotoImage(img_norm)
        photo_hov = ImageTk.PhotoImage(img_hov)
        
        # Frame conteneur
        container = tk.Frame(parent, bg=parent.cget("bg"))
        
        btn = tk.Button(
            container,
            text=text,
            command=command,
            font=self.FONT_BUTTON,
            fg="white",
            image=photo_norm,
            compound="center",
            relief="flat",
            borderwidth=0,
            activeforeground="white",
            activebackground=self.BG_COLOR,
            bg=container.cget("bg"),
            cursor="hand2"
        )
        btn.pack()
        
        # Références pour éviter le garbage collection
        btn.photo_norm = photo_norm
        btn.photo_hov = photo_hov
        btn.base_color = base_color # Pour réutilisation
        
        # Logique hover
        def on_enter(e): btn.config(image=btn.photo_hov)
        def on_leave(e): btn.config(image=btn.photo_norm)
        def on_press(e): btn.config(pady=2)
        def on_release(e): btn.config(pady=0)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)
        
        container.button = btn
        return container

    def lighten_color(self, hex_color):
        """Eclaircit la couleur pour l'effet hover"""
        # Couleurs prédéfinies pour le thème sombre
        map_hover = {
            self.BG_COLOR: "#1A1C1E",
            self.CARD_BG: "#25282C",
            self.PRIMARY: "#FFFFFF",
            self.ACCENT: "#5DADE2",
            self.SUCCESS: "#58D68D",
            self.DANGER: "#EC7063",
        }
        return map_hover.get(hex_color, hex_color)
        
    def clear_window(self):
        """Supprime tous les widgets de la fenêtre"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def setup(self):
        """
        Configure l'écran (à surcharger dans les sous-classes)
        C'est ici que les widgets sont créés
        """
        raise NotImplementedError("Les sous-classes doivent implémenter setup()")
        
    def destroy(self):
        """Détruit l'écran et nettoie les ressources"""
        self.clear_window()
        
    def back_to_menu(self):
        """Retour au menu principal"""
        from .menu import MenuScreen
        self.app.show_screen(MenuScreen)
