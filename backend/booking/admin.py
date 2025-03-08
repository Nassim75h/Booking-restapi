from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=['property','guest','check_in_date','check_out_date']


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display=['title','city','is_available','max_guests','user_name']
    list_filter=['city','title','host']

    #search_fields[]
    #autocomplete_fields=[]
    
    list_select_related=['host']
    def user_name(self,profile):
        return profile.host.username

@admin.register(models.WaitListEntry)
class WishlistAdmin(admin.ModelAdmin):
    list_display=["guest","confirmed"]
    list_select_related=['related_property']


@admin.register(models.PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display=['property','owner','property_address']
    list_select_related=['related_property'] 

    def property(self,images):
        return images.related_property.title

    def property_address(self,property_address):
        return property_address.related_property.address

    def owner(self,property_owner):
        return property_owner.related_property.host



class ParticipantInline(admin.TabularInline):
    model = models.Conversation.participants.through
    extra = 0
    can_delete=False


@admin.register(models.Conversation)
class ConverstationAdmin(admin.ModelAdmin):
    list_display=['id','participant_names','created_at']
    search_fields=['participant_names']
    inlines=[ParticipantInline]


    
@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=['conversation','sender','time_stamp','participants','content']

    def participants(self,obj):
        return ", ".join([user.username for user in obj.conversation.participants.all()])
    participants.short_description="Participants"
    
