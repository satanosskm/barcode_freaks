# -*- mode: python ; coding: utf-8 -*-
"""
Fichier de configuration PyInstaller pour Barcode Freaks
Génère un fichier .exe unique avec toutes les ressources incluses
"""

import os

block_cipher = None

# Liste de tous les fichiers de données à inclure
import pyzbar
pyzbar_path = os.path.dirname(pyzbar.__file__)
added_files = [
    ('images', 'images'),  # Dossier images
    (pyzbar_path, 'pyzbar'), # DLLs de pyzbar
]

# Liste de tous les imports cachés
hidden_imports = [
    'pyzbar',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageDraw',
    'tkinter',
    'creatures',
    'table',
    'gen_ligue',
    'dictionnaire',
    'utils',
]

a = Analysis(
    ['main.py'],  # Point d'entrée - architecture refactorisée
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BarcodeFreaks',  # Nom de l'exécutable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compression UPX pour réduire la taille
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Pas de console (application GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='images/logo_BF.png',  # Icône (à convertir en .ico si nécessaire)
)
