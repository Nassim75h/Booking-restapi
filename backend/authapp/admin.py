from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display=[
        'username',
        'is_staff',
        'email'
    ]
    list_filter=['username']
    # autocomplete_fields=['username'] 
    search_fields=['username']

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=[
        'user_id',
        'location',
        'user_name'
    ]
    
    list_select_related=['user']
    def user_name(self,profile):
        return profile.user.username
    autocomplete_fields=['user']
