import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_about_page(client):
    r = client.get(reverse("insurance:about"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_privacy_page(client):
    r = client.get(reverse("insurance:privacy"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_news_list(client):
    r = client.get(reverse("insurance:news-list"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_cart_page(client):
    r = client.get(reverse("insurance:cart"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_checkout_page(client):
    r = client.get(reverse("insurance:checkout"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_glossary_page(client):
    r = client.get(reverse("insurance:glossary"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_contacts_page(client):
    r = client.get(reverse("insurance:contacts"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_vacancies_page(client):
    r = client.get(reverse("insurance:vacancies"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_reviews_page(client):
    r = client.get(reverse("insurance:reviews"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_promos_page(client):
    r = client.get(reverse("insurance:promos"))
    assert r.status_code == 200
