# 🚀 Guide de Démarrage Rapide

## Lancer le projet

1. **Activer l'environnement virtuel**
```bash
env\Scripts\activate
```

2. **Lancer le serveur**
```bash
python manage.py runserver
```

3. **Accéder au site**
- Site web : http://127.0.0.1:8000/
- Administration : http://127.0.0.1:8000/admin/

## 👤 Comptes de test disponibles

### Administrateur
- Username : `admin`
- Password : `admin123`
- Accès : Interface d'administration complète

### Vendeur
- Username : `vendeur1`
- Password : `vendeur123`
- Accès : Espace vendeur pour gérer les produits

### Client
- Username : `client1`
- Password : `client123`
- Accès : Navigation, panier, commandes

## ✨ Fonctionnalités à tester

### En tant que Visiteur (sans connexion)
1. Parcourir les produits sur la page d'accueil
2. Filtrer par catégorie et rechercher des produits
3. Voir les détails d'un produit

### En tant que Client (client1)
1. Se connecter
2. Ajouter des produits au panier
3. Modifier les quantités dans le panier
4. Passer une commande
5. Voir l'historique des commandes

### En tant que Vendeur (vendeur1)
1. Se connecter
2. Accéder au tableau de bord vendeur
3. Ajouter un nouveau produit
4. Modifier un produit existant
5. Gérer le stock

### En tant qu'Administrateur (admin)
1. Accéder à /admin/
2. Gérer les utilisateurs
3. Gérer les catégories et étiquettes
4. Voir toutes les commandes
5. Modifier le statut des commandes

## 📦 Créer de nouvelles données

Pour réinitialiser ou ajouter des données d'exemple :
```bash
python create_sample_data.py
```

## 🎨 Structure des Pages

### Pages publiques
- `/` - Page d'accueil
- `/produits/` - Liste des produits
- `/produit/<id>/` - Détails d'un produit
- `/inscription/` - Inscription
- `/connexion/` - Connexion

### Pages client (authentification requise)
- `/panier/` - Panier d'achats
- `/commander/` - Finaliser la commande
- `/mes-commandes/` - Historique des commandes
- `/commande/<id>/` - Détails d'une commande

### Pages vendeur (authentification requise)
- `/vendeur/tableau-de-bord/` - Tableau de bord
- `/vendeur/produit/creer/` - Ajouter un produit
- `/vendeur/produit/<id>/modifier/` - Modifier un produit
- `/vendeur/produit/<id>/supprimer/` - Supprimer un produit

### Administration
- `/admin/` - Interface d'administration Django

## 🔧 Personnalisation

### Ajouter des catégories
1. Connexion admin : /admin/
2. Shop > Catégories > Ajouter

### Ajouter des étiquettes
1. Connexion admin : /admin/
2. Shop > Étiquettes > Ajouter

### Créer un nouveau vendeur
1. S'inscrire sur le site
2. Choisir "Vendeur" comme type de compte

## 📝 Notes importantes

- Le stock est automatiquement mis à jour lors d'une commande
- Les images de produits sont stockées dans `media/products/`
- Les fichiers CSS sont dans `static/css/`
- SQLite est utilisé pour la base de données (fichier `db.sqlite3`)

## 🐛 Dépannage

### Le serveur ne démarre pas
- Vérifier que l'environnement virtuel est activé
- Vérifier que Django est installé : `pip install -r requirements.txt`

### Les images ne s'affichent pas
- Vérifier que `DEBUG = True` dans `settings.py`
- Vérifier que les dossiers `media/` et `static/` existent

### Erreur de base de données
- Supprimer `db.sqlite3`
- Réexécuter : `python manage.py migrate`
- Réexécuter : `python create_sample_data.py`

## 🎯 Prochaines étapes

1. Tester toutes les fonctionnalités
2. Personnaliser le design (modifier `static/css/style.css`)
3. Ajouter vos propres produits
4. Explorer l'interface d'administration

---

**Bon développement ! 🎉**


