from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import BookingInquiry, GalleryImage
import random
import string
import requests
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Thêm vào đầu file (cấu hình Zalo OA)
# ZALO_ACCESS_TOKEN = 'YOUR_ZALO_OA_ACCESS_TOKEN'  
# ZALO_API_URL = 'https://openapi.zalo.me/v2.0/oa/message'

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    return render(request, 'destinations.html')

def tours(request):
    return render(request, 'tours.html')

def gallery(request):
    # Lấy ảnh, sắp xếp CŨ NHẤT TRƯỚC → MỚI NHẤT SAU
    gallery_images = GalleryImage.objects.all().order_by('created_at')  # ĐẢO NGƯỢC
    
    return render(request, 'gallery.html', {
        'gallery_images': gallery_images
    })

def gallery_details(request):
    return render(request, 'gallery-details.html')  # Tạo file gallery-details.html nếu cần

def blog(request):
    return render(request, 'blogs/blog.html')

def destination_details(request):
    return render(request, 'destination-details.html')

def tour_details(request):
    return render(request, 'tour-details.html')

def booking(request):
    return render(request, 'booking.html')

def testimonials(request):
    return render(request, 'testimonials.html')

def faq(request):
    return render(request, 'faq.html')

def blog_details(request):
    return render(request, 'blogs/blog-details.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def contact(request):
    return render(request, 'contact.html')

def page_not_found(request):
    return render(request, '404.html')


# def send_zalo_message(phone, name, service, date, people):
#     """Gửi tin nhắn Zalo OA"""
#     headers = {
#         'access_token': ZALO_ACCESS_TOKEN,
#         'Content-Type': 'application/json',
#     }
#     data = {
#         "recipient": {
#             "phone": phone
#         },
#         "message": {
#             "text": f"Xin chào {name}!\n\nCảm ơn bạn đã đặt chỗ tại Wecamp Cafe Retreat.\n\n📅 Ngày: {date}\n👥 Số người: {people}\n🍲 Dịch vụ: {service}\n\nChúng tôi sẽ gọi xác nhận trong 24h. Chúc bạn ngày vui!\n\nWecamp Team"
#         }
#     }
#     response = requests.post(ZALO_API_URL, headers=headers, json=data)
#     return response.status_code == 200

def booking_submit(request):
    if request.method == 'POST':
        try:
            # 1. Lưu vào DB
            inquiry = BookingInquiry(
                name=request.POST['name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                date=request.POST['date'],
                people=request.POST['people'],
                service=request.POST['service'],
            )
            inquiry.save()

            # 2. Gửi email cho khách (HTML) – DÙNG 5 MẪU RIÊNG
            template_map = {
                'meal': 'emails/email_meal.html',
                'coffee': 'emails/email_coffee.html',
                'tent_rental': 'emails/email_tent.html',
                'herbal_foot_soak': 'emails/email_herbal.html',
                'art_activity': 'emails/email_art.html',
                'other': 'emails/email_default.html',
            }
            template = template_map.get(inquiry.service, 'emails/email_default.html')

            html_message = render_to_string(template, {
                'name': inquiry.name,
                'date': inquiry.date,
                'people': inquiry.people,
                'phone': inquiry.phone,
            })
            plain_message = strip_tags(html_message)

            send_mail(
                subject="Cảm ơn bạn đã liên hệ Wecamp Cafe Retreat!",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.email],
                html_message=html_message,
                fail_silently=False,  # Bắt lỗi ngay
            )

            # 3. Gửi email cho admin
            admin_msg = f"""
            BOOKING MỚI
            Tên: {inquiry.name}
            SĐT: {inquiry.phone}
            Dịch vụ: {inquiry.get_service_display()}
            Ngày: {inquiry.date}
            Người: {inquiry.people}
            """
            send_mail(
                subject=f"[BOOKING] {inquiry.name} - {inquiry.get_service_display()}",
                message=admin_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['wecampofficial@gmail.com'],
                fail_silently=False,
            )

            # # MỚI: Gửi Zalo OA cho khách
            # zalo_success = send_zalo_message(
            #     phone=inquiry.phone,
            #     name=inquiry.name,
            #     service=inquiry.get_service_display(),
            #     date=inquiry.date.strftime('%d/%m/%Y'),
            #     people=inquiry.people
            # )
            # if zalo_success:
            #     print("Gửi Zalo thành công!")

            messages.success(request, "Gửi thành công! Chúng tôi sẽ liên hệ bạn sớm.")
            return redirect('index')

        except Exception as e:
            messages.error(request, "Lỗi hệ thống. Vui lòng thử lại.")
            print("LỖI GỬI EMAIL:", e)

    return redirect('index')

def newsletter_submit(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Thêm logic xử lý newsletter (ví dụ: lưu email hoặc gửi xác nhận)
        return HttpResponse("Your subscription request has been sent. Thank you!")
    return HttpResponse("Invalid request.")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # Thêm logic xử lý email hoặc lưu vào database
        return HttpResponse("Your message has been sent. Thank you!")
    return render(request, 'contact.html')


# thuê lều 
def tent_day(request):
    return render(request, 'tent_services/tent_day.html')  # Tạo file này sau

def tent_night(request):
    return render(request, 'tent_services/tent_night.html')  # Tạo file này sau