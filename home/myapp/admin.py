from django.contrib import admin
from .models import BookingInquiry
from .models import GalleryImage
# Register your models here.

@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service_display', 'date', 'people', 'created_at', 'is_processed']
    list_filter = ['service', 'date', 'is_processed', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at']
    list_editable = ['is_processed']
    date_hierarchy = 'date'

    def service_display(self, obj):
        return obj.get_service_display()
    service_display.short_description = "Dịch vụ"

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'season_display', 'created_at']
    list_filter = ['season', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['image_preview']  # Thêm preview

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return "No image"
    image_preview.short_description = 'Preview'
    image_preview.allow_tags = True

    def season_display(self, obj):
        return obj.get_season_display()
    season_display.short_description = 'Mùa'
