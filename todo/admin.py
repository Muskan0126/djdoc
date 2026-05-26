from django.contrib import admin
from .models import todolist
# Register your models here.
@admin.register(todolist)

class todoadmin(admin.ModelAdmin):

    list_display = ('id' , 'title', 'description', 'completed', 'created_on', 'updated_on','user')
    search_fields  = ('title', 'user__username')
    ordering = ('-created_on',)
    readonly_fields = ('created_on', 'updated_on', 'user')