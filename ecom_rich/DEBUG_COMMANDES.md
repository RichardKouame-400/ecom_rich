# 🔍 DEBUG - Confirmation des Commandes

## Étapes de Vérification

### Étape 1 : Vérifier l'Utilisateur

**Connecté comme :** vendeur1 ?
**Type d'utilisateur :** seller ?

Pour vérifier, ajoutez temporairement dans le template :
```html
{{ user.username }} - {{ user.user_type }}
```

### Étape 2 : Vérifier les Commandes

Sur `/vendeur/commandes/`, vous devriez voir :
- Une liste de commandes
- Des badges de statut colorés
- Des boutons dans la colonne Actions

### Étape 3 : Inspecter le Formulaire

Faites clic droit sur le bouton ✓ → "Inspecter"

Vous devriez voir :
```html
<form method="post" action="/vendeur/commande/1/statut/">
    <input type="hidden" name="csrfmiddlewaretoken" value="...">
    <input type="hidden" name="return_to_list" value="true">
    <button type="submit" name="status" value="confirmed">
        <i class="fas fa-check"></i>
    </button>
</form>
```

### Étape 4 : Vérifier la Soumission

1. Ouvrez la console du navigateur (F12)
2. Onglet "Réseau" (Network)
3. Cliquez sur le bouton ✓
4. Regardez la requête POST

**Ce que vous devriez voir :**
- Méthode : POST
- URL : /vendeur/commande/1/statut/
- Code : 302 (redirection)
- Données : status=confirmed, return_to_list=true

### Étape 5 : Vérifier les Messages

Après le clic, en haut de la page, vous devriez voir :
```
✅ Statut de la commande #1 mis à jour : En attente → Confirmée
```

## Solutions Possibles

### Si le bouton ne fait rien :

**Vérifiez JavaScript :**
- Désactivez temporairement `static/js/main.js`
- Testez à nouveau

**Vérifiez CSRF :**
- Le token CSRF doit être présent dans le formulaire
- Vérifiez dans le code source de la page

### Si vous avez une erreur 403 (Forbidden) :

C'est un problème CSRF. Solution :
```python
# Dans settings.py, vérifiez :
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]
```

### Si vous avez une erreur 404 :

L'URL n'est pas trouvée. Vérifiez :
```bash
python manage.py show_urls | grep seller
```

### Si le statut ne change pas :

Vérifiez dans le shell :
```python
from shop.models import Order
order = Order.objects.get(pk=1)
print(f"Statut : {order.status}")
# Essayez manuellement
order.status = 'confirmed'
order.save()
print(f"Nouveau statut : {order.status}")
```

## Test Manuel Simple

Créons une commande et changeons son statut manuellement :

```bash
python manage.py shell
```

```python
# Importer les modèles
from shop.models import Order, User

# Créer une commande test
user = User.objects.get(username='client1')
Order.objects.create(
    user=user,
    status='pending',
    total_amount=100.00,
    shipping_address='Test',
    phone='0123456789'
)

# Vérifier
orders = Order.objects.filter(status='pending')
print(f"Commandes en attente : {orders.count()}")
```

## Code Simplifié pour Test

Si le problème persiste, utilisez ce code simplifié :

```python
# Dans views.py, remplacez temporairement par :
@login_required
def seller_order_update_status(request, pk):
    print(f"=== DEBUG ===")
    print(f"User: {request.user.username}")
    print(f"User type: {request.user.user_type}")
    print(f"Method: {request.method}")
    print(f"Order ID: {pk}")
    
    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        order = Order.objects.get(pk=pk)
        print(f"Old status: {order.status}")
        
        new_status = request.POST.get('status')
        print(f"New status: {new_status}")
        
        order.status = new_status
        order.save()
        print(f"Saved status: {order.status}")
        
        messages.success(request, f"Statut changé en {new_status}")
    
    return redirect('seller_orders')
```

Regardez la console du serveur pour voir les messages de debug.

