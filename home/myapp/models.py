# myapp/models.py
from django.db import models
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from ckeditor_uploader.fields import RichTextUploadingField
from autoslug import AutoSlugField
import re

# ==================== CÁC CHOICES ====================
SERVICE_CHOICES = [
    ('meal', 'Nhà Hàng'),
    ('coffee', 'Đồ Uống'),
    ('herbal_foot_soak', 'Ngâm chân thảo mộc'),
    ('tent_rental', 'Nghỉ Dưỡng'),
    ('art_activity', 'Vẽ tranh & tô tượng'),
    ('campfire', 'Lửa trại & nướng kẹo'),
    ('other', 'Khác'),
]

TENT_TYPE = [('overnight', 'Nghỉ Đêm'), ('day_use', 'Trong Ngày')]
MEAL_TYPE = [('nuong', 'Set Nướng'), ('lau', 'Set Lẩu'), ('mon_le', 'Món Lẻ'), ('combo', 'Combo')]
DRINK_TYPE = [('tra_sua', 'Trà Sữa'), ('ca_phe', 'Cà Phê'), ('nuoc_ep', 'Nước Ép'), ('tra_hoa_qua', 'Trà Hoa Quả'), ('nuoc_giai_khat', 'Nước Giải Khát')]
SEASON_CHOICES = [('spring', 'Xuân'), ('summer', 'Hạ'), ('autumn', 'Thu'), ('winter', 'Đông')]

STATUS_CHOICES = [('pending', 'Chưa xử lý'), ('processing', 'Đang xử lý'), ('completed', 'Đã xử lý')]

POST_TYPE_CHOICES = [('featured', 'Nổi bật'), ('headline', 'Tiêu đề'), ('regular', 'Thường')]
CATEGORY_CHOICES = [('weather', 'Thời tiết'), ('landscape', 'Cảnh quan'), ('news', 'Tin tức')]

# ==================== MODELS ====================

