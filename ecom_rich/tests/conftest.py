import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model

from shop.models import Category, Product, Cart, CartItem, Order, OrderItem


@pytest.fixture
def user_password():
    return "TestPassword123!"


@pytest.fixture
def visitor_user(db, user_password):
    User = get_user_model()
    return User.objects.create_user(
        username="client_test",
        email="client@example.com",
        password=user_password,
        user_type="visitor",
        first_name="Client",
        last_name="Testeur",
        phone="0102030405",
        address="10 rue du Test, Paris"
    )


@pytest.fixture
def seller_user(db, user_password):
    User = get_user_model()
    return User.objects.create_user(
        username="vendeur_test",
        email="vendeur@example.com",
        password=user_password,
        user_type="seller",
        first_name="Vendeur",
        last_name="Expert",
        phone="0607080910",
        address="20 avenue Qualité, Lyon"
    )


@pytest.fixture
def admin_user(db, user_password):
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin_test",
        email="admin@example.com",
        password=user_password,
        user_type="admin"
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronique", description="Produits électroniques de test")


@pytest.fixture
def product(db, category, seller_user):
    return Product.objects.create(
        name="Smartphone QA",
        description="Appareil de test pour la boutique",
        price=Decimal("150000.00"),
        stock=10,
        category=category,
        seller=seller_user,
        is_active=True
    )


@pytest.fixture
def cart(db, visitor_user):
    return Cart.objects.create(user=visitor_user)


@pytest.fixture
def cart_item(db, cart, product):
    return CartItem.objects.create(cart=cart, product=product, quantity=2)


@pytest.fixture
def order(db, visitor_user, seller_user, product):
    order = Order.objects.create(
        user=visitor_user,
        status="pending",
        total_amount=product.price,
        shipping_address=visitor_user.address or "Adresse test",
        phone=visitor_user.phone or "0102030405",
        notes="Commande de test"
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price=product.price
    )
    return order
