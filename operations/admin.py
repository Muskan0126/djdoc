from django.contrib import admin
from operations.models import CustomUser

# admin.site.register(CustomUser)
@admin.register(CustomUser)
class CustomUseradmin(admin.ModelAdmin):
    list_display = ('username', 'email','date_joined')
    ordering = ('-date_joined',)
    search_fields = ('username', 'email')
