# Projet E-Commerce Django

Plateforme de vente en ligne développée avec Django permettant aux vendeurs de publier leurs produits et aux visiteurs d'effectuer des achats.

## 🚀 Fonctionnalités

### Pour les Visiteurs/Clients
- ✅ Inscription et connexion
- ✅ Navigation dans le catalogue de produits
- ✅ Filtrage par catégorie, étiquette et recherche
- ✅ Ajout de produits au panier
- ✅ Passage de commandes (nécessite une connexion)
- ✅ Suivi des commandes

### Pour les Vendeurs
- ✅ Inscription en tant que vendeur
- ✅ Tableau de bord vendeur
- ✅ Création et publication de produits
- ✅ Gestion des produits (modification, suppression)
- ✅ Attribution de catégories et d'étiquettes aux produits

### Pour les Administrateurs
- ✅ Interface d'administration Django complète
- ✅ Gestion de tous les utilisateurs
- ✅ Gestion des catégories et étiquettes
- ✅ Gestion des produits et commandes
- ✅ Contrôle total de la plateforme

## 📋 Modèles de Données

### User (Utilisateur personnalisé)
- Types : Visiteur, Vendeur, Administrateur
- Informations : username, email, téléphone, adresse

### Product (Produit)
- Attributs : nom, description, prix, stock, image
- Relations : catégorie, étiquettes, vendeur

### Category (Catégorie)
- Organisation des produits par catégories

### Tag (Étiquette)
- Étiquettes multiples par produit (ex: Nouveau, Promotion, etc.)

### Cart (Panier)
- Panier unique par utilisateur
- Articles avec quantités

### Order (Commande)
- Statuts : En attente, Confirmée, Expédiée, Livrée, Annulée
- Mise à jour automatique du stock

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Django 5.2.7

### Étapes d'installation

1. **Cloner le projet**
```bash
cd ecom_rich
```

2. **Activer l'environnement virtuel**
```bash
# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

3. **Installer les dépendances**
```bash
pip install django pillow
```

4. **Effectuer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer les données d'exemple (optionnel)**
```bash
python create_sample_data.py
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

7. **Accéder à l'application**
- Site web : http://127.0.0.1:8000/
- Administration : http://127.0.0.1:8000/admin/

## 👤 Comptes de Test

Si vous avez exécuté le script `create_sample_data.py`, les comptes suivants sont disponibles :

### Administrateur
- **Username :** admin
- **Password :** admin123

### Vendeur
- **Username :** vendeur1
- **Password :** vendeur123

### Client
- **Username :** client1
- **Password :** client123

## 📁 Structure du Projet

```
ecom_rich/
├── ecom_richard/           # Configuration du projet
│   ├── settings.py         # Paramètres Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py
├── shop/                   # Application principale
│   ├── models.py          # Modèles de données
│   ├── views.py           # Vues
│   ├── urls.py            # Routes de l'application
│   ├── forms.py           # Formulaires
│   ├── admin.py           # Configuration admin
│   └── templates/shop/    # Templates HTML
├── static/                # Fichiers statiques (CSS, JS)
│   └── css/
│       └── style.css
├── media/                 # Fichiers uploadés (images produits)
├── db.sqlite3            # Base de données SQLite
└── manage.py             # Script de gestion Django
```

## 🎨 Technologies Utilisées

- **Backend :** Django 5.2.7
- **Frontend :** HTML5, CSS3, Bootstrap 5.3
- **Base de données :** SQLite
- **Icônes :** Font Awesome 6.4

## 🔑 Fonctionnalités Techniques

- Modèle utilisateur personnalisé avec types de rôles
- Gestion de panier avec calcul automatique des totaux
- Système de commandes avec gestion du stock
- Upload et affichage d'images pour les produits
- Filtrage et recherche de produits
- Interface d'administration personnalisée
- Messages flash pour le feedback utilisateur
- Design responsive (mobile-friendly)

## 📝 Utilisation

### Créer un Vendeur
1. S'inscrire sur le site
2. Choisir "Vendeur" comme type de compte
3. Accéder au tableau de bord vendeur depuis le menu
4. Ajouter des produits avec images, prix, catégories

### Effectuer un Achat
1. S'inscrire ou se connecter
2. Parcourir les produits
3. Ajouter des articles au panier
4. Finaliser la commande avec adresse de livraison
5. Suivre la commande dans "Mes Commandes"

### Administration
1. Se connecter avec le compte admin
2. Accéder à /admin/
3. Gérer tous les aspects de la plateforme

## 🚧 Développement Futur

Améliorations possibles :
- Système de paiement en ligne
- Système d'évaluation et d'avis produits
- Messagerie entre acheteurs et vendeurs
- Notifications par email
- Historique des ventes pour les vendeurs
- Statistiques et graphiques
- Export de données
- API REST

## 📄 Licence

Projet éducatif - Libre d'utilisation

## 👨‍💻 Auteur

Développé dans le cadre du Projet 3 : Conception d'un site E-commerce

---

**Note :** Ce projet est destiné à des fins éducatives et de développement. Pour une utilisation en production, des améliorations de sécurité et de performance sont recommandées.


