# 🎯 Instructions de Lancement - Projet E-Commerce

## 🚀 Démarrage Rapide

### Méthode 1 : Script PowerShell (Recommandé)
Double-cliquez sur le fichier **`start_server.ps1`** ou exécutez :
```powershell
.\start_server.ps1
```

### Méthode 2 : Script Batch
Double-cliquez sur le fichier **`start_server.bat`**

### Méthode 3 : Manuelle
```bash
# 1. Activer l'environnement virtuel
env\Scripts\activate

# 2. Lancer le serveur
python manage.py runserver
```

## 🌐 Accès au Site

Une fois le serveur lancé, ouvrez votre navigateur et accédez à :

- **🏠 Site web :** http://127.0.0.1:8000/
- **⚙️ Administration :** http://127.0.0.1:8000/admin/

## 👤 Comptes de Test

### 🔑 Administrateur
```
Username : admin
Password : admin123
```
**Capacités :** Gestion complète de la plateforme via /admin/

### 🛒 Vendeur
```
Username : vendeur1
Password : vendeur123
```
**Capacités :** Ajouter et gérer des produits

### 🛍️ Client
```
Username : client1
Password : client123
```
**Capacités :** Acheter des produits, gérer le panier

## 📋 Checklist de Test

### ✅ Tests Basiques

**En tant que visiteur (sans connexion) :**
- [ ] Voir la page d'accueil avec les produits
- [ ] Naviguer dans la liste des produits
- [ ] Filtrer par catégorie
- [ ] Rechercher un produit
- [ ] Voir les détails d'un produit

**En tant que client (client1) :**
- [ ] Se connecter
- [ ] Ajouter un produit au panier
- [ ] Modifier la quantité dans le panier
- [ ] Supprimer un article du panier
- [ ] Passer une commande
- [ ] Voir l'historique des commandes
- [ ] Voir les détails d'une commande

**En tant que vendeur (vendeur1) :**
- [ ] Se connecter
- [ ] Accéder au tableau de bord vendeur
- [ ] Créer un nouveau produit avec image
- [ ] Modifier un produit existant
- [ ] Désactiver un produit
- [ ] Supprimer un produit

**En tant qu'administrateur (admin) :**
- [ ] Accéder à l'interface d'administration
- [ ] Créer un nouveau vendeur
- [ ] Créer une nouvelle catégorie
- [ ] Créer une nouvelle étiquette
- [ ] Voir toutes les commandes
- [ ] Modifier le statut d'une commande
- [ ] Gérer les utilisateurs

## 📁 Structure des URLs

| Page | URL | Accès |
|------|-----|-------|
| Accueil | `/` | Public |
| Liste produits | `/produits/` | Public |
| Détail produit | `/produit/<id>/` | Public |
| Inscription | `/inscription/` | Public |
| Connexion | `/connexion/` | Public |
| Panier | `/panier/` | Connecté |
| Commander | `/commander/` | Connecté |
| Mes commandes | `/mes-commandes/` | Connecté |
| Tableau de bord vendeur | `/vendeur/tableau-de-bord/` | Vendeur |
| Créer produit | `/vendeur/produit/creer/` | Vendeur |
| Administration | `/admin/` | Admin |

## 🐛 Dépannage

### Problème : "Pillow is not installed"
```bash
env\Scripts\python.exe -m pip install Pillow
```

### Problème : Le serveur ne démarre pas
1. Vérifier que l'environnement virtuel est activé
2. Réinstaller les dépendances :
```bash
pip install -r requirements.txt
```

### Problème : Erreur de base de données
1. Supprimer le fichier `db.sqlite3`
2. Réexécuter les migrations :
```bash
python manage.py migrate
python create_sample_data.py
```

### Problème : Les images ne s'affichent pas
- Vérifier que le dossier `media/products/` existe
- S'assurer que `DEBUG = True` dans `settings.py`

## 📦 Réinitialiser les Données

Pour recréer les données d'exemple (catégories, produits, comptes) :
```bash
python create_sample_data.py
```

## 🎨 Personnalisation

### Modifier le CSS
Éditez le fichier : `static/css/style.css`

### Ajouter des catégories
Via l'admin : http://127.0.0.1:8000/admin/shop/category/

### Ajouter des étiquettes
Via l'admin : http://127.0.0.1:8000/admin/shop/tag/

## 📸 Captures d'Écran Recommandées

Pour votre documentation, prenez des captures de :
1. Page d'accueil avec les produits
2. Page de détail d'un produit
3. Panier avec articles
4. Formulaire de commande
5. Tableau de bord vendeur
6. Interface d'administration

## 🔐 Sécurité (Important pour la Production)

⚠️ **Ce projet est configuré pour le développement. Avant de le mettre en production :**

1. Changer `SECRET_KEY` dans `settings.py`
2. Mettre `DEBUG = False`
3. Configurer `ALLOWED_HOSTS`
4. Utiliser une vraie base de données (PostgreSQL, MySQL)
5. Configurer les fichiers statiques avec `collectstatic`
6. Activer HTTPS
7. Changer tous les mots de passe par défaut

## 📞 Support

En cas de problème, vérifiez :
- `README.md` - Documentation complète
- `GUIDE_DEMARRAGE.md` - Guide détaillé
- Les fichiers de logs Django dans le terminal

## ✨ Fonctionnalités Disponibles

✅ Authentification multi-rôles (Visiteur, Vendeur, Admin)
✅ Gestion complète des produits avec images
✅ Système de panier avec calcul automatique
✅ Passage de commandes avec mise à jour du stock
✅ Interface d'administration complète
✅ Filtrage et recherche de produits
✅ Design responsive et moderne
✅ Messages de confirmation/erreur
✅ Gestion des stocks automatique

---

**🎉 Profitez de votre plateforme E-Commerce !**

*Dernière mise à jour : Octobre 2025*

