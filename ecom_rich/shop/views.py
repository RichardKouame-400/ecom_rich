from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Tag, Cart, CartItem, Order, OrderItem, User
from .forms import UserRegistrationForm, UserLoginForm, ProductForm, OrderForm


# ==================== Vues publiques ====================

def home(request):
    """Page d'accueil avec les produits récents"""
    products = Product.objects.filter(is_active=True).select_related('category', 'seller')[:8]
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    """Liste de tous les produits avec filtres"""
    products = Product.objects.filter(is_active=True).select_related('category', 'seller')
    
    # Filtrage par catégorie
    category_id = request.GET.get('category')
    current_category_int = None
    if category_id:
        try:
            current_category_int = int(category_id)
            products = products.filter(category_id=current_category_int)
        except ValueError:
            pass
    
    # Filtrage par étiquette
    tag_id = request.GET.get('tag')
    current_tag_int = None
    if tag_id:
        try:
            current_tag_int = int(tag_id)
            products = products.filter(tags__id=current_tag_int)
        except ValueError:
            pass
    
    # Recherche
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        'current_category': current_category_int,
        'current_tag': current_tag_int,
        'search_query': search,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Détails d'un produit"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


# ==================== Authentification ====================

def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ! Votre compte a été créé avec succès.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'shop/register.html', {'form': form})


def user_login(request):
    """Connexion d'un utilisateur"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = UserLoginForm()
    
    return render(request, 'shop/login.html', {'form': form})


def user_logout(request):
    """Déconnexion d'un utilisateur"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('home')


# ==================== Gestion des produits (Vendeurs) ====================

@login_required
def seller_dashboard(request):
    """Tableau de bord du vendeur"""
    if request.user.user_type != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs.')
        return redirect('home')
    
    products = Product.objects.filter(seller=request.user)
    
    context = {
        'products': products,
        'total_products': products.count(),
        'active_products': products.filter(is_active=True).count(),
    }
    return render(request, 'shop/seller_dashboard.html', context)


@login_required
def product_create(request):
    """Création d'un nouveau produit"""
    if request.user.user_type != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            form.save_m2m()  # Sauvegarder les tags (ManyToMany)
            messages.success(request, 'Produit créé avec succès !')
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Créer un produit'})


@login_required
def product_edit(request, pk):
    """Modification d'un produit"""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès !')
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Modifier le produit'})


@login_required
def product_delete(request, pk):
    """Suppression d'un produit"""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produit supprimé avec succès !')
        return redirect('seller_dashboard')
    
    return render(request, 'shop/product_confirm_delete.html', {'product': product})


# ==================== Panier ====================

@login_required
def cart_view(request):
    """Affichage du panier"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context)


@login_required
def cart_add(request, pk):
    """Ajout d'un produit au panier"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, 'Stock insuffisant.')
        return redirect('product_detail', pk=pk)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            messages.error(request, 'Stock insuffisant.')
            return redirect('cart_view')
        cart_item.save()
    
    messages.success(request, f'{product.name} ajouté au panier.')
    return redirect('cart_view')


@login_required
def cart_update(request, pk):
    """Mise à jour de la quantité d'un article du panier"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Article retiré du panier.')
    elif quantity > cart_item.product.stock:
        messages.error(request, 'Stock insuffisant.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Panier mis à jour.')
    
    return redirect('cart_view')


@login_required
def cart_remove(request, pk):
    """Suppression d'un article du panier"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
    cart_item.delete()
    
    messages.success(request, 'Article retiré du panier.')
    return redirect('cart_view')


# ==================== Commandes ====================

@login_required
def checkout(request):
    """Processus de commande"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Votre panier est vide.')
        return redirect('cart_view')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Vérifier le stock avant de créer la commande
            for item in cart.items.all():
                if item.quantity > item.product.stock:
                    messages.error(request, f'Stock insuffisant pour {item.product.name}.')
                    return redirect('cart_view')
            
            # Créer la commande
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total()
            order.save()
            
            # Créer les items de commande et mettre à jour le stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                # Décrémenter le stock
                item.product.stock -= item.quantity
                item.product.save()
            
            # Vider le panier
            cart.items.all().delete()
            
            messages.success(request, f'Commande #{order.id} passée avec succès !')
            return redirect('order_detail', pk=order.id)
    else:
        # Pré-remplir avec les infos de l'utilisateur
        initial_data = {
            'phone': request.user.phone,
            'shipping_address': request.user.address,
        }
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def order_list(request):
    """Liste des commandes de l'utilisateur"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    
    context = {
        'orders': orders,
    }
    return render(request, 'shop/order_list.html', context)


