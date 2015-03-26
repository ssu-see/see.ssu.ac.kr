from django.test import TestCase
from users.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from seeseehome import testdata, msg


class UserManagerTestCase(TestCase):

    def setUp(self):
        pass

    def test_create_user(self):
        self.assertIsNotNone(
            User.objects.create_user(
                username=testdata.users_valid_name,
                email=testdata.users_valid_email,
                password=testdata.users_valid_password,
            )
        )

    def test_check_default_user_perm(self):
        user = User.objects.create_superuser(
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.assertEqual(user.userperm, testdata.perm_user)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.assertTrue(user.is_staff)

    def test_get_user(self):
        user = User.objects.create_user(
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.assertIsNotNone(
            User.objects.get_user(
                id=user.id
            )
        )

# PASSWORD TEST
    def test_user_password_without_alphabet_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_pwd_without_alphabet_char,
        )
    """
#   regex or special characters may be added later
    def test_user_password_without_special_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username = testdata.users_valid_name,
            email = testdata.users_valid_email,
            password = testdata.users_pwd_without_special_char,
        )
    """

    def test_user_password_under_6_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_pwd_under_6_characters,
        )

    def test_user_password_over_255_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_pwd_over_255_characters,
        )


##########
# USERNAME TEST

    def test_user_name_with_special_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username=testdata.users_name_with_special_char,
            email=testdata.users_valid_email,
            password=testdata.users_pwd_without_special_char,
        )

    def test_user_name_argument_under_1_char(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            username=testdata.users_name_under_1_char,
            email=testdata.users_valid_email,
            password=testdata.users_pwd_without_special_char,
        )

    def test_user_name_argument_over_30_char(self):
        self.assertRaises(
            ValidationError,
            User.objects.create_user,
            username=testdata.users_name_over_30_char,
            email=testdata.users_valid_email,
            password=testdata.users_pwd_without_special_char,
        )

##########
# EMAIL TEST
# email test none. because I trust django validate email method

##########
# RETRIEVE
    def test_get_user(self):
        user = User.objects.create_user(
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        user_from_get_method = User.objects.get_user(user.id)
        self.assertEqual(user_from_get_method, user)

##########
# UPDATE
    def test_update_username(self):
        user = User.objects.create_user(
            username=testdata.users_old_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.assertEqual(user.username, testdata.users_old_name)
        User.objects.update_user(user.id, username=testdata.users_new_name)
        updated_user = User.objects.get_user(user.id)
        self.assertEqual(updated_user.username, testdata.users_new_name)

    def test_update_userperm(self):
        user = User.objects.create_user(
            username=testdata.users_old_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.assertEqual(user.userperm, testdata.perm_user)
        User.objects.update_user(user.id, userperm=5)
        updated_user = User.objects.get_user(user.id)
        self.assertEqual(updated_user.userperm, "5")

    def test_update_contact_number(self):
        user = User.objects.create_user(
            username=testdata.users_old_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.assertEqual(user.username, testdata.users_old_name)
        User.objects.update_user(user.id,
                                 contact_number=testdata.users_contact_number)
        updated_user = User.objects.get_user(user.id)
        self.assertEqual(updated_user.contact_number,
                         testdata.users_contact_number)

##########
# DELETE
    def test_update_user_name(self):
        user = User.objects.create_user(
            username=testdata.users_old_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        user = User.objects.get_user(user.id)
        User.objects.delete_user(user.id)
        self.assertEqual(None, User.objects.get_user(user.id))
