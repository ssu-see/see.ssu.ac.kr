#-*- coding: utf-8 -*-
# default encoding type : utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
from django.db import OperationalError
from seeseehome import msg


class UserManager(BaseUserManager):
    # CREATE

    def _create_user(self, username, email, password,
                     is_admin=False, **extra_fields):
        """
        It Creates and saves a User with the given username, email and
        password, and values in extra fields.
        """
        self.validate_username(username)
        email = self.normalize_email(email)
        validate_email(email)
        self.validate_password(password)

        user = self.model(username=username, email=email, is_admin=is_admin)

        if 'contact_number' in extra_fields:
            contact_number = extra_fields['contact_number']
            self.validate_contact_number(contact_number)
            user.contact_number = contact_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password,
                                 is_admin=True, **extra_fields)
        return user

    def validate_username(self, username):
        if not username:
            raise ValueError(msg.users_name_must_be_set)
        elif len(username) > 30:
            raise ValidationError(msg.users_name_at_most_30)
        if bool(re.match('^[가-힣a-zA-Z0-9_-]+$', str(username))) is False:
            raise ValidationError(msg.users_invalid_name)

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError(
                msg.users_pwd_at_least_6,
            )
        elif len(password) > 255:
            raise ValidationError(
                msg.users_pwd_at_most_255,
            )

        if bool(re.search('[0-9]', password)) is False:
            raise ValidationError(msg.users_pwd_no_numeric_char)

        if bool(re.search('[a-zA-Z]', password)) is False:
            raise ValidationError(msg.users_pwd_no_alphabet_char)

        """
#       regex for special characters may be added later
        if bool(re.search(
                   '[~`$&+,:;=?@#|\'\"<>.^*()%!-[]{},./?]',
                   password)) is False:
            raise ValidationError(msg.users_pwd_no_special_char)
        """

    def validate_userperm(self, userperm):
        if (userperm == 1) or (userperm == 2) or (userperm == 3) or \
                (userperm == 4) or (userperm == 5):
            pass
        else:
            raise ValidationError(
                msg.users_userperm_validation_error,
            )

    def validate_contact_number(self, contact_number):

        if len(contact_number) < 8:
            raise ValidationError(
                "User contact_number length should be at least 8",
            )
        elif len(contact_number) > 30:
            raise ValidationError(
                "User contact_number max length 30",
            )

        if bool(re.match('^[0-9-]+$', contact_number)) is False:
            raise ValidationError(
                "contact number should be number, and '-' is only available")

##########
# RETRIEVE
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
##########
# UPDATE

    def update_user(self, id, **extra_fields):
        user = User.objects.get_user(id)
        if 'username' in extra_fields:
            self.validate_username(extra_fields['username'])
            try:
                User.objects.get(username=extra_fields['username'])
            except ObjectDoesNotExist:
                user.username = extra_fields['username']
            else:
                raise ValidationError(msg.users_username_already_exist)

        if 'email' in extra_fields:
            validate_email(extra_fields['email'])
            try:
                User.objects.get(email=extra_fields['email'])
            except ObjectDoesNotExist:
                user.email = extra_fields['email']
            else:
                raise ValidationError(msg.users_email_already_exist)

        if 'contact_number' in extra_fields:
            contact_number = extra_fields['contact_number']
            self.validate_contact_number(contact_number)
            user.contact_number = contact_number

        if 'userperm' in extra_fields:
            self.validate_userperm(extra_fields['userperm'])
            user.userperm = extra_fields['userperm']

        if 'is_admin' in extra_fields:
            is_admin = extra_fields['is_admin']
            if isinstance(is_admin, bool):
                user.is_admin = is_admin
            else:
                raise ValidationError(
                    msg.users_update_is_admin_must_be_bool_type)

        user.save(using=self._db)

##########
# DELETE
    def delete_user(self, id):
        user = self.get(id=id)
        user.delete()


class User(AbstractBaseUser):
    objects = UserManager()

#   For custom user model, username field must be set
    USERNAME_FIELD = 'username'

#   When create superuser using cli, required field data is used.
    REQUIRED_FIELDS = ['email']

    username = models.CharField(
        help_text="User name",
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        help_text="User email",
        max_length=64,
        unique=True,
    )

    contact_number = models.CharField(
        help_text="User Contact Number",
        max_length=30,
    )

    is_active = models.BooleanField(
        help_text="Is active user?",
        default=True
    )

    """
    If you want your custom User model to also work with Admin,
    your User model must define some additional attributes and methods.
    """
    is_admin = models.BooleanField(
        help_text=('Is the user can access & edit admin page?'),
        default=False,
    )

    """
    Read/Write permission of Board model is described to multiple select field.
    That is constructed by Char field.
    """
    userperm = models.CharField(
        help_text='Available User Permission [ User, Member, '
        'Core member, Graduate, President ]',
        choices=(('1', 'User',), ('2', 'Member'),
                 ('3', 'Core member'), ('4', 'Graduate'),
                 ('5', 'President')),
        default='1',
        max_length = 1,
    )

    signup_date = models.DateTimeField(
        blank=True,
        null=True,
        auto_now_add=True
    )

    def deactivate(self):
        self.is_active = False
        self.save()
        return self.is_active

    def activate(self):
        self.is_active = True
        self.save()
        return self.is_active

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_superuser(self):
        return is_admin
    """
    The following two method 'has_perm', 'has_module_perms' is important to
    access built-in admin site.
    """

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

#   for showing user name instead of object itself
    def __unicode__(self):
        return 'User name: ' + self.username
