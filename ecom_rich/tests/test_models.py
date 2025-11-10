from decimal import Decimal

import pytest

from shop.models import CartItem, Order, Product


@pytest.mark.django_db
def test_cart_total_updates(cart, product, category, seller_user):
    cart.items.all().delete()
    CartItem.objects.create(cart=cart, product=product, quantity=3)

    second_product = Product.objects.create(
        name="Casque QA",
        description="Accessoire audio",
        price=Decimal("50000.00"),
        stock=5,
        category=category,
        seller=seller_user,
        is_active=True,
    )
    CartItem.objects.create(cart=cart, product=second_product, quantity=1)

    assert cart.get_item_count() == 4
    assert cart.get_total() == product.price * 3 + Decimal("50000.00")


@pytest.mark.django_db
def test_cart_item_subtotal(cart_item, product):
    expected = product.price * 2
    assert cart_item.get_subtotal() == expected


@pytest.mark.django_db
def test_order_string_representation(order, visitor_user):
    label = str(order)
    assert f"Commande #{order.id}" in label
    assert visitor_user.username in label
    assert Order.STATUS_CHOICES[0][1] in label


@pytest.mark.django_db
def test_order_status_choices_cover_expected_states():
    statuses = {code for code, _ in Order.STATUS_CHOICES}
    assert statuses == {"pending", "confirmed", "shipped", "delivered", "cancelled"}
