from django.contrib import admin
from inventory.models import Box

class BoxAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'box_category', 'box_size', 'weight', 'get_expiration')

admin.site.register(Box, BoxAdmin)
