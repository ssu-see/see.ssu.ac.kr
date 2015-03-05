from django.contrib import admin
from users.models import User
from django.contrib.auth.models import Group
from users.forms import UserForm


admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    form = UserForm
    list_display = ('username', 'email', 'contact_number', 'userperm',
                    'signup_date')

#   admin does not have edit following fields
    exclude = ('password', 'username', 'email',
               'last_login', 'contact_number')
    search_fields = ['username', 'users__email']

admin.site.register(User, UserAdmin)