class BookingInquiry(models.Model):
    name = models.CharField("Họ & Tên", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Số điện thoại", max_length=15)
    date = models.DateField("Ngày đặt")
    people = models.PositiveIntegerField("Số lượng người")
    service = models.CharField("Dịch vụ", max_length=50, choices=SERVICE_CHOICES)
    created_at = models.DateTimeField("Thời gian gửi", default=timezone.now)
    status = models.CharField("Trạng thái", max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = "Yêu cầu tư vấn"
        verbose_name_plural = "Yêu cầu tư vấn"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_service_display()} - {self.date}"


class GalleryImage(models.Model):
    image = CloudinaryField('Ảnh', folder='wecamp/gallery/')
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
    post_type = models.CharField('Loại bài viết', max_length=20, choices=POST_TYPE_CHOICES, default='regular')
    category = models.CharField('Chủ đề', max_length=20, choices=CATEGORY_CHOICES, default='news')
    title = models.CharField('Tiêu đề chính', max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    subtitle = models.CharField('Tiêu đề phụ', max_length=300, blank=True)
    content = RichTextUploadingField('Nội dung')
    image = CloudinaryField('Ảnh bài viết', folder='wecamp/blog/')
    author_name = models.CharField('Tên người đăng', max_length=100, default='Admin')
    author_image = CloudinaryField('Ảnh người đăng', folder='wecamp/authors/', blank=True, null=True)
    published_at = models.DateTimeField('Ngày đăng', auto_now_add=True)
    is_published = models.BooleanField('Đã xuất bản', default=True)

    class Meta:
        verbose_name = 'Bài Viết'
        verbose_name_plural = 'Bài Viết'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def clean(self):
        if self.post_type == 'featured' and BlogPost.objects.filter(post_type='featured').exclude(pk=self.pk).exists():
            raise ValidationError("Chỉ được phép có 1 bài viết Nổi bật!")
        if self.post_type == 'headline' and BlogPost.objects.filter(post_type='headline').exclude(pk=self.pk).count() >= 2:
            raise ValidationError("Chỉ được phép có tối đa 2 bài viết Tiêu đề!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_table_of_contents(self):
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


class Combo(models.Model):
    title = models.CharField("Tên combo", max_length=100)
    description = models.TextField("Mô tả ngắn")
    details = models.TextField("Chi tiết món", blank=True)
    original_price = models.DecimalField("Giá gốc", max_digits=10, decimal_places=0)
    discount_price = models.DecimalField("Giá ưu đãi", max_digits=10, decimal_places=0)
    image = models.ImageField("Hình ảnh", upload_to='wecamp/combos/', blank=True, null=True)
    meal_type = models.CharField("Loại combo", max_length=20, choices=MEAL_TYPE, default='mon_le')
    is_active = models.BooleanField("Hiển thị", default=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

    class Meta:
        verbose_name = "Combo"
        verbose_name_plural = "Danh Sách Combo"
        ordering = ['meal_type', '-created_at']

    def __str__(self):
        return f"[{self.get_meal_type_display()}] {self.title}"


class MenuItem(models.Model):
    name = models.CharField("Tên món", max_length=100)
    description = models.TextField("Mô tả")
    price = models.DecimalField("Giá", max_digits=10, decimal_places=0)
    image = models.ImageField("Hình ảnh", upload_to='menu/', blank=True, null=True)
    meal_type = models.CharField("Loại món", max_length=20, choices=MEAL_TYPE, default='mon_le')
    is_available = models.BooleanField("Còn phục vụ", default=True)
    created_at = models.DateTimeField("Ngày thêm", auto_now_add=True)

    class Meta:
        verbose_name = "Món Ăn"
        verbose_name_plural = "Menu"
        ordering = ['meal_type', 'name']

    def __str__(self):
        return f"[{self.get_meal_type_display()}] {self.name}"


class Booking(models.Model):
    name = models.CharField("Họ tên", max_length=100)
    phone = models.CharField("SĐT", max_length=15)
    date = models.DateField("Ngày")
    time = models.CharField("Giờ", max_length=5, help_text="VD: 13:30")
    note = models.TextField("Ghi chú", blank=True, default='')
    service = models.CharField("Dịch vụ", max_length=50, choices=SERVICE_CHOICES, default="meal")
    created_at = models.DateTimeField("Thời gian đặt", auto_now_add=True)
    status = models.CharField("Trạng thái", max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = "Đặt bàn / Dịch vụ"
        verbose_name_plural = "Đặt bàn / Dịch vụ"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_service_display()} - {self.date} {self.time}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and settings.EMAIL_HOST_USER:
            subject = f"ĐẶT {self.get_service_display().upper()} MỚI"
            message = f"""
WECAMP - THÔNG BÁO ĐƠN ĐẶT MỚI

Khách hàng: {self.name}
SĐT: {self.phone}
Ngày: {self.date.strftime('%d/%m/%Y')}
Giờ: {self.time}
Dịch vụ: {self.get_service_display()}

Ghi chú:
{self.note or 'Không có'}

---
Vui lòng liên hệ xác nhận sớm!
            """.strip()
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            except Exception as e:
                print(f"[Lỗi gửi email] {e}")


class Drink(models.Model):
    name = models.CharField("Tên đồ uống", max_length=100)
    description = models.TextField("Mô tả")
    price = models.DecimalField("Giá", max_digits=10, decimal_places=0)
    image = models.ImageField("Hình ảnh", upload_to='drinks/', blank=True, null=True)
    drink_type = models.CharField("Loại", max_length=20, choices=DRINK_TYPE, default='coffee')
    is_available = models.BooleanField("Còn phục vụ", default=True)
    created_at = models.DateTimeField("Ngày thêm", auto_now_add=True)

    class Meta:
        verbose_name = "Đồ Uống"
        verbose_name_plural = "Menu Đồ Uống"
        ordering = ['drink_type', 'name']

    def __str__(self):
        return f"[{self.get_drink_type_display()}] {self.name}"


class Tent(models.Model):
    name = models.CharField("Tên lều", max_length=100)
    description = models.TextField("Mô tả")
    price = models.DecimalField("Giá", max_digits=10, decimal_places=0)
    image = models.ImageField("Hình ảnh", upload_to='tents/', blank=True, null=True)
    tent_type = models.CharField("Loại lều", max_length=20, choices=TENT_TYPE, default='day_use')
    capacity = models.PositiveIntegerField("Sức chứa", default=2)
    is_available = models.BooleanField("Còn trống", default=True)
    created_at = models.DateTimeField("Ngày thêm", auto_now_add=True)

    class Meta:
        verbose_name = "Lều"
        verbose_name_plural = "Nghỉ Dưỡng"
        ordering = ['tent_type', 'name']

    def __str__(self):
        return f"{self.get_tent_type_display()} - {self.name}"


class Review(models.Model):
    name = models.CharField("Tên khách hàng", max_length=100)
    photo = models.ImageField("Ảnh khách hàng", upload_to='reviews/', blank=True, null=True)
    service = models.CharField("Dịch vụ trải nghiệm", max_length=50, choices=SERVICE_CHOICES)
    content = models.TextField("Nội dung đánh giá")
    rating = models.IntegerField("Điểm đánh giá", validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    created_at = models.DateTimeField("Ngày đánh giá", auto_now_add=True)
    is_featured = models.BooleanField("Hiển thị trên trang chủ", default=False)

    class Meta:
        verbose_name = "Đánh giá khách hàng"
        verbose_name_plural = "Đánh giá khách hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_service_display()}"

    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Chủ đề")
    message = models.TextField(verbose_name="Nội dung")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Thời gian gửi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")

    class Meta:
        verbose_name = "Tin nhắn liên hệ"
        verbose_name_plural = "Tin nhắn liên hệ"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"