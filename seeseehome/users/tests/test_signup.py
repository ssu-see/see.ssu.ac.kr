from django.test import TestCase
from users.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from seeseehome import testdata, msg
from django.test.client import Client
from django.core.urlresolvers import reverse


class UserSignUpTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_response_to_signup_page(self):
        response = self.client.get(reverse("users:signup"), follow=True)
        self.assertEqual(response.wsgi_request.path, reverse("users:signup"))
    """
    # signup test method has a problem.
    def test_signup(self):
        response = \
            self.client.post(
                reverse("users:signup"),
                {
                    "uesrname" : testdata.users_valid_name,
                    "email" : testdata.users_valid_email,
                    "pwd" : testdata.users_valid_password,
                    "confirm_pwd" : testdata.users_valid_password,
                },
            )

        self.assertIsNotNone(
            User.objects.get(username = testdata.users_valid_name)
        )
        self.assertContains(request, msg.users_signup_success)
        self.assertContains(request, msg.users_signup_success_info)
    """
