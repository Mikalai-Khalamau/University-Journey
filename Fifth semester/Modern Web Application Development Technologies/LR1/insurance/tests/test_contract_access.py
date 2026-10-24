import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_client_can_open_own_contract_detail(
    client, user_client_group, client_record, contract
):
    client_record.user = user_client_group
    client_record.save()
    contract.client = client_record
    contract.save()
    client.force_login(user_client_group)
    url = reverse("insurance:contract-detail", kwargs={"pk": contract.pk})
    r = client.get(url)
    assert r.status_code == 200


@pytest.mark.django_db
def test_client_cannot_open_other_contract(client, user_client_group, contract):
    client.force_login(user_client_group)
    url = reverse("insurance:contract-detail", kwargs={"pk": contract.pk})
    assert client.get(url).status_code == 403
