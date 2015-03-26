from django.test import TestCase
from linkboard.models import LinkPost
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from seeseehome import testdata
from users.models import User


class LinkPostManagerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password
        )

##########
# CREATE POST TEST
    def test_create_linkpost_with_writer_who_has_invalid_permission(self):
        self.assertRaises(
            ValidationError,
            LinkPost.objects.create_linkpost,
            description=testdata.linkboard_valid_description,
            url=testdata.linkboard_valid_url,
            writer=self.user
        )

    def test_create_linkpost_with_writer_who_has_valid_permission(self):
        self.user.userperm = testdata.perm_member
        self.assertIsNotNone(
            LinkPost.objects.create_linkpost(
                description=testdata.linkboard_valid_description,
                url=testdata.linkboard_valid_url,
                writer=self.user
            )
        )
