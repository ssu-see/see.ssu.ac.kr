from django.contrib import admin
from linkboard.models import LinkPost
#from boards.forms import BoardForm


class LinkBoardAdmin(admin.ModelAdmin):
    #    form = BoardForm
    list_display = ('description', 'url')

    def has_add_permission(self, request):
        return False

    exclude = ('writer', 'description', 'url')
    search_fields = ['description']

admin.site.register(LinkPost, LinkBoardAdmin)
