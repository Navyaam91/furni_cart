from django.contrib import admin
from .models import Customer
from .models import Contact 
admin.site.register(Customer)


@admin.register(Contact) # Update this too
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
