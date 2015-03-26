from django.test import TestCase
from django.test.client import Client


class AdminURLTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_security_admin_url(self):
        try:
            from seeseehome import security_informaion
            ADMIN_URL = security_information.ADMIN_URL
        except:
            AttributeError("Security URL for Admin page was not set")

    def get_admin_url(self):
        from seeseehome import security_informaion
        ADMIN_URL = security_information.ADMIN_URL
        response = self.client.get('/' + ADMIN_URL + '/')
        self.assertEqual(response.status_code, 200)
