from django.contrib import admin
from .models import Memory

# Register your models here.
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'description', 'date_created']
    list_filter = ['user', 'description', 'date_created']

    def __str__(self):
        return  self.user


admin.site.register(Memory, MemoryAdmin)


