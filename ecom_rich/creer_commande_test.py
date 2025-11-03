# -*- coding: utf-8 -*-
"""
Script pour creer une commande de test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_richard.settings')
django.setup()

from shop.models import User, Product, Order, OrderItem, Cart, CartItem


def create_test_order():
    print("Creation d'une commande de test...")
    
    # Récupérer le client et le vendeur
    try:
        client = User.objects.get(username='client1')
        vendeur = User.objects.get(username='vendeur1')
    except User.DoesNotExist:
        print("[ERREUR] Utilisateurs non trouves. Executez d'abord create_sample_data.py")
        return
    
    # Récupérer les produits du vendeur
    produits = Product.objects.filter(seller=vendeur, is_active=True)[:2]
    
    if not produits:
        print("[ERREUR] Aucun produit trouve pour le vendeur1")
        return
    
    print(f"[OK] Client : {client.username}")
    print(f"[OK] Vendeur : {vendeur.username}")
    print(f"[OK] Produits a commander : {produits.count()}")
    
    # Créer une commande
    order = Order.objects.create(
        user=client,
        status='pending',  # En attente
        total_amount=0,  # Sera calculé
        shipping_address='123 Rue de Test, 75001 Paris',
        phone='0123456789',
        notes='Commande de test pour tester la confirmation'
    )
    
    print(f"\n[OK] Commande creee : #{order.id}")
    print(f"[OK] Statut : {order.get_status_display()}")
    
    # Ajouter les produits
    total = 0
    for produit in produits:
        quantity = 2
        OrderItem.objects.create(
            order=order,
            product=produit,
            quantity=quantity,
            price=produit.price
        )
        subtotal = quantity * produit.price
        total += subtotal
        print(f"[OK] Ajoute : {quantity}x {produit.name} = {subtotal} EUR")
    
    # Mettre à jour le total
    order.total_amount = total
    order.save()
    
    print(f"\n[OK] Total commande : {total} EUR")
    print(f"\n[SUCCESS] Commande de test creee avec succes !")
    print(f"\n[INFO] Maintenant :")
    print(f"  1. Connectez-vous comme vendeur1")
    print(f"  2. Allez sur Dashboard > Commandes")
    print(f"  3. Vous devriez voir la commande #{order.id} en 'En attente'")
    print(f"  4. Cliquez sur le bouton vert [V] pour confirmer")
    print(f"\n[INFO] URL directe : http://127.0.0.1:8000/vendeur/commandes/")


if __name__ == '__main__':
    create_test_order()

