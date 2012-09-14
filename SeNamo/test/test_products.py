from django.test import TestCase
from app.models import Product, Category
from mock import MagicMock,patch
import requests

class ProductsTestSuite(TestCase):
    def setUP(self):
        pass
    def tearDown(self):
        pass

    def test_delete_product(self):
        category = Category.objects.create(name='Test Category',description='Category description')
        product = Product.objects.create(
            name = 'Test',
            price = '111',
            point = '222',
            category = category,
            description = 'Product description',
            image = None,
        )
        url = '/product/%d/delete' % product.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertNotIn(product,Product.objects.all())
        print(response.content)
        self.assertContains(response,"Successfully delete product.")

    def test_mock(self):
        # Stub response from outside
        mocked_response = MagicMock()
        mocked_response.status_code = 200
        mocked_response.content = 'yes' \
                                  ''
        requests.get = mocked_response




        url = '/'
        response = self.client.get(url)

        print(response)
        mocked_response.assert_called_once_with('haha')
        self.assertEqual(response.status_code,200)
        self.fail('not finish')