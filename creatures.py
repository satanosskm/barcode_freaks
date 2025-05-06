creatures = [
    {"name": "Kakamu", "type": "Poison", "description": "C'est un champion de natation, surtout dans les égouts."},
    {"name": "Rockfort", "type": "Mineral", "description": "Ses bretelles sont en fait des tiges de titane."},
    {"name": "Mantalo", "type": "Aqua", "description": "Elle court sur l'eau à la façon d'un ninja."},
    {"name": "Aspigeon", "type": "Ciel", "description": "Il peut avaler des proies plus grosses que lui."},
    {"name": "Colocrater", "type": "Feu", "description": "A la fois solide et liquide, il carbonise tout ce qu'il touche."},
    {"name": "Ptibriquet", "type": "Feu", "description": "Ne le faites pas crier, vous pourriez prendre feu."},
    {"name": "Piloufass", "type": "Mineral", "description": "Décidé à prendre son destin en main, il ne retombe que sur la tranche."},
    {"name": "Hairison", "type": "Plante", "description": "Les épis sur son dos repoussent tous les jours."},
    {"name": "Carcajoute", "type": "Tech", "description": "Il se goinfre et dépense son surplus d'énergie par des décharges."},
    {"name": "Barakarot", "type": "Plante", "description": "Espèce mutante qui a reçu par mégarde trop de fertilisants."},
    {"name": "Foualievr", "type": "Poison", "description": "Il a testé toutes les substances et ne s'en ai jamais remis."},
    {"name": "Coupegorge", "type": "Ciel", "description": "Il utilise son apparence inoffensive pour détrousser ses victimes."},
    {"name": "Flaturance", "type": "Poison", "description": "Il ressemble à une pêche, mais ne sent pas la rose."},
    {"name": "Telecommando", "type": "Tech", "description": "On dit qu'il rêve de contrôler le monde."},
    {"name": "Gringalet", "type": "Mineral", "description": "Si tu le ramasses sur la plage, tu entendras qu'il pleurniche."},
    {"name": "Chaurizo", "type": "Feu", "description": "On a du revoir l'échelle de Scoville lorsque son espèce a été découverte."},
    {"name": "Playstecheum", "type": "Tech", "description": "Personne ne veut jouer avec elle, alors elle en veut à tout le monde."},
    {"name": "Asterigolo", "type": "Aqua", "description": "Il a fait l'école du rire, mais il a été recalé."},
    {"name": "Pisthache", "type": "Plante", "description": "Complètement fêlée, elle veut décortiquer tout individu qu'elle croise."},
    {"name": "Gravyeah", "type": "Mineral", "description": "Très pacifique, il refuse d'être lancé sur quelqu'un."},
    {"name": "Canarime", "type": "Ciel", "description": "Fan de rap, ses punchlines ne servent qu'à blesser."},
    {"name": "Koalanta", "type": "Normal", "description": "Son esprit d'équipe est très virulent, il déteste Gravyeah qu'il considère comme son rival."},
    {"name": "Kangouroue", "type": "Tech", "description": "Ce chauffard ne vit que pour la vitesse, il ne se soucie pas de la sécurité des autres."},
    {"name": "Amours", "type": "Normal", "description": "Trop amical, il serre tout le monde dans ses bras jusqu'à la blessure."},
    {"name": "Pumarteau", "type": "Normal", "description": "Il cherche desespérément le gong pour sonner la fin du monde."},
    {"name": "Grododo", "type": "Ciel", "description": "Il n'était pas disparu, il était juste en train de dormir."},
    {"name": "Attachien", "type": "Normal", "description": "On dit qu'il est à l'origine de tous les t-shirts cringe vendus sur le marché."},
    {"name": "Requindeutroi", "type": "Aqua", "description": "Ses trois têtes ne veulent jamais manger la même chose."},
    {"name": "Watzephoque", "type": "Aqua", "description": "Ses tours de magie peuvent te rendre fou."},
    {"name": "Pepsycho", "type": "Poison", "description": "Ses bulles brûlent comme de l'acide."},
    {"name": "Dynapaud", "type": "Feu", "description": "Il explose pour rien, ne l'énervez jamais."},
    {"name": "Ananarch", "type": "Plante", "description": "Le punk des tropiques, il adore se bagarrer."},
    {"name": "Prizdenerf", "type": "Tech", "description": "Il n'est pas défectueux, il est juste méchant."},
    {"name": "Abeillcool", "type": "Ciel", "description": "Son style extravagant déstabilise ses ennemis."},
    {"name": "Mouchamer", "type": "Poison", "description": "Ne la regardez pas dans les yeux, elle vous cracherait au visage."},
    {"name": "Filoutre", "type": "Aqua", "description": "Elle ne voit pas très bien, mais ne manque pas de courage."},
    {"name": "Discochon", "type": "Normal", "description": "Sa chorégraphie est en fait un art martial."},
    {"name": "Belugaz", "type": "Feu", "description": "On peut voir sa flamme dépasser des nappes de lave."},
    {"name": "Baobaffe", "type": "Plante", "description": "Il peut déraciner un congénère qui lui fait de l'ombre."},
    {"name": "Avatanche", "type": "Mineral", "description": "Il adore dégringoler le long des pentes rocheuses."},
]

# Exemple de données fictives pour les créatures
CREATURES = {
    "Freak1": {
        "image": "freak1.png",
        "type": "Feu",
        "stats": {"attack": 50, "defense": 30, "hp": 100},
    },
    "Freak2": {
        "image": "freak2.png",
        "type": "Eau",
        "stats": {"attack": 40, "defense": 40, "hp": 120},
    },
    # Ajoutez d'autres créatures ici
}

def get_creature_data(name):
    """
    Récupère les données d'une créature en fonction de son nom.
    :param name: Nom de la créature
    :return: Dictionnaire contenant les données de la créature
    """
    return CREATURES.get(name, None)
