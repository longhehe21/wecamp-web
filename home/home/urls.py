from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('tours/', views.tours, name='tours'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery-details/', views.gallery_details, name='gallery_details'),  # Thêm route cho gallery details
    path('blog/', views.blog, name='blog'),
    path('destination-details/', views.destination_details, name='destination_details'),
    path('tour-details/', views.tour_details, name='tour_details'),
    path('booking/', views.booking, name='booking'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faq/', views.faq, name='faq'),
    path('blog-details/', views.blog_details, name='blog_details'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
    path('404/', views.page_not_found, name='404'),
    path('booking-submit/', views.booking_submit, name='booking_submit'),
    path('newsletter-submit/', views.newsletter_submit, name='newsletter_submit'),
]