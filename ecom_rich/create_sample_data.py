# -*- coding: utf-8 -*-
"""
Script pour creer des donnees d'exemple pour le site e-commerce
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_richard.settings')
django.setup()

from shop.models import User, Category, Tag, Product


def create_sample_data():
    print("Creation des donnees d'exemple...")
    
    # Creer un superutilisateur admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@ecommerce.fr',
            password='admin123',
            user_type='admin'
        )
        print("[OK] Superutilisateur cree: admin / admin123")
    
    # Creer un vendeur
    if not User.objects.filter(username='vendeur1').exists():
        vendeur = User.objects.create_user(
            username='vendeur1',
            email='vendeur1@ecommerce.fr',
            password='vendeur123',
            user_type='seller',
            first_name='Jean',
            last_name='Dupont',
            phone='0123456789',
            address='123 Rue du Commerce, 75001 Paris'
        )
        print("[OK] Vendeur cree: vendeur1 / vendeur123")
    else:
        vendeur = User.objects.get(username='vendeur1')
    
    # Creer un visiteur/acheteur
    if not User.objects.filter(username='client1').exists():
        client = User.objects.create_user(
            username='client1',
            email='client1@ecommerce.fr',
            password='client123',
            user_type='visitor',
            first_name='Marie',
            last_name='Martin',
            phone='0987654321',
            address='456 Avenue des Acheteurs, 69001 Lyon'
        )
        print("[OK] Client cree: client1 / client123")
    
    # Creer des categories
    categories_data = [
        {'name': 'Electronique', 'description': 'Appareils electroniques et accessoires'},
        {'name': 'Vetements', 'description': 'Mode et accessoires vestimentaires'},
        {'name': 'Maison & Jardin', 'description': 'Articles pour la maison et le jardin'},
        {'name': 'Sports & Loisirs', 'description': 'Equipements sportifs et loisirs'},
        {'name': 'Livres', 'description': 'Livres et magazines'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print("[OK] Categorie creee: {0}".format(category.name))
    
    # Creer des etiquettes
    tags_data = ['Nouveau', 'Promotion', 'Populaire', 'Ecologique', 'Premium', 'Soldes']
    
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            print("[OK] Etiquette creee: {0}".format(tag.name))
    
    # Creer des produits d'exemple
    electronique = Category.objects.get(name='Electronique')
    vetements = Category.objects.get(name='Vetements')
    maison = Category.objects.get(name='Maison & Jardin')
    
    nouveau_tag = Tag.objects.get(name='Nouveau')
    promo_tag = Tag.objects.get(name='Promotion')
    populaire_tag = Tag.objects.get(name='Populaire')
    
    products_data = [
        {
            'name': 'Smartphone XPro 12',
            'description': 'Smartphone derniere generation avec ecran AMOLED 6.5", 128Go de stockage, camera 48MP',
            'price': 599.99,
            'stock': 25,
            'category': electronique,
            'tags': [nouveau_tag, populaire_tag],
        },
        {
            'name': 'Casque Bluetooth Premium',
            'description': 'Casque sans fil avec reduction de bruit active, autonomie 30h, son haute fidelite',
            'price': 149.99,
            'stock': 40,
            'category': electronique,
            'tags': [populaire_tag],
        },
        {
            'name': 'T-shirt Coton Bio',
            'description': 'T-shirt 100% coton biologique, disponible en plusieurs couleurs, coupe moderne',
            'price': 24.99,
            'stock': 100,
            'category': vetements,
            'tags': [promo_tag],
        },
        {
            'name': 'Jean Slim Stretch',
            'description': 'Jean confortable avec stretch, coupe slim, lavage stone, toutes tailles disponibles',
            'price': 49.99,
            'stock': 60,
            'category': vetements,
            'tags': [populaire_tag],
        },
        {
            'name': 'Lampe LED Design',
            'description': "Lampe de bureau LED avec variateur d'intensite, design moderne, economie d'energie",
            'price': 39.99,
            'stock': 30,
            'category': maison,
            'tags': [nouveau_tag],
        },
        {
            'name': 'Set de 4 Coussins Deco',
            'description': 'Ensemble de 4 coussins decoratifs 40x40cm, housses lavables, motifs modernes',
            'price': 34.99,
            'stock': 50,
            'category': maison,
            'tags': [promo_tag],
        },
    ]
    
    for prod_data in products_data:
        tags = prod_data.pop('tags', [])
        if not Product.objects.filter(name=prod_data['name']).exists():
            product = Product.objects.create(
                seller=vendeur,
                is_active=True,
                **prod_data
            )
            product.tags.set(tags)
            print("[OK] Produit cree: {0}".format(product.name))
    
    print("\n[SUCCESS] Donnees d'exemple creees avec succes!")
    print("\n[INFO] Comptes crees:")
    print("   Admin: admin / admin123")
    print("   Vendeur: vendeur1 / vendeur123")
    print("   Client: client1 / client123")
    print("\n[INFO] Acces au site: http://127.0.0.1:8000/")
    print("[INFO] Administration: http://127.0.0.1:8000/admin/")


if __name__ == '__main__':
    create_sample_data()


