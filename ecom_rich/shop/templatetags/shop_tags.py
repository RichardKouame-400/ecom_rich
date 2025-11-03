from django import template

register = template.Library()


@register.filter
def tag_color(tag_name):
    """
    Retourne une couleur de dégradé spécifique pour chaque étiquette
    """
    # Dictionnaire des couleurs par nom d'étiquette
    tag_colors = {
        'Nouveau': 'linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%)',  # Rouge
        'Promotion': 'linear-gradient(135deg, #fed330 0%, #f7b731 100%)',  # Jaune
        'Populaire': 'linear-gradient(135deg, #a55eea 0%, #8854d0 100%)',  # Violet
        'Écologique': 'linear-gradient(135deg, #26de81 0%, #20bf6b 100%)',  # Vert
        'Ecologique': 'linear-gradient(135deg, #26de81 0%, #20bf6b 100%)',  # Vert (sans accent)
        'Premium': 'linear-gradient(135deg, #ff9f43 0%, #ff6348 100%)',  # Orange
        'Soldes': 'linear-gradient(135deg, #fc5c65 0%, #eb3b5a 100%)',  # Rouge foncé
    }
    
    # Retourner la couleur spécifique ou une couleur par défaut
    return tag_colors.get(tag_name, 'linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%)')  # Turquoise par défaut


@register.filter
def tag_icon(tag_name):
    """
    Retourne une icône spécifique pour chaque étiquette
    """
    tag_icons = {
        'Nouveau': 'fa-sparkles',  # Étoiles
        'Promotion': 'fa-percent',  # Pourcentage
        'Populaire': 'fa-fire',  # Feu
        'Écologique': 'fa-leaf',  # Feuille
        'Ecologique': 'fa-leaf',  # Feuille (sans accent)
        'Premium': 'fa-crown',  # Couronne
        'Soldes': 'fa-tag',  # Tag
    }
    
    return tag_icons.get(tag_name, 'fa-tag')  # Tag par défaut

