from django.contrib import admin
from .models import Booking, BookingInquiry, Combo, ContactMessage, Drink, GalleryImage, BlogPost, MenuItem, Review, Tent
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html
# Register your models here.

@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'date', 'people', 'service_display', 'status_badge', 'created_at']
    list_filter = ['status', 'service', 'date', 'created_at']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    list_per_page = 25

    # Hiển thị tên dịch vụ đẹp
    def service_display(self, obj):
        return obj.get_service_display()
    service_display.short_description = 'Dịch vụ'

    # Badge trạng thái
    def status_badge(self, obj):
        colors = {
            'pending': '#dc3545',      # Đỏ
            'processing': '#ffc107',   # Vàng
            'completed': '#28a745',    # Xanh
        }
        color = colors.get(obj.status, '#6c757d')
        text = obj.get_status_display()
        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:12px; font-size:0.8rem; font-weight:600;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Trạng thái'

    # Hành động nhanh
    actions = ['mark_processing', 'mark_completed']

    def mark_processing(self, request, queryset):
        count = queryset.update(status='processing')
        self.message_user(request, f"Đã đánh dấu {count} yêu cầu là Đang xử lý.")
    mark_processing.short_description = "Đánh dấu: Đang xử lý"

    def mark_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f"Đã đánh dấu {count} yêu cầu là Đã xử lý.")
    mark_completed.short_description = "Đánh dấu: Đã xử lý"

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


# Form tùy chỉnh cho CKEditor (để hiển thị đẹp hơn)
class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
        }


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'post_type', 'category', 'is_published', 'published_at')
    list_filter = ('post_type', 'category', 'is_published', 'published_at')
    search_fields = ('title', 'subtitle', 'content')
    
    readonly_fields = ('published_at',)
    fieldsets = (
        ('Thông tin chính', {
            'fields': ('post_type', 'category', 'title', 'subtitle', 'image', 'author_name', 'author_image')
        }),
        ('Nội dung', {
            'fields': ('content',),
        }),
        ('Xuất bản', {
            'fields': ('is_published', 'published_at'),
        }),
    )

    # Hiển thị ảnh preview
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover; border-radius: 8px;" />')
        return "Chưa có ảnh"
    image_tag.short_description = 'Ảnh xem trước'

    def author_image_tag(self, obj):
        if obj.author_image:
            return mark_safe(f'<img src="{obj.author_image.url}" width="50" height="50" style="border-radius: 50%;" />')
        return "—"
    author_image_tag.short_description = 'Ảnh tác giả'

    list_display = ('image_tag', 'title', 'post_type', 'category', 'is_published', 'published_at')
    readonly_fields = ('image_tag', 'author_image_tag', 'published_at')



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'date', 'time', 'service_display', 'status_badge', 'created_at']
    list_filter = ['status', 'service', 'date', 'created_at']
    search_fields = ['name', 'phone', 'note']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    list_per_page = 25

    # Hiển thị tên dịch vụ đẹp
    def service_display(self, obj):
        return obj.get_service_display()
    service_display.short_description = 'Dịch vụ'

    # Badge trạng thái
    def status_badge(self, obj):
        colors = {
            'pending': '#dc3545',      # Đỏ
            'processing': '#ffc107',   # Vàng
            'completed': '#28a745',    # Xanh
        }
        color = colors.get(obj.status, '#6c757d')
        text = obj.get_status_display()
        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:12px; font-size:0.8rem; font-weight:600;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Trạng thái'

    # Hành động nhanh
    actions = ['mark_processing', 'mark_completed']

    def mark_processing(self, request, queryset):
        count = queryset.update(status='processing')
        self.message_user(request, f"Đã đánh dấu {count} đơn là Đang xử lý.")
    mark_processing.short_description = "Đánh dấu: Đang xử lý"

    def mark_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f"Đã đánh dấu {count} đơn là Đã xử lý.")
    mark_completed.short_description = "Đánh dấu: Đã xử lý"

@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_meal_type_display', 'discount_price', 'is_active', 'created_at']
    list_filter = ['meal_type', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_meal_type_display', 'price', 'is_available']
    list_filter = ['meal_type', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available']

# admin.py
@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_drink_type_display', 'price', 'is_available']
    list_filter = ['drink_type', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available']

@admin.register(Tent)
class TentAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_tent_type_display', 'price', 'capacity', 'is_available']
    list_filter = ['tent_type', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'price']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'rating', 'created_at', 'is_featured']
    list_filter = ['service', 'rating', 'is_featured']
    search_fields = ['name', 'content']
    list_editable = ['is_featured']
    readonly_fields = ['created_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_per_page = 25

    # Badge trạng thái
    def status_badge(self, obj):
        colors = {
            'pending': '#dc3545',      # Đỏ - Chưa đọc
            'processing': '#ffc107',   # Vàng - Đang xử lý
            'completed': '#28a745',    # Xanh - Đã đọc
        }
        color = colors.get(obj.status, '#6c757d')
        text = obj.get_status_display()
        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:12px; font-size:0.8rem; font-weight:600;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Trạng thái'

    # Hành động nhanh
    actions = ['mark_processing', 'mark_completed']

    def mark_processing(self, request, queryset):
        count = queryset.update(status='processing')
        self.message_user(request, f"Đã đánh dấu {count} tin nhắn là Đang xử lý.")
    mark_processing.short_description = "Đánh dấu: Đang xử lý"

    def mark_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f"Đã đánh dấu {count} tin nhắn là Đã đọc.")
    mark_completed.short_description = "Đánh dấu: Đã đọc"