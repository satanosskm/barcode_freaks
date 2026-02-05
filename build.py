"""
Script de build pour Barcode Freaks
Compile le jeu Python en un fichier .exe unique
"""
import os
import sys
import shutil

def main():
    print("=== Build Barcode Freaks ===\n")
    
    # Vérifier que PyInstaller est installé
    try:
        import PyInstaller
        print(f"✓ PyInstaller version {PyInstaller.__version__} trouvé")
    except ImportError:
        print("✗ PyInstaller n'est pas installé.")
        print("  Installation: pip install pyinstaller")
        return 1
    
    # Vérifier que les dépendances sont install\u00e9es
    print("\nVérification des dépendances...")
    dependencies = ['PIL', 'pyzbar', 'pyperclip', 'tkinter']
    missing = []
    
    for dep in dependencies:
        try:
            if dep == 'PIL':
                import PIL
            elif dep == 'pyzbar':
                import pyzbar
            elif dep == 'pyperclip':
                import pyperclip
            elif dep == 'tkinter':
                import tkinter
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} manquant")
            missing.append(dep)
    
    if missing:
        print(f"\nDépendances manquantes: {', '.join(missing)}")
        print("Installation: pip install -r requirements.txt")
        return 1
    
    # Nettoyer les anciens builds
    print("\nNettoyage des anciens builds...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            print(f"  Suppression de {folder}/")
            shutil.rmtree(folder)
    
    # Lancer PyInstaller
    print("\nCompilation avec PyInstaller...")
    print("  (Cela peut prendre plusieurs minutes...)\n")
    
    import subprocess
    result = subprocess.run([
        'pyinstaller',
        'BarcodeFreaks.spec',
        '--clean',  # Nettoyer le cache
        '--noconfirm',  # Ne pas demander confirmation
    ], capture_output=False)
    
    if result.returncode != 0:
        print("\n✗ Erreur lors de la compilation")
        return 1
    
    # Vérifier que le build a réussi
    exe_path = os.path.join('dist', 'BarcodeFreaks.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n✓ Build réussi!")
        print(f"  Fichier: {exe_path}")
        print(f"  Taille: {size_mb:.1f} MB")
        print(f"\n📂 Profils sauvegardés dans: %APPDATA%\\BarcodeFreaks\\profils")
        return 0
    else:
        print("\n✗ Échec du build")
        print("  Vérifiez les messages d'erreur ci-dessus")
        return 1

if __name__ == '__main__':
    sys.exit(main())
