from django.test import TestCase
from django.core.urlresolvers import  reverse
from django.contrib.auth.models import  User

class AuthTestCase(TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_login(self):
        username = 'mark'
        password = 'mark'
        email = 'mark.z@facebook.com'
        member = User.objects.create_user(username,email,password)
        response = self.client.login(username=username,password=password)
        self.assertTrue(response)

    def test_logout(self):
        username = 'mark'
        password = 'mark'
        email = 'mark.z@facebook.com'
        member = User.objects.create_user(username,email,password)
        self.client.login(username=username,password=password)
        url = '/logout'
        response = self.client.get(url,follow=True)
        print(response)
        self.assertEqual(200,response.status_code)
