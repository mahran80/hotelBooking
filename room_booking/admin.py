from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Room, OccupiedDate, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ['image', 'caption']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'pricePerNight', 'currency', 'maxOccupancy']
    list_filter = ['type', 'currency', 'maxOccupancy']
    search_fields = ['name', 'description']
    inlines = [RoomImageInline]
    list_editable = ['pricePerNight', 'maxOccupancy']
    fieldsets = (
        (None, {
            'fields': ('name', 'type')
        }),
        (_('Pricing'), {
            'fields': ('pricePerNight', 'currency')
        }),
        (_('Details'), {
            'fields': ('maxOccupancy', 'description')
        }),
    )

@admin.register(OccupiedDate)
class OccupiedDateAdmin(admin.ModelAdmin):
    list_display = ['date', 'room', 'user']
    list_filter = ['date', 'room', 'user']
    search_fields = ['room__name', 'user__username']
    date_hierarchy = 'date'
    raw_id_fields = ['user']

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room', 'caption', 'image_preview']
    list_filter = ['room']
    search_fields = ['room__name', 'caption']
    raw_id_fields = ['room']

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px;"/>'
        return _('No Image')
    image_preview.allow_tags = True
    image_preview.short_description = _('Preview')
