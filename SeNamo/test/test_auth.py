from django.test import TestCase,Client
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

    def test_get_register_page(self):
        url = '/register'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        print(response)
        self.assertContains(response,'form')

    def test_register(self):
        username = 'mark'
        password = 'mark'
        email = 'mark.z@facebook.com'

        url = '/register'
        params = {
            'username' : username,
            'password' : password,
            'confirm_password' : password,
            'email' : email,
            'confirm_email' : email
        }

        #client = Client(enforce_csrf_checks=False)
        response = self.client.post(url,params,follow=True)

        print(response)
        self.assertIn(User.objects.get(username=username),User.objects.all())
        self.assertContains(response,"successfully registered.")
