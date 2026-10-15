import unittest

from app import app


class ProductsBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук".encode("utf-8"), response.data)
        self.assertIn("Смартфон".encode("utf-8"), response.data)
        self.assertIn("Навушники".encode("utf-8"), response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук".encode("utf-8"), response.data)
        self.assertIn(b"35000", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()