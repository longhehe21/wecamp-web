from django.contrib import admin
from .models import BookingInquiry, GalleryImage, BlogPost
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe
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
