import importlib

import pytest
from django.contrib.auth import get_user_model

from shop.models import Category, Product


@pytest.mark.django_db
def test_create_sample_data_script_creates_baseline_users():
    module = importlib.import_module("create_sample_data")
    module.create_sample_data()

    User = get_user_model()
    assert User.objects.filter(username="admin").exists()
    assert User.objects.filter(username="vendeur1", user_type="seller").exists()
    assert User.objects.filter(username="client1", user_type="visitor").exists()


@pytest.mark.django_db
def test_create_sample_data_script_populates_catalogue():
    module = importlib.import_module("create_sample_data")
    module.create_sample_data()

    assert Category.objects.exists()
    assert Product.objects.exists()
