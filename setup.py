from distutils.core import setup
import py2exe

setup(
    console=[
        "barcodefreaks.py",
        "scan.py",
        "stockage.py",
        "training.py",
        "ligue.py",
        "freakopedia.py",
        "visualizer.py",
        "profil.py",
        "dueltest.py",
        "scan_image.py",
        "gen_ligue.py",
    ],
    options={
        "py2exe": {
            "includes": ["os", "tkinter", "PIL", "pyzbar.pyzbar"],
            "bundle_files": 1,
            "compressed": True,
        }
    },
    zipfile=None,
)
