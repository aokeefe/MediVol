from django.contrib import admin
from inventory.models import Box

class BoxAdmin(admin.ModelAdmin):
    list_display = ('box_id', 'box_size', 'weight', 'old_contents', 'expiration')
    def get_id(self, obj):
        return '%s'%(obj.box.box_id)
    get_id.short_discription = 'Box Id'

admin.site.register(Box, BoxAdmin)