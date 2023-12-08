from django.contrib import admin

from ssr_demo.core.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'created', 'content']
    list_filter = [
        ('created', admin.DateFieldListFilter),
        'creator__username',
    ]
    list_select_related = ['creator']

    search_fields = ['creator__username', 'content']

    autocomplete_fields = ['creator']
