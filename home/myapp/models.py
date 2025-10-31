from django.db import models
from cloudinary.models import CloudinaryField


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