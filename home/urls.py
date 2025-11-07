# home/urls.py
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# URL KHÔNG CẦN DỊCH (admin, i18n, static)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# TẤT CẢ URL CỦA BẠN → ĐƯỢC DỊCH
urlpatterns += i18n_patterns(
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery-details/', views.gallery_details, name='gallery_details'),
    path('blogs/blog/', views.blog, name='blog'),
    path('tour-details/', views.tour_details, name='tour_details'),
    path('booking/', views.booking, name='booking'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faq/', views.faq, name='faq'),
    path('blogs/blog/<int:pk>/', views.blog_details, name='blog_details'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
    path('404/', views.page_not_found, name='404'),
    path('booking-submit/', views.booking_submit, name='booking_submit'),   
    path('newsletter-submit/', views.newsletter_submit, name='newsletter_submit'),
    path('service/tent/', views.tent, name='tent'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('service/meal/', views.meal, name='meal'),
    path('service/coffee/', views.coffee, name='coffee'),
    path('service/herbal-foot-soak/', views.herbal_foot_soak, name='herbal_foot_soak'),
    path('service/art-activity/', views.art_activity, name='art_activity'),
    
    # set_language KHÔNG CẦN TRONG i18n_patterns
    # → Django tự thêm vào
    prefix_default_language=False  # KHÔNG thêm /vi/ vào URL tiếng Việt
)

# MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



