# 🔍 Guide de Debug - Confirmation des Commandes

## ✅ Commande de Test Créée

**Commande #3** a été créée avec :
- Client : client1
- Vendeur : vendeur1
- Statut : **En attente**
- Produits : 2 produits du vendeur1
- Total : 149.96 €

---

## 🚀 ÉTAPES DE TEST EXACTES

### 1. Connectez-vous comme Vendeur

```
URL : http://127.0.0.1:8000/connexion/
Username : vendeur1
Password : vendeur123
```

### 2. Allez sur la Gestion des Commandes

**Méthode A - Via Dashboard :**
1. Navbar → "Espace Vendeur"
2. Cliquez sur le bouton bleu "Commandes"

**Méthode B - Directe :**
```
URL : http://127.0.0.1:8000/vendeur/commandes/
```

### 3. Vérifiez que Vous Voyez la Commande #3

Vous devriez voir dans le tableau :

| N° | Client | Date | Statut | Total | Actions |
|----|--------|------|--------|-------|---------|
| #3 | Marie Martin | ... | 🟡 En attente | 149.96€ | [👁️] [✓] |

**Si vous ne voyez PAS la commande #3 :**
- Vérifiez que vous êtes bien connecté comme vendeur1
- Rafraîchissez la page (F5)
- Exécutez à nouveau le script : `python creer_commande_test.py`

### 4. Testez la Confirmation

**Dans la colonne "Actions", vous devez voir 2 boutons :**
- 👁️ (bleu) = Détails
- ✓ (vert) = Confirmer

**Cliquez sur le bouton VERT ✓**

**Ce qui DOIT se passer :**
1. La page se recharge
2. Le badge passe de 🟡 "En attente" à 🔵 "Confirmée"
3. Un message vert apparaît en haut :
   ```
   ✅ Statut de la commande #3 mis à jour : En attente → Confirmée
   ```
4. Le bouton ✓ disparaît et est remplacé par 🚚 (Expédier)

---

## 🐛 SI ÇA NE FONCTIONNE PAS

### Problème 1 : Le bouton n'apparaît pas

**Causes possibles :**
- La commande n'est pas en statut "pending"
- La commande ne contient pas de produits du vendeur

**Solution :**
```bash
# Vérifier dans le shell
python manage.py shell
```

```python
from shop.models import Order
order = Order.objects.get(pk=3)
print(f"Statut : {order.status}")  # Doit afficher "pending"

# Vérifier les produits
for item in order.items.all():
    print(f"{item.product.name} - Vendeur: {item.product.seller.username}")
```

### Problème 2 : Le bouton ne fait rien quand on clique

**Causes possibles :**
- JavaScript qui bloque
- Problème CSRF
- Formulaire mal configuré

**Solution :**
1. Ouvrez la console du navigateur (F12)
2. Onglet "Console" - Regardez les erreurs
3. Onglet "Réseau" - Cliquez sur ✓ et regardez la requête

**Vous devriez voir :**
- Requête POST vers `/vendeur/commande/3/statut/`
- Code 302 (redirection)
- Pas d'erreur 403 ou 500

### Problème 3 : Erreur 403 (Forbidden)

**Cause :** Problème CSRF

**Solution :**
Vérifiez que le template a bien :
```html
<form method="post" action="...">
    {% csrf_token %}
    ...
</form>
```

### Problème 4 : Erreur 500 (Serveur)

**Cause :** Erreur Python dans la vue

**Solution :**
Regardez le terminal où tourne le serveur, vous devriez voir l'erreur complète.

---

## 🔬 TEST MANUEL DANS LE SHELL

Si rien ne fonctionne, testez manuellement :

```bash
python manage.py shell
```

```python
from shop.models import Order

# Récupérer la commande #3
order = Order.objects.get(pk=3)
print(f"Statut actuel : {order.status}")  # pending
print(f"Nom affiché : {order.get_status_display()}")  # En attente

# Changer le statut manuellement
order.status = 'confirmed'
order.save()

# Vérifier
print(f"Nouveau statut : {order.status}")  # confirmed
print(f"Nom affiché : {order.get_status_display()}")  # Confirmée
```

