import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_loads(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert b"Bienvenue" in response.content


@pytest.mark.django_db
def test_product_list_accessible(client):
    response = client.get(reverse("product_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration_page_accessible(client):
    response = client.get(reverse("register"))
    assert response.status_code == 200


@pytest.mark.xfail(reason="La page FAQ n'est pas encore implémentée.")
def test_faq_page_should_exist(client):
    response = client.get("/faq/")
    assert response.status_code == 200
