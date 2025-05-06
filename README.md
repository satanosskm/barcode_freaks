# Barcode Freaks

## Présentation
Bienvenue dans **Barcode Freaks**, créé par Satanos en 2025. Scannez des codes-barres pour découvrir des créatures uniques, entraînez-les, et affrontez des adversaires dans une ligue palpitante !

## Inspirations
Ce jeu s'inspire de plusieurs œuvres et concepts :
- **Barcode Battler** : Un jouet des années 90 basé sur les codes-barres, qui a inspiré le système de combat et la génération de créatures à partir de codes-barres.
- **Keitai Denjū Telefang** : Pour l'interaction des types entre les créatures.
- **Pokemon Go** : Pour le principe de récolte de points afin d'entraîner sa créature.
- **Monster Rancher** : Pour le principe d'entraînement et la ligue compétitive.

## Prérequis
Pour faire fonctionner le jeu, vous devez disposer des éléments suivants :
- **Python 3.10 ou supérieur** : Assurez-vous d'avoir une version récente de Python installée. Vous pouvez le télécharger depuis [python.org](https://www.python.org/).
- **pip** : L'outil de gestion des paquets Python, généralement inclus avec Python.

## Installation des dépendances
Avant de lancer le jeu, installez les dépendances nécessaires en exécutant la commande suivante dans un terminal :
```
pip install -r requirements.txt
```
Si le fichier `requirements.txt` n'est pas présent, installez manuellement les bibliothèques suivantes :
```
pip install pillow pyzbar pyperclip
```

## Lancement du jeu
Pour démarrer le jeu, exécutez le fichier `barcodefreaks.py` :
```
python barcodefreaks.py
```
Cela ouvrira l'interface principale du jeu.

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
- **Codes-barres compatibles** : Les codes-barres compatibles sont au format **EAN-13**, c'est-à-dire ceux à 13 chiffres. Vous pouvez :
  - Entrer directement les 13 chiffres dans le champ prévu.
  - Fournir une image (en **.jpg** ou **.png**) d'un code-barre en gros plan et centré dans l'image.

## Développement
- **Durée** : Le jeu a été développé en 5 jours début mai 2025.
- **Code** : Le code a été écrit en immense majorité par Copilot dans **VS Code**, car je ne sais pas coder et c'était ça le challenge. Tout a été codé en Python.
- **Images** : Les images des créatures ont été générées avec **Bing Image Creator**.
- **Système de jeu et créatures** : Le système de jeu et les créatures ont été entièrement inventés par moi.
- **Bugs** : Il y a probablement beaucoup de bugs, merci de votre indulgence !
- **Futur** : J'aimerais transposer le jeu en webapp, mais je n'y arrive pas pour le moment. On verra ça plus tard.

## Retrouvez-moi
Si vous aimez le retrogaming, n'hésitez pas à visiter ma chaîne YouTube :  
[https://www.youtube.com/@satanosSKM](https://www.youtube.com/@satanosSKM)

Amusez-vous bien dans l'univers de Barcode Freaks !