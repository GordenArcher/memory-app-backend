from django.contrib import admin
from .models import Memory, ProfilePic

# Register your models here.
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'media', 'description', 'date_created']
    list_filter = ['user', 'description', 'date_created']

    def __str__(self):
        return  self.user


class Profile_PicAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_image',]
    list_filter = ['user']

    def __str__(self):
        return  self.user

admin.site.register(Memory, MemoryAdmin)
admin.site.register(ProfilePic, Profile_PicAdmin)
