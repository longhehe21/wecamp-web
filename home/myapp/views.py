from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    return render(request, 'destinations.html')

def tours(request):
    return render(request, 'tours.html')

def gallery(request):
    return render(request, 'gallery.html')

def gallery_details(request):
    return render(request, 'gallery-details.html')  # Tạo file gallery-details.html nếu cần

def blog(request):
    return render(request, 'blog.html')

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
    return render(request, 'blog-details.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def contact(request):
    return render(request, 'contact.html')

def page_not_found(request):
    return render(request, '404.html')

def booking_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        people = request.POST.get('people')
        service = request.POST.get('service')

        # Xử lý dữ liệu: lưu vào DB, gửi email, v.v.
        # Ví dụ: in ra console
        print(f"Booking: {name}, {email}, {phone}, {date}, {people} người, Dịch vụ: {service}")

        messages.success(request, f"Cảm ơn {name}! Chúng tôi sẽ liên hệ bạn sớm nhất!")
        return redirect('index')  # Quay lại trang chủ

    return HttpResponse("Invalid request", status=400)

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