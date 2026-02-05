"""
Barcode Freaks - Point d'entrée principal
Application refactorisée avec architecture Tkinter unifiée
"""
from app import BarcodeFreaksApp
from screens.menu import MenuScreen

if __name__ == "__main__":
    # Créer l'application
    app = BarcodeFreaksApp()
    
    # Afficher le menu principal
    app.show_screen(MenuScreen)
    
    # Lancer la boucle principale
    app.run()
