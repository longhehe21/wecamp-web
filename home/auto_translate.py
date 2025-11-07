# auto_translate.py
import polib
from googletrans import Translator
import time
import os

# Đường dẫn file .po tiếng Anh
po_file = 'locale/en/LC_MESSAGES/django.po'

# Kiểm tra file tồn tại
if not os.path.exists(po_file):
    print(f"Không tìm thấy file: {po_file}")
    print("Chạy trước: python manage.py makemessages -l en")
    exit()

# Khởi tạo translator
translator = Translator()

# Mở file .po
po = polib.pofile(po_file)

# Lọc các dòng chưa dịch
untranslated = [e for e in po if not e.msgstr.strip() and e.msgid.strip()]
print(f"Đang dịch {len(untranslated)} dòng từ Tiếng Việt → Tiếng Anh...")

count = 0
for entry in untranslated:
    try:
        # Dịch
        translated = translator.translate(entry.msgid, src='vi', dest='en').text
        entry.msgstr = translated
        print(f"✓ {entry.msgid} → {translated}")
        count += 1
        time.sleep(0.1)  # Tránh bị chặn
    except Exception as e:
        print(f"✗ Lỗi: {entry.msgid} → {e}")
        entry.msgstr = entry.msgid  # Giữ nguyên nếu lỗi

# Đánh dấu fuzzy để bạn kiểm tra lại
for entry in untranslated:
    if 'fuzzy' not in entry.flags:
        entry.flags.append('fuzzy')

# Lưu file
po.save()
print(f"\nHOÀN TẤT! Đã dịch {count} dòng.")
print("Chạy lệnh:")
print("   python manage.py compilemessages")