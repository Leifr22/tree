from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order',)
    list_filter = ('menu',)
    ordering = ('menu', 'parent', 'order')
    search_fields = ('title', 'named_url', 'url')