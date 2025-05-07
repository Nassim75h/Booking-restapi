from django.contrib import admin
from .models import Property, PropertyImage, Booking, Conversation, Message, WaitListEntry

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'price_per_night', 'address')
    search_fields = ('title', 'address')
    list_filter = ('host',)

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('related_property', 'image')
    list_filter = ('related_property',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'check_in_date', 'check_out_date', 'total_price', 'status')
    list_filter = ('status', 'property', 'guest')
    search_fields = ('property__title', 'guest__username')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'created_at', 'updated_at')
    list_filter = ('property',)
    search_fields = ('messages__content', 'property__title')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'content', 'created_at')
    list_filter = ('conversation', 'sender')
    search_fields = ('content',)

@admin.register(WaitListEntry)
class WaitListEntryAdmin(admin.ModelAdmin):
    list_display = ('related_property', 'guest', 'created_at')
    list_filter = ('related_property', 'guest')
