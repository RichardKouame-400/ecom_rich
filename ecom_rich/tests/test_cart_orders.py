from decimal import Decimal

import pytest
from django.urls import reverse

from shop.models import CartItem, Order, OrderItem


@pytest.mark.django_db
def test_add_product_to_cart_flow(client, visitor_user, user_password, product):
    client.login(username=visitor_user.username, password=user_password)

    response = client.post(reverse("cart_add", args=[product.id]), {"quantity": 2})
    assert response.status_code == 302
    assert response.headers["Location"].endswith(reverse("cart_view"))

    cart_item = CartItem.objects.get(cart__user=visitor_user, product=product)
    assert cart_item.quantity == 2


@pytest.mark.django_db
def test_add_product_to_cart_stock_guard(client, visitor_user, user_password, product):
    client.login(username=visitor_user.username, password=user_password)
    response = client.post(reverse("cart_add", args=[product.id]), {"quantity": product.stock + 5})
    assert response.status_code == 302
    assert response.headers["Location"].endswith(reverse("product_detail", args=[product.id]))


@pytest.mark.django_db
def test_checkout_creates_order_and_decrements_stock(client, visitor_user, user_password, product):
    client.login(username=visitor_user.username, password=user_password)
    client.post(reverse("cart_add", args=[product.id]), {"quantity": 2})

    payload = {
        "shipping_address": "10 rue du Test, Paris",
        "phone": "0101010101",
        "notes": "Livraison express",
    }
    response = client.post(reverse("checkout"), payload)
    assert response.status_code == 302

    order = Order.objects.get(user=visitor_user)
    assert order.total_amount == Decimal("300000.00")
    assert order.status == "pending"

    order_item = OrderItem.objects.get(order=order, product=product)
    assert order_item.quantity == 2

    product.refresh_from_db()
    assert product.stock == 8


@pytest.mark.django_db
def test_checkout_with_empty_cart_displays_error(client, visitor_user, user_password):
    from shop.models import Cart

    Cart.objects.create(user=visitor_user)

    client.login(username=visitor_user.username, password=user_password)

    response = client.post(reverse("checkout"), {"shipping_address": "vide", "phone": "0000"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith(reverse("cart_view"))
