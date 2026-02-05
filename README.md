# Barcode Freaks

## Présentation
Bienvenue dans **Barcode Freaks**, créé par Satanos en 2025. Scannez des codes-barres pour découvrir des créatures uniques, entraînez-les, et affrontez des adversaires dans une ligue palpitante !

## Développement & Crédits
- **Code initial** : Le jeu a été développé en 5 jours début mai 2025, écrit en immense majorité par **Copilot** dans VS Code (car je ne sais pas coder, c'était le challenge !).
- **Mise à jour & Modernisation** : Le code a ensuite été repris, modernisé (UI premium) et compilé en exécutable par **Gemini** via le logiciel **Antigravity**.
- **Images** : Les images des créatures ont été générées avec **Bing Image Creator**.
- **Concept** : Système de jeu et créatures entièrement inventés par moi.

## Installation et Lancement (Recommandé)
Ce jeu est conçu pour **Windows**.

1. **Télécharger** : Récupérez la dernière release `BarcodeFreaks.exe`.
2. **Lancer** : Double-cliquez simplement sur `BarcodeFreaks.exe` pour jouer.
   
> **Note** : Vos profils de sauvegarde sont stockés automatiquement dans le dossier `%APPDATA%\BarcodeFreaks\profils`.

## Inspirations
Ce jeu s'inspire de plusieurs œuvres et concepts :
- **Barcode Battler** : Un jouet des années 90 basé sur les codes-barres.
- **Keitai Denjū Telefang** : Pour l'interaction des types.
- **Pokemon Go** : Pour le principe de récolte de points (candies).
- **Monster Rancher** : Pour le principe d'entraînement et la ligue.

## Fonctionnement du jeu
1. **Scanner des codes-barres** : Scannez des codes-barres pour découvrir de nouvelles créatures.
2. **Freakopedia** : Consultez les fiches des créatures découvertes.
3. **Mes Freaks** : Gérez vos créatures capturées.
4. **Ligue Barcode Freaks** : Affrontez des adversaires dans une ligue compétitive.
5. **Entraînement** : Améliorez les statistiques de vos créatures pour les rendre plus puissantes.
6. **Profil** : Gérez votre profil et vos données de jeu.

## Explications
- **Objectif principal** : Vaincre l'adversaire 50 de la ligue.
- **Points d'espèce** : Chaque nouveau code-barre scanné vous donne 5 points pour l'espèce rencontrée.
- **Entraînement** : Vous pouvez entraîner votre freak pour augmenter son attaque, sa défense ou ses points de vie. L'entraînement peut être faible, moyen ou super, rapportant plus ou moins de points.
- **Niveau maximum** : Le niveau maximum de votre freak ne peut pas dépasser :
  - Le nombre de points de son espèce que vous possédez.
  - Le niveau de votre dernier adversaire dans la ligue.
- **Codes-barres réutilisables** : Vous pouvez scanner plusieurs fois le même code-barre et recommencer l'entraînement de zéro. Vos points ne sont jamais consommés, ils sont débloqués définitivement.
- **Types et créatures** : Il y a 40 créatures différentes réparties en 8 types. Chaque type est efficace contre un autre type, infligeant 50% de dégâts supplémentaires.
- **Niveaux et stats** : Chaque créature générée est de base au niveau 1. Ses statistiques sont les suivantes :
  - **Attaque** : Entre 1 et 20.
  - **Défense** : Entre 1 et 20.
  - **PV** : Entre 20 et 40.
  Il en va de même pour les adversaires. Essayez d'adopter ceux qui ont les meilleures stats !
- **Codes-barres compatibles** : Les codes-barres compatibles sont au format **EAN-13** (13 chiffres) et **EAN-8** (8 chiffres). Vous pouvez :
  - Entrer directement les 13 ou 8 chiffres dans le champ prévu.
  - Fournir une image (en **.jpg** ou **.png**) d'un code-barre EAN-13 ou EAN-8 en gros plan et centré dans l'image.

---

## Version Python (Développement / Legacy)
Si vous souhaitez lancer le jeu depuis le code source (Python 3.10+ requis) :

### Installation des dépendances
```bash
pip install -r requirements.txt
# Ou manuellement :
pip install pillow pyzbar pyperclip
```

### Lancement
Exécutez le fichier principal :
```bash
python main.py
```

## Retrouvez-moi
Si vous aimez le retrogaming, n'hésitez pas à visiter ma chaîne YouTube :  
[https://www.youtube.com/@satanosSKM](https://www.youtube.com/@satanosSKM)

Amusez-vous bien dans l'univers de Barcode Freaks !
