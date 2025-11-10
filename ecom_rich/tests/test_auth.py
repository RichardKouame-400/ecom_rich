import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_success_redirects_home(client, visitor_user, user_password):
    response = client.post(reverse("login"), {"username": visitor_user.username, "password": user_password})
    assert response.status_code == 302
    assert response.headers["Location"].endswith(reverse("home"))


@pytest.mark.django_db
def test_login_invalid_credentials_shows_error(client, visitor_user):
    response = client.post(reverse("login"), {"username": visitor_user.username, "password": "wrong-pass"})
    assert response.status_code == 200
    assert b"alert" in response.content


@pytest.mark.xfail(reason="Le formulaire d'inscription expose encore le champ user_type au public.")
@pytest.mark.django_db
def test_public_registration_should_not_expose_user_type(client):
    response = client.get(reverse("register"))
    assert b"user_type" not in response.content


@pytest.mark.xfail(reason="Le site doit proposer un CTA vendeur informatif plutôt qu'une auto-inscription.")
@pytest.mark.django_db
def test_homepage_should_not_instantly_offer_become_seller_cta(client):
    response = client.get(reverse("home"))
    assert b"Devenir Vendeur" not in response.content


@pytest.mark.xfail(reason="Workflow de r\u00e9initialisation de mot de passe non configur\u00e9.")
def test_password_reset_route_available():
    reverse("password_reset")


@pytest.mark.xfail(reason="Page contact manquante dans les URLs publiques.")
def test_contact_page_accessible(client):
    response = client.get("/contact/")
    assert response.status_code == 200
