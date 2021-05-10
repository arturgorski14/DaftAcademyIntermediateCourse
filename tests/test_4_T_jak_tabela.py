from unittest import mock
import pytest


@pytest.mark.skip
class TestEndpointsSqlLite:
    def test_return_all_categories_and_customers(self) -> None:
        self._given_all_sample_categories()
        self._given_all_sample_customers()

    def _given_all_sample_categories(self) -> None:
        self.sample_categories = [{
            'CategoryID': 1,
            'Description': 'something',
            'Picture': 'pic.jpg'
        }, {
            'CategoryID': 2,
            'Description': 'something',
            'Picture': 'pic.jpg'
        }, {
            'CategoryID': 3,
            'Description': 'something',
            'Picture': 'pic.jpg'
        }]

    def _given_all_sample_customers(self) -> None:
        self.sample_customers = [{
            'CustomerID': 1,
            'CompanyName': 'company_name',
            'ContractName': 'pic.jpg',
            'ContractTitle': 'title',
            'Address': 'address',
        }, {
            'CustomerID': 2,
            'CompanyName': 'company_name',
            'ContractName': 'pic.jpg',
            'ContractTitle': 'title',
            'Address': 'address',
        }, {
            'CustomerID': 3,
            'CompanyName': 'company_name',
            'ContractName': 'pic.jpg',
            'ContractTitle': 'title',
            'Address': 'address',
        }]
