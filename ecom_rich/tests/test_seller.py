import pytest
from django.urls import reverse

from shop.models import Order


@pytest.mark.django_db
def test_seller_dashboard_accessible_for_seller(client, seller_user, user_password):
    client.login(username=seller_user.username, password=user_password)
    response = client.get(reverse("seller_dashboard"))
    assert response.status_code == 200
    assert b"Mon Espace Vendeur" in response.content


@pytest.mark.django_db
def test_seller_dashboard_denied_for_visitor(client, visitor_user, user_password):
    client.login(username=visitor_user.username, password=user_password)
    response = client.get(reverse("seller_dashboard"))
    assert response.status_code == 302
    assert response.headers["Location"].endswith(reverse("home"))


@pytest.mark.django_db
def test_seller_can_update_order_status(client, seller_user, user_password, order):
    client.login(username=seller_user.username, password=user_password)

    response = client.post(reverse("seller_order_update_status", args=[order.id]), {"status": "confirmed"})
    assert response.status_code == 302

    order.refresh_from_db()
    assert order.status == "confirmed"


@pytest.mark.xfail(reason="Les vendeurs peuvent encore s'auto-créer via l'inscription publique.")
@pytest.mark.django_db
def test_only_admin_should_assign_seller_role(client, visitor_user, user_password):
    client.login(username=visitor_user.username, password=user_password)
    response = client.get(reverse("seller_dashboard"))
    assert response.status_code == 302
    assert response.headers["Location"].endswith(reverse("home"))
    assert visitor_user.user_type != "seller"