**Si ça fonctionne dans le shell mais pas via le bouton :**
→ Le problème est dans la vue ou le template

**Si ça ne fonctionne pas dans le shell non plus :**
→ Problème de base de données ou de modèle

---

## 📝 VÉRIFICATION DE LA VUE

La vue `seller_order_update_status` doit :

1. ✅ Vérifier que l'utilisateur est un vendeur
2. ✅ Vérifier que c'est une requête POST
3. ✅ Récupérer la commande
4. ✅ Vérifier que la commande a des produits du vendeur
5. ✅ Récupérer le nouveau statut du formulaire
6. ✅ Valider que le statut est valide
7. ✅ Sauvegarder le nouveau statut
8. ✅ Afficher un message de succès
9. ✅ Rediriger vers la page appropriée

---

## 🎯 TEST COMPLET PAS À PAS

### TEST 1 : Vérifier l'Accès

1. Allez sur : http://127.0.0.1:8000/vendeur/commandes/
2. **Si redirection vers /connexion/** → Pas connecté
3. **Si message "Accès réservé"** → Pas vendeur
4. **Si vous voyez le tableau** → ✅ OK

### TEST 2 : Vérifier la Commande

1. Dans le tableau, cherchez la commande #3
2. **Si vous ne la voyez pas** → Problème de filtrage
3. **Si vous la voyez** → ✅ OK
4. Vérifiez que le statut est bien 🟡 "En attente"

### TEST 3 : Vérifier le Bouton

1. Dans la colonne "Actions" de la commande #3
2. **Si vous voyez [👁️] seulement** → Bouton de confirmation manquant
3. **Si vous voyez [👁️] [✓]** → ✅ OK

### TEST 4 : Cliquer sur le Bouton

1. Faites un clic droit sur le bouton vert ✓
2. "Inspecter l'élément"
3. Vérifiez le code HTML :

```html
<form method="post" action="/vendeur/commande/3/statut/" class="d-inline">
    <input type="hidden" name="csrfmiddlewaretoken" value="...">
    <input type="hidden" name="return_to_list" value="true">
    <button type="submit" name="status" value="confirmed" ...>
        <i class="fas fa-check"></i>
    </button>
</form>
```

4. Cliquez normalement sur le bouton
5. Observez ce qui se passe

### TEST 5 : Vérifier la Requête

1. Ouvrez F12 → Onglet "Réseau" (Network)
2. Cliquez sur le bouton ✓
3. Regardez la requête qui apparaît

**Vous devriez voir :**
- Nom : `statut/`
- Méthode : POST
- Statut : 302 (Found - redirection)
- Type : document

**Si vous voyez :**
- Statut 403 → Problème CSRF
- Statut 404 → URL incorrecte
- Statut 500 → Erreur serveur (regardez le terminal)

---

## ✅ CE QUI A ÉTÉ CRÉÉ POUR VOUS

**Commande #3** avec :
- ✅ Statut : "En attente" (pending)
- ✅ Client : client1 (Marie Martin)
- ✅ 2 produits du vendeur1
- ✅ Total : 149.96 €
- ✅ Prête à être confirmée

---

## 🎯 ACTIONS À FAIRE MAINTENANT

1. **Connectez-vous** comme vendeur1
2. **Allez** sur http://127.0.0.1:8000/vendeur/commandes/
3. **Trouvez** la commande #3
4. **Cliquez** sur le bouton vert ✓
5. **Observez** le changement de statut

---

## 💡 SI VOUS VOULEZ CRÉER PLUS DE COMMANDES

Exécutez à nouveau le script :
```bash
python creer_commande_test.py
```

Cela créera une nouvelle commande de test.

---

## 📞 INFORMATIONS DE DEBUG

Si ça ne fonctionne toujours pas, envoyez-moi :
1. Le message d'erreur exact (screenshot ou texte)
2. Ce que vous voyez dans la console du navigateur (F12)
3. Ce qui apparaît dans le terminal du serveur

Je pourrai alors identifier le problème exact et le corriger !