@login_required
def order_detail(request, pk):
    """Détails d'une commande"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_detail.html', context)


# ==================== Gestion des commandes (Vendeurs) ====================

@login_required
def seller_orders(request):
    """Liste des commandes contenant les produits du vendeur"""
    if request.user.user_type != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs.')
        return redirect('home')
    
    # Récupérer les commandes contenant les produits du vendeur
    from django.db.models import Q
    orders = Order.objects.filter(
        items__product__seller=request.user
    ).distinct().order_by('-created_at')
    
    # Statistiques
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    completed_orders = orders.filter(status='delivered').count()
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
    }
    return render(request, 'shop/seller_orders.html', context)


@login_required
def seller_order_detail(request, pk):
    """Détails d'une commande pour le vendeur"""
    if request.user.user_type != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs.')
        return redirect('home')
    
    # Récupérer la commande
    order = get_object_or_404(Order, pk=pk)
    
    # Filtrer uniquement les articles du vendeur
    seller_items = order.items.filter(product__seller=request.user)
    
    # Vérifier que la commande contient au moins un produit du vendeur
    if not seller_items.exists():
        messages.error(request, 'Cette commande ne contient aucun de vos produits.')
        return redirect('seller_orders')
    
    # Calculer le total pour le vendeur
    seller_total = sum(item.get_subtotal() for item in seller_items)
    
    context = {
        'order': order,
        'seller_items': seller_items,
        'seller_total': seller_total,
    }
    return render(request, 'shop/seller_order_detail.html', context)


@login_required
def seller_order_update_status(request, pk):
    """Mise à jour du statut d'une commande par le vendeur"""
    # Debug
    print(f"\n===== DEBUG SELLER ORDER UPDATE =====")
    print(f"User: {request.user.username} ({request.user.user_type})")
    print(f"Method: {request.method}")
    print(f"Order ID: {pk}")
    print(f"POST data: {request.POST}")
    
    if request.user.user_type != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs.')
        return redirect('home')
    
    if request.method != 'POST':
        print("Not POST, redirecting...")
        return redirect('seller_orders')
    
    # Récupérer la commande
    order = get_object_or_404(Order, pk=pk)
    print(f"Order found: #{order.id}, current status: {order.status}")
    
    # Vérifier que la commande contient des produits du vendeur
    seller_items = order.items.filter(product__seller=request.user)
    print(f"Seller items count: {seller_items.count()}")
    
    if not seller_items.exists():
        messages.error(request, 'Cette commande ne contient aucun de vos produits.')
        return redirect('seller_orders')
    
    # Récupérer le nouveau statut
    new_status = request.POST.get('status')
    print(f"New status requested: {new_status}")
    
    # Valider et mettre à jour le statut
    valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    if new_status in valid_statuses:
        old_status_display = order.get_status_display()
        order.status = new_status
        order.save()
        print(f"Status updated! Old: {old_status_display}, New: {order.get_status_display()}")
        
        # Message de succès avec émojis
        status_emoji = {
            'pending': '',
            'confirmed': '',
            'shipped': '',
            'delivered': '',
            'cancelled': ''
        }
        
        messages.success(
            request, 
            f'Statut de la commande #{order.id} mis a jour : {old_status_display} -> {order.get_status_display()}'
        )
        print(f"Success message added")
    else:
        print(f"Invalid status: {new_status}")
        messages.error(request, 'Statut invalide.')
    
    # Redirection intelligente : retour d'où on vient
    return_to_list = request.POST.get('return_to_list', 'false')
    print(f"Return to list: {return_to_list}")
    print(f"===== END DEBUG =====\n")
    
    if return_to_list == 'true':
        return redirect('seller_orders')
    else:
        return redirect('seller_order_detail', pk=pk)
