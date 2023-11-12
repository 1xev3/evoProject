import unittest
import logging

import requests
import pydantic
import typing


ENTRYPOINT = "http://product-service:5010"
PRODUCT_DELETED_MESSAGE = {"message": "Deleted"}

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s | %(message)s"
)

class Product(pydantic.BaseModel):
    product_name: str
    description: str
    id: str
    status: int
    images: list[typing.Any]

class TestCase(unittest.TestCase):
    def test_get_products(self):
        response = requests.get(f"{ENTRYPOINT}/products")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def _create_product(self, name="test_product", desc="test_description") -> Product:
        payload = {
            "product_name": name,
            "description": desc
        }
        response = requests.post(f"{ENTRYPOINT}/products", json=payload)
        self.assertEqual(response.status_code, 200)
        return Product(**response.json())
    
    def _update_product(self, product_id, name="test_product", desc="test_description", status=2) -> Product:
        payload = {
            "product_name": name,
            "description": desc,
            "status": status
        }
        response = requests.put(f"{ENTRYPOINT}/products/{product_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        return Product(**response.json())
    
    def _del_product(self, product_id) -> requests.Response:
        response = requests.delete(f"{ENTRYPOINT}/products/{product_id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), PRODUCT_DELETED_MESSAGE)
        return response

    def test_create_delete_product(self):
        prod = self._create_product(name="test_product", desc="test_description")
        try:
            self.assertIsInstance(prod, Product)
            self.assertEqual(prod.product_name, "test_product")
            self.assertEqual(prod.description, "test_description")
        finally:
            self._del_product(prod.id)

    def test_update_product(self):
        prod = self._create_product()
        try:
            prod_updated = self._update_product(prod.id, name="two_test_product", desc="two_test_description", status=2)
            self.assertIsInstance(prod_updated, Product)
            self.assertEqual(prod_updated.product_name, "two_test_product")
            self.assertEqual(prod_updated.description, "two_test_description")
            self.assertEqual(prod_updated.status, 2)
        finally:
            self._del_product(prod.id)