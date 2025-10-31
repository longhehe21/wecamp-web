from django.db import models
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe  # THÊM DÒNG NÀY
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from autoslug import AutoSlugField


class Tour(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone

class BookingInquiry(models.Model):
    SERVICE_CHOICES = [
        ('meal', 'Dùng bữa'),
        ('coffee', 'Uống cafe'),
        ('herbal_foot_soak', 'Ngâm chân thảo mộc'),
        ('tent_rental', 'Thuê lều'),
        ('art_activity', 'Vẽ tranh & tô tượng'),
        ('other', 'Khác'),
    ]

    name = models.CharField("Họ & Tên", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Số điện thoại", max_length=15)
    date = models.DateField("Ngày đặt")
    people = models.PositiveIntegerField("Số lượng người")
    service = models.CharField("Dịch vụ", max_length=50, choices=SERVICE_CHOICES)
    created_at = models.DateTimeField("Thời gian gửi", default=timezone.now)
    is_processed = models.BooleanField("Đã xử lý", default=False)

    class Meta:
        verbose_name = "Yêu cầu tư vấn"
        verbose_name_plural = "Yêu cầu tư vấn"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_service_display()} - {self.date}"


class GalleryImage(models.Model):
    SEASON_CHOICES = [
        ('spring', 'Xuân'),
        ('summer', 'Hạ'),
        ('autumn', 'Thu'),
        ('winter', 'Đông'),
    ]

    image = CloudinaryField('Ảnh', folder='wecamp/gallery/')  # Thay đổi này
    title = models.CharField('Tiêu đề', max_length=100)
    description = models.TextField('Mô tả', blank=True)
    season = models.CharField('Mùa', max_length=20, choices=SEASON_CHOICES, default='spring')
    created_at = models.DateTimeField('Ngày tải lên', auto_now_add=True)

    class Meta:
        verbose_name = 'Ảnh Thư Viện'
        verbose_name_plural = 'Ảnh Thư Viện'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class BlogPost(models.Model):
    POST_TYPE_CHOICES = [
        ('featured', 'Nổi bật'),
        ('headline', 'Tiêu đề'),
        ('regular', 'Thường'),
    ]
    CATEGORY_CHOICES = [
        ('weather', 'Thời tiết'),
        ('landscape', 'Cảnh quan'),
        ('news', 'Tin tức'),
    ]

    post_type = models.CharField('Loại bài viết', max_length=20, choices=POST_TYPE_CHOICES, default='regular')
    category = models.CharField('Chủ đề', max_length=20, choices=CATEGORY_CHOICES, default='news')
    title = models.CharField('Tiêu đề chính', max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)  # TỰ ĐỘNG
    subtitle = models.CharField('Tiêu đề phụ', max_length=300, blank=True)
    content = RichTextUploadingField('Nội dung')  # CKEDITOR + CLOUDINARY
    image = CloudinaryField('Ảnh bài viết', folder='wecamp/blog/')
    author_name = models.CharField('Tên người đăng', max_length=100, default='Admin')
    author_image = CloudinaryField('Ảnh người đăng', folder='wecamp/authors/', blank=True, null=True)
    published_at = models.DateTimeField('Ngày đăng', auto_now_add=True)
    is_published = models.BooleanField('Đã xuất bản', default=True)

    def __str__(self):
        return self.title

    def get_table_of_contents(self):
        import re
        pattern = r'<h([23])[^>]*>(.*?)</h[23]>'
        matches = re.findall(pattern, self.content, re.IGNORECASE)
        toc = []
        for level, title in matches:
            slug = slugify(title)
            toc.append({'level': int(level), 'title': title, 'slug': slug})
            self.content = re.sub(
                f'<h{level}[^>]*>{re.escape(title)}</h{level}>',
                f'<h{level} id="{slug}">{title}</h{level}>',
                self.content, count=1
            )
        return toc

    def get_content_with_ids(self):
        self.get_table_of_contents()
        return mark_safe(self.content)
    POST_TYPE_CHOICES = [
        ('featured', 'Nổi bật'),
        ('headline', 'Tiêu đề'),
        ('regular', 'Thường'),
    ]

    CATEGORY_CHOICES = [
        ('weather', 'Thời tiết'),
        ('landscape', 'Cảnh quan'),
        ('news', 'Tin tức'),
    ]

    post_type = models.CharField(
        'Loại bài viết', max_length=20, choices=POST_TYPE_CHOICES, default='regular'
    )
    category = models.CharField(
        'Chủ đề', max_length=20, choices=CATEGORY_CHOICES, default='news'
    )
    title = models.CharField('Tiêu đề chính', max_length=200)
    subtitle = models.CharField('Tiêu đề phụ', max_length=300, blank=True)
    content = RichTextUploadingField('Nội dung')
    image = CloudinaryField('Ảnh bài viết', folder='wecamp/blog/')
    author_name = models.CharField('Tên người đăng', max_length=100, default='Admin')
    author_image = CloudinaryField(
        'Ảnh người đăng', folder='wecamp/authors/', blank=True, null=True
    )
    published_at = models.DateTimeField('Ngày đăng', auto_now_add=True)
    is_published = models.BooleanField('Đã xuất bản', default=True)

    class Meta:
        verbose_name = 'Bài Viết'
        verbose_name_plural = 'Bài Viết'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def clean(self):
        # Kiểm tra: chỉ 1 bài Nổi bật
        if self.post_type == 'featured':
            if BlogPost.objects.filter(post_type='featured').exclude(pk=self.pk).exists():
                raise ValidationError("Chỉ được phép có 1 bài viết Nổi bật!")

        # Kiểm tra: chỉ 2 bài Tiêu đề
        if self.post_type == 'headline':
            count = BlogPost.objects.filter(post_type='headline').exclude(pk=self.pk).count()
            if count >= 2:
                raise ValidationError("Chỉ được phép có tối đa 2 bài viết Tiêu đề!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    content = models.TextField('Nội dung', help_text="Dùng &lt;h2&gt;, &lt;h3&gt; để tạo mục lục tự động")

    def get_table_of_contents(self):
        """Trích xuất <h2>, <h3> từ content → sinh TOC"""
        import re
        from django.utils.text import slugify

        # Tìm tất cả heading
        pattern = r'<h([23])[^>]*>(.*?)</h[23]>'
        matches = re.findall(pattern, self.content, re.IGNORECASE)

        toc = []
        for level, title in matches:
            slug = slugify(title)
            toc.append({
                'level': int(level),
                'title': title,
                'slug': slug
            })
            # Thay heading bằng có id
            self.content = re.sub(
                f'<h{level}[^>]*>{re.escape(title)}</h{level}>',
                f'<h{level} id="{slug}">{title}</h{level}>',
                self.content,
                count=1
            )
        return toc

    def get_content_with_ids(self):
        """Trả về content đã thêm id cho heading"""
        # Gọi để sinh id
        self.get_table_of_contents()
        return mark_safe(self.content)