from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """Modèle utilisateur personnalisé avec rôles"""
    USER_TYPE_CHOICES = (
        ('visitor', 'Visiteur'),
        ('seller', 'Vendeur'),
        ('admin', 'Administrateur'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='visitor')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Category(models.Model):
    """Catégorie de produits"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Étiquettes pour les produits"""
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = "Étiquette"
        verbose_name_plural = "Étiquettes"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Produit mis en vente par un vendeur"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Prix")
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Catégorie")
    tags = models.ManyToManyField(Tag, blank=True, related_name='products', verbose_name="Étiquettes")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', limit_choices_to={'user_type': 'seller'}, verbose_name="Vendeur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.price} CFA"


class Cart(models.Model):
    """Panier d'un utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Utilisateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"
    
    def __str__(self):
        return f"Panier de {self.user.username}"
    
    def get_total(self):
        """Calcule le total du panier"""
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_item_count(self):
        """Retourne le nombre total d'articles"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Article dans un panier"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Panier")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name="Quantité")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Ajouté le")
    
    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_subtotal(self):
        """Calcule le sous-total de l'article"""
        if self.quantity and self.product and self.product.price:
            return self.quantity * self.product.price
        return 0


class Order(models.Model):
    """Commande passée par un utilisateur"""
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Utilisateur")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    shipping_address = models.TextField(verbose_name="Adresse de livraison")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créée le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifiée le")
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commande #{self.id} - {self.user.username} - {self.get_status_display()}"


class OrderItem(models.Model):
    """Article dans une commande"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Commande")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Quantité")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    
    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_subtotal(self):
        """Calcule le sous-total de l'article"""
        if self.quantity and self.price:
            return self.quantity * self.price
        return 0
