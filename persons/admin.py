from django.contrib import admin
from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title')
    # list_editable = ('first_name', 'last_name', 'title')


admin.site.register(Person, PersonAdmin)
