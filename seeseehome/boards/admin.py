from django.contrib import admin
from boards.models import *
from boards.forms import BoardForm


class BoardAdmin(admin.ModelAdmin):
    form = BoardForm
    list_display = ('boardname',)


class PostAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    list_display = ('subject', 'writer', 'date_posted',)
    exclude = ('writer', 'subject', 'content',)
    search_fields = ['subject']

admin.site.register(Board, BoardAdmin)
admin.site.register(Post, PostAdmin)
