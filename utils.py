"""
Utilitaires pour Barcode Freaks
Gestion des chemins de ressources et des profils pour PyInstaller
"""
import os
import sys


def resource_path(relative_path):
    """
    Obtenir le chemin absolu vers une ressource.
    Fonctionne en développement et dans un .exe PyInstaller.
    
    :param relative_path: Chemin relatif de la ressource
    :return: Chemin absolu de la ressource
    """
    try:
        # PyInstaller crée un dossier temporaire _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # En développement, utiliser le répertoire courant
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def get_profiles_dir():
    """
    Obtenir le dossier de sauvegarde des profils.
    Utilise %APPDATA%/BarcodeFreaks/profils pour la portabilité.
    
    :return: Chemin absolu du dossier profils
    """
    # Essayer d'utiliser APPDATA (recommandé pour Windows)
    appdata = os.getenv('APPDATA')
    
    if appdata:
        # Sauvegarder dans %APPDATA%\BarcodeFreaks\profils
        profiles_dir = os.path.join(appdata, 'BarcodeFreaks', 'profils')
    else:
        # Fallback : à côté de l'exécutable ou du script
        try:
            base_path = os.path.dirname(sys.executable)
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        profiles_dir = os.path.join(base_path, 'profils')
    
    # Créer le dossier s'il n'existe pas
    os.makedirs(profiles_dir, exist_ok=True)
    
    return profiles_dir


def get_image_path(image_name):
    """
    Obtenir le chemin vers une image dans le dossier images/.
    
    :param image_name: Nom du fichier image (ex: "kakamu.png")
    :return: Chemin absolu de l'image
    """
    return resource_path(os.path.join("images", image_name))


def get_barcode_path(barcode_name):
    """
    Obtenir le chemin vers un code-barre de test dans le dossier barcodes/.
    
    :param barcode_name: Nom du fichier de code-barre
    :return: Chemin absolu du code-barre
    """
    return resource_path(os.path.join("barcodes", barcode_name))
