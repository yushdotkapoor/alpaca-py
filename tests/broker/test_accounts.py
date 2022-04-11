import pytest
import requests_mock

from alpaca.common import APIError
from alpaca.broker.client import BrokerClient
from alpaca.broker.models import Account


@pytest.fixture
def reqmock():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def client():
    client = BrokerClient("key-id", "secret-key")
    return client


@pytest.fixture
def raw_client():
    raw_client = BrokerClient("key-id", "secret-key", raw_data=True)
    return raw_client


def test_get_account(reqmock, client: BrokerClient):
    account_id = "2a87c088-ffb6-472b-a4a3-cd9305c8605c"

    reqmock.get(
        f"https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}",
        text="""
        {
          "id": "2a87c088-ffb6-472b-a4a3-cd9305c8605c",
          "account_number": "601865070",
          "status": "ACTIVE",
          "crypto_status": "INACTIVE",
          "currency": "USD",
          "last_equity": "47604.17306484226",
          "created_at": "2022-01-21T21:25:26.470131Z",
          "contact": {
            "email_address": "agitated_golick_69906574@example.com",
            "phone_number": "386-555-3557",
            "street_address": [
              "20 N San Mateo Dr"
            ],
            "city": "San Mateo",
            "state": "CA",
            "postal_code": "94401"
          },
          "identity": {
            "given_name": "Agitated",
            "family_name": "Golick",
            "date_of_birth": "1970-01-01",
            "tax_id_type": "USA_SSN",
            "country_of_citizenship": "USA",
            "country_of_birth": "USA",
            "country_of_tax_residence": "USA",
            "funding_source": [
              "employment_income"
            ],
            "visa_type": null,
            "visa_expiration_date": null,
            "date_of_departure_from_usa": null,
            "permanent_resident": null
          },
          "disclosures": {
            "is_control_person": false,
            "is_affiliated_exchange_or_finra": false,
            "is_politically_exposed": false,
            "immediate_family_exposed": false,
            "is_discretionary": false
          },
          "agreements": [
            {
              "agreement": "margin_agreement",
              "signed_at": "2022-01-21T21:25:26.466094194Z",
              "ip_address": "127.0.0.1",
              "revision": null
            },
            {
              "agreement": "customer_agreement",
              "signed_at": "2022-01-21T21:25:26.466094194Z",
              "ip_address": "127.0.0.1",
              "revision": null
            },
            {
              "agreement": "account_agreement",
              "signed_at": "2022-01-21T21:25:26.466094194Z",
              "ip_address": "127.0.0.1",
              "revision": null
            }
          ],
          "documents": [
            {
              "document_type": "identity_verification",
              "document_sub_type": "passport",
              "id": "bb6de14c-9393-4b6c-8e93-c6724ac7b703",
              "content": "https://example.com/not-a-real-url",
              "created_at": "2022-01-21T21:25:28.189455Z"
            }
          ],
          "trusted_contact": {
            "given_name": "Jane",
            "family_name": "Doe",
            "email_address": "agitated_golick_69906574@example.com"
          },
          "account_type": "trading",
          "trading_configurations": null
        }
            """,
    )

    account = client.get_account_by_id(account_id)

    assert type(account) == Account
    assert account.id == account_id


def test_get_account_account_not_found(reqmock, client: BrokerClient):
    account_id = "2a87c088-ffb6-472b-a4a3-cd9305c8605c"

    # Api returns an unauthorized if you try to ask for a uuid thats not one of your accounts
    reqmock.get(
        f"https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}",
        status_code=401,
        text="""
        {
          "code": 40110000,
          "message": "request is not authorized"
        }
        """,
    )

    with pytest.raises(APIError) as error:
        client.get_account_by_id(account_id)

    assert error.value.status_code == 401


def test_get_account_validates_non_uuid_str(client: BrokerClient):
    with pytest.raises(ValueError):
        client.get_account_by_id("not a valid uuid")

    with pytest.raises(ValueError):
        client.get_account_by_id(4)
