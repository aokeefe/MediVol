from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    search_fields = ['question']
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'

# admin.site.register(Poll, PollAdmin)