from django.contrib import admin
from boards.models import Board, Post
from boards.forms import BoardForm


class PostInline(admin.TabularInline):
    model = Post
    classes = ('grp-collapse grp-closed',)

    def has_add_permission(self, request):
        return False

    exclude = ('content',)
    search_fields = ['subject']


class BoardAdmin(admin.ModelAdmin):
    inlines = [
        PostInline
    ]

    form = BoardForm
    list_display = ('boardname',)


admin.site.register(Board, BoardAdmin)
