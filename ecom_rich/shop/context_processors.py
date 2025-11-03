"""
Context processors pour rendre certaines variables disponibles dans tous les templates
"""
from .models import Cart


def cart_count(request):
    """
    Retourne le nombre total d'articles dans le panier de l'utilisateur
    """
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.get_item_count()
        except Cart.DoesNotExist:
            count = 0
    
    return {'cart_item_count': count}

