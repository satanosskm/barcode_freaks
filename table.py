# Table des types et leurs interactions
type_chart = {
    "Mineral": "Normal",
    "Normal": "Tech",
    "Tech": "Ciel",
    "Ciel": "Poison",
    "Poison": "Aqua",
    "Aqua": "Feu",
    "Feu": "Plante",
    "Plante": "Mineral"
}

def is_effective(attacker_type, defender_type):
    """
    Vérifie si un type est efficace contre un autre.
    :param attacker_type: Type de l'attaquant (str)
    :param defender_type: Type du défenseur (str)
    :return: True si le type de l'attaquant est efficace contre celui du défenseur, sinon False
    """
    return type_chart.get(attacker_type.capitalize()) == defender_type.capitalize()

def calculate_damage(base_damage, attacker_type, defender_type):
    """
    Calcule les dégâts en fonction des types.
    :param base_damage: Dégâts de base (int)
    :param attacker_type: Type de l'attaquant (str)
    :param defender_type: Type du défenseur (str)
    :return: Dégâts ajustés (int)
    """
    # Étape 1 : Ajout de +1 et vérification des dégâts minimum
    base_damage = max(1, base_damage)  # Si le résultat est <= 0, on le change en 1

    # Étape 2 : Application du bonus d'interaction des types
    if is_effective(attacker_type.capitalize(), defender_type.capitalize()):
        adjusted_damage = -(-base_damage * 1.5 // 1)  # Arrondi à l'entier supérieur
        return adjusted_damage

    # Étape 3 : Retour des dégâts de base si pas d'avantage
    return base_damage
