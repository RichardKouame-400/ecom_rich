from django.urls import path
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('produits/', views.product_list, name='product_list'),
    path('produit/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Authentification
    path('inscription/', views.register, name='register'),
    path('connexion/', views.user_login, name='login'),
    path('deconnexion/', views.user_logout, name='logout'),
    
    # Espace vendeur
    path('vendeur/tableau-de-bord/', views.seller_dashboard, name='seller_dashboard'),
    path('vendeur/produit/creer/', views.product_create, name='product_create'),
    path('vendeur/produit/<int:pk>/modifier/', views.product_edit, name='product_edit'),
    path('vendeur/produit/<int:pk>/supprimer/', views.product_delete, name='product_delete'),
    
    # Panier
    path('panier/', views.cart_view, name='cart_view'),
    path('panier/ajouter/<int:pk>/', views.cart_add, name='cart_add'),
    path('panier/modifier/<int:pk>/', views.cart_update, name='cart_update'),
    path('panier/retirer/<int:pk>/', views.cart_remove, name='cart_remove'),
    
    # Commandes
    path('commander/', views.checkout, name='checkout'),
    path('mes-commandes/', views.order_list, name='order_list'),
    path('commande/<int:pk>/', views.order_detail, name='order_detail'),
    
    # Gestion commandes vendeur
    path('vendeur/commandes/', views.seller_orders, name='seller_orders'),
    path('vendeur/commande/<int:pk>/', views.seller_order_detail, name='seller_order_detail'),
    path('vendeur/commande/<int:pk>/statut/', views.seller_order_update_status, name='seller_order_update_status'),
]


