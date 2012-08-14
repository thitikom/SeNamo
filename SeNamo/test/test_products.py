from django.test import TestCase

class ProductsTestSuite(TestCase):
    def setUP(self):
        pass
    def tearDown(self):
        pass

    def test_delete_product(self):
        url = '/product/%d/delete'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.fail('not finished')