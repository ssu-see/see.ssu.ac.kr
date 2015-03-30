from django.contrib import admin
from boards.models import Board, Post
from boards.forms import BoardForm


class PostInline(admin.TabularInline):
    model = Post

    def has_add_permission(self, request):
        return False

    list_display = ('subject', 'writer', 'date_posted',)
    exclude = ('writer', 'subject', 'content',)
    search_fields = ['subject']


class BoardAdmin(admin.ModelAdmin):
    inlines = [
        PostInline
    ]

    form = BoardForm
    list_display = ('boardname',)


admin.site.register(Board, BoardAdmin)
