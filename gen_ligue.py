import random
import hashlib
from creatures import creatures

def generate_valid_ean13():
    """
    Génère un code EAN-13 valide aléatoire.
    """
    base = [random.randint(0, 9) for _ in range(12)]
    checksum = (10 - sum((3 if i % 2 else 1) * digit for i, digit in enumerate(base)) % 10) % 10
    return ''.join(map(str, base)) + str(checksum)

def generate_freak_from_ean13(ean13):
    """
    Génère un freak à partir d'un code EAN-13 valide.
    Utilise la même méthode que dans scan.py.
    """
    hash_value = hashlib.sha256(ean13.encode()).hexdigest()
    creature_index = int(hash_value[:8], 16) % len(creatures)
    selected_creature = creatures[creature_index]

    stats = {
        "attack": int(hash_value[8:16], 16) % 20 + 1,
        "defense": int(hash_value[16:24], 16) % 20 + 1,
        "pv": int(hash_value[24:32], 16) % 21 + 20
    }

    return {
        "name": selected_creature["name"],
        "type": selected_creature["type"],
        "stats": stats
    }

def apply_stat_increase(freak, num_d3):
    """
    Applique une augmentation de statistiques à un freak.
    :param freak: Dictionnaire représentant le freak.
    :param num_d3: Nombre de dés D3 à lancer.
    """
    total_points = sum(random.randint(1, 3) for _ in range(num_d3))
    for _ in range(total_points):
        stat_to_increase = random.choice(["attack", "defense", "pv"])
        if stat_to_increase == "pv":
            freak["stats"]["pv"] += 2  # Les points en PV sont doublés
        else:
            freak["stats"][stat_to_increase] += 1

def generate_opponent_for_level(level):
    """
    Génère un adversaire pour un niveau donné.
    :param level: Niveau de l'adversaire.
    :return: Dictionnaire représentant le freak avec ses statistiques augmentées.
    """
    # Étape 1 : Générer un code EAN-13 valide
    ean13 = generate_valid_ean13()
    print(f"EAN-13 généré : {ean13}")

    # Étape 2 : Générer un freak de base
    freak = generate_freak_from_ean13(ean13)
    print(f"Freak de base (niveau {level}) : {freak}")

    # Étape 3 : Appliquer une augmentation de statistiques selon le niveau
    if level > 1:
        apply_stat_increase(freak, level - 1)  # (niveau - 1)D3
    print(f"Freak après augmentation (niveau {level}) : {freak}")

    return freak

def generate_ligue():
    """
    Génère les 50 niveaux de la ligue.
    :return: Liste des freaks adverses pour chaque niveau.
    """
    ligue = []
    for level in range(1, 51):
        opponent = generate_opponent_for_level(level)
        ligue.append(opponent)
    return ligue

if __name__ == "__main__":
    # Test : Générer les adversaires pour les 50 niveaux de la ligue
    ligue = generate_ligue()
    for i, opponent in enumerate(ligue, start=1):
        print(f"Niveau {i}: {opponent['name']} ({opponent['type']}) - Stats: {opponent['stats']}")
