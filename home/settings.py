"""
Django settings for home project - HOÀN HẢO CHO RENDER.COM (FREE PLAN)
Tác giả: Grok AI | Ngày: 10/11/2025 | Quốc gia: VN
"""

import os
from pathlib import Path
import dj_database_url

# ====================== CẤU HÌNH CƠ BẢN ======================
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Dùng biến môi trường (Render)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')

# DEBUG = False trên Render
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# TỰ ĐỘNG thêm tên miền Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, '.onrender.com']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

# ====================== ỨNG DỤNG ======================
INSTALLED_APPS = [
    'jazzmin',  # PHẢI ĐẶT TRƯỚC admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps của bạn
    'modeltranslation',
    'myapp',
    
    # Cloudinary
    'cloudinary_storage',
    'cloudinary',
    
    # CKEditor
    'ckeditor',
    'ckeditor_uploader',
    
    # Tiện ích
    'mathfilters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'home.urls'

# ====================== TEMPLATES ======================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'home.wsgi.application'

# ====================== DATABASE (TỰ ĐỘNG) ======================
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ====================== PASSWORD VALIDATION ======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ====================== STATIC & MEDIA ======================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary (TỰ ĐỘNG từ Environment Variables)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ====================== EMAIL (GMAIL) ======================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'wecampofficial@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-app-password')
DEFAULT_FROM_EMAIL = 'Wecamp Cafe Retreat <wecampofficial@gmail.com>'

# ====================== CKEDITOR ======================
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
    },
}

# ====================== JAZZMIN ADMIN ======================
JAZZMIN_SETTINGS = {
    "site_title": "Wecamp Cafe Retreat",
    "site_header": "WECAMP ADMIN",
    "site_brand": "Wecamp",
    "site_logo": "admin/img/logo/logo.svg",
    "login_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": "admin/img/favicon.png",
    "welcome_sign": "Chào mừng đến Wecamp Admin",
    "copyright": "Wecamp Cafe Retreat",
    "search_model": ["myapp.Booking", "myapp.ContactMessage"],
    "topmenu_links": [
        {"name": "Trang chủ", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth.user": "fas fa-user",
        "myapp.Booking": "fas fa-calendar-check",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "related_modal_active": True,
    "custom_css": "admin/css/custom-admin.css",
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-success",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-success",
    "theme": "default",
    "dark_mode_theme": "darkly",
}

# ====================== NGÔN NGỮ (VI/EN) ======================
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'vi'
LANGUAGES = [
    ('vi', _('Tiếng Việt')),
    ('en', _('English')),
]
LOCALE_PATHS = [BASE_DIR / 'locale']

USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Ho_Chi_Minh'  # VIỆT NAM

# ====================== DEFAULT ======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'