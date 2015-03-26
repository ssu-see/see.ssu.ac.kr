from django import forms
from seeseehome import msg
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):

    def clean_username(self):
        try:
            User.objects.validate_username(self.cleaned_data["username"])
        except ValueError:
            raise forms.ValidationError(msg.users_name_must_be_set)
        except ValidationError:
            raise forms.ValidationError(
                msg.users_name_at_most_30 + " OR  " +
                msg.users_invalid_name
            )
        return self.cleaned_data["username"]

    """
    Admin cannot create user in admin page. So I stopped to create the
    validator for add user in admin page
    """
