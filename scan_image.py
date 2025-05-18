import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pyzbar.pyzbar import decode
import pyperclip

def is_valid_ean(barcode):
    """Vérifie si un code-barres EAN-13 ou EAN-8 est valide."""
    if not barcode.isdigit():
        return False
    if len(barcode) == 13:
        checksum = sum(int(barcode[i]) * (3 if i % 2 else 1) for i in range(12))
        check_digit = (10 - (checksum % 10)) % 10
        return check_digit == int(barcode[-1])
    elif len(barcode) == 8:
        # EAN-8: impairs (0,2,4,6) *3, pairs (1,3,5) *1
        checksum = sum(int(barcode[i]) * (3 if i % 2 == 0 else 1) for i in range(7))
        check_digit = (10 - (checksum % 10)) % 10
        return check_digit == int(barcode[-1])
    else:
        return False

def select_image():
    """Ouvre une boîte de dialogue pour sélectionner une image et lit le code-barres EAN-13 ou EAN-8."""
    file_path = filedialog.askopenfilename(
        title="Sélectionnez une image",
        filetypes=[("Images PNG et JPEG", "*.png;*.jpg;*.jpeg")]
    )
    if not file_path:
        return

    try:
        # Charger l'image et décoder le code-barres
        image = Image.open(file_path)
        decoded_objects = decode(image)

        if not decoded_objects:
            messagebox.showerror("Erreur", "Aucun code-barres détecté dans l'image.")
            return

        # Extraire le premier code-barres EAN-13 ou EAN-8 trouvé
        for obj in decoded_objects:
            if obj.type in ("EAN13", "EAN8"):
                code = obj.data.decode("utf-8")
                if is_valid_ean(code):
                    ean13_var.set(code)
                    return

        messagebox.showerror("Erreur", "Aucun code-barres EAN-13 ou EAN-8 valide trouvé dans l'image.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire l'image : {e}")

def copy_to_clipboard():
    """Copie le code EAN-13 dans le presse-papier."""
    ean13_code = ean13_var.get()
    if ean13_code:
        pyperclip.copy(ean13_code)
        messagebox.showinfo("Succès", "Code EAN-13 copié dans le presse-papier.")
    else:
        messagebox.showerror("Erreur", "Aucun code EAN-13 à copier.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Scanner d'image pour code-barres")
root.geometry("400x200")
root.configure(bg="lightblue")

# Variable pour afficher le code EAN-13
ean13_var = tk.StringVar()

# Bouton pour sélectionner une image
select_button = tk.Button(root, text="Sélectionner une image", command=select_image, font=("Arial", 14), bg="lightgreen")
select_button.pack(pady=10)

# Champ pour afficher le code EAN-13 ou EAN-8
ean13_label = tk.Label(root, text="Code EAN-13 ou EAN-8 :", font=("Arial", 12), bg="lightblue")
ean13_label.pack(pady=5)
ean13_entry = tk.Entry(root, textvariable=ean13_var, font=("Arial", 14), state="readonly", width=30)
ean13_entry.pack(pady=5)

# Bouton pour copier le code dans le presse-papier
copy_button = tk.Button(root, text="Copier dans le presse-papier", command=copy_to_clipboard, font=("Arial", 14), bg="lightyellow")
copy_button.pack(pady=10)

# Lancer la boucle principale
root.mainloop()
