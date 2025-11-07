from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views.i18n import set_language as django_set_language
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from .models import BookingInquiry, ContactMessage, Drink, GalleryImage, Review, Tent
import random
import string
import requests
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import BlogPost, Combo, MenuItem, Booking

# Thêm vào đầu file (cấu hình Zalo OA)
# ZALO_ACCESS_TOKEN = 'YOUR_ZALO_OA_ACCESS_TOKEN'  
# ZALO_API_URL = 'https://openapi.zalo.me/v2.0/oa/message'

def index(request):
    # Lấy 3 bài viết thường mới nhất
    latest_posts = BlogPost.objects.filter(
        post_type='regular',
        is_published=True
    ).order_by('-published_at')[:3]

    # Lấy 5 đánh giá nổi bật
    featured_reviews = Review.objects.filter(is_featured=True).order_by('-created_at')[:5]

    # LẤY COMBO ĐỂ HIỂN THỊ TRÊN TRANG CHỦ
    combos = Combo.objects.filter(is_active=True)

    context = {
        'latest_posts': latest_posts,
        'featured_reviews': featured_reviews,
        'combos': combos,  # TRUYỀN VÀO TEMPLATE
    }
    return render(request, 'index.html', context)

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
    featured = BlogPost.objects.filter(post_type='featured', is_published=True).first()
    headlines = BlogPost.objects.filter(post_type='headline', is_published=True)[:2]
    regular_posts = BlogPost.objects.filter(post_type='regular', is_published=True).order_by('-published_at')

    paginator = Paginator(regular_posts, 9)
    page = request.GET.get('page')
    try:
        regular_posts_page = paginator.page(page)
    except PageNotAnInteger:
        regular_posts_page = paginator.page(1)
    except EmptyPage:
        regular_posts_page = paginator.page(paginator.num_pages)

    context = {
        'featured': featured,
        'headlines': headlines,
        'regular_posts': regular_posts_page,
    }

    # AJAX → chỉ trả về phần bài thường + pagination
    if request.headers.get('HX-Request'):
        return render(request, 'blogs/_regular_posts.html', context)

    return render(request, 'blogs/blog.html', context)

def blog_details(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    return render(request, 'blogs/blog_details.html', {'post': post})

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

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def contact(request):
    if request.method == 'POST':
        try:
            # LẤY DỮ LIỆU TỪ FORM CŨ
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # LƯU VÀO DB
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            messages.success(request, "Tin nhắn đã được gửi thành công!")
        except Exception as e:
            messages.error(request, "Có lỗi xảy ra, vui lòng thử lại.")

        return redirect('contact')

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


MEAL_TYPE = [
    ('nuong', 'Set Nướng'),
    ('lau', 'Set Lẩu'),
    ('mon_le', 'Món Lẻ'),
    ('combo', 'Combo'),
]

def meal(request):
    combos = Combo.objects.filter(is_active=True)
    menu_items = MenuItem.objects.filter(is_available=True)

    if request.method == 'POST':
        Booking.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            note=request.POST.get('note', ''),
            service='Nhà Hàng'
        )
        messages.success(request, "Gửi yêu cầu đặt bàn thành công!")
        return redirect('meal')

    return render(request, 'service/meal.html', {
        'combos': combos,
        'menu_items': menu_items,
        'MEAL_TYPE': MEAL_TYPE,  # BẮT BUỘC
    })

DRINK_TYPE = [
    ('tra_sua', 'Trà Sữa'),
    ('ca_phe', 'Cà Phê'),
    ('nuoc_ep', 'Nước Ép'),
    ('tra_hoa_qua', 'Trà Hoa Quả'),
    ('nuoc_giai_khat', 'Nước Giải Khát'),
]
def coffee(request):
    combos = Combo.objects.filter(is_active=True)
    drinks = Drink.objects.filter(is_available=True)

    if request.method == 'POST':
        Booking.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            note=request.POST.get('note', ''),
            service='Uống Nước'
        )
        messages.success(request, "Đặt bàn thành công!")
        return redirect('coffee')

    return render(request, 'service/coffee.html', {
        'drinks': drinks,
        'DRINK_TYPE': DRINK_TYPE,
        'combos': combos,
    })

TENT_TYPE = [
    ('overnight', 'Nghỉ Đêm'),
    ('day_use', 'Trong Ngày'),
]

def tent(request):
    tents = Tent.objects.filter(is_available=True)
    combos = Combo.objects.filter(meal_type='combo')  # Nếu có combo lều

    if request.method == 'POST':
        Booking.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            note=request.POST.get('note', ''),
            service='Lều'
        )
        messages.success(request, "Đặt lều thành công!")
        return redirect('tent')

    return render(request, 'service/tent.html', {
        'tents': tents,
        'combos': combos,
        'TENT_TYPE': TENT_TYPE,
    })


def herbal_foot_soak(request):
    combos = Combo.objects.filter(meal_type='combo')  # Nếu có combo riêng

    if request.method == 'POST':
        Booking.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            note=request.POST.get('note', ''),
            service='Ngâm Chân Thảo Mộc',
        )
        messages.success(request, "Đặt lịch ngâm chân thành công!")
        return redirect('herbal_foot_soak')

    return render(request, 'service/herbal_foot_soak.html', {
        'combos': combos,
    })


def art_activity(request):
    combos = Combo.objects.filter(meal_type='combo')  # Nếu có combo nghệ thuật

    if request.method == 'POST':
        Booking.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            note=request.POST.get('note', ''),
            service='Vẽ Tranh & Tô Tượng',
        )
        messages.success(request, "Đặt lịch hoạt động nghệ thuật thành công!")
        return redirect('art_activity')

    return render(request, 'service/art_activity.html', {
        'combos': combos,
    })


def set_language(request):
    from django.views.i18n import set_language as django_set_language
    
    response = django_set_language(request)
    
    # LẤY NEXT TỪ POST HOẶC GET
    next_url = request.POST.get('next') or request.GET.get('next')
    
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        response = redirect(next_url)
    else:
        response = redirect('/')
    
    return response