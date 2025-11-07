import polib
from googletrans import Translator
import os

# Cấu hình file gốc & đích
SRC_FILE = "locale/vi/LC_MESSAGES/django.po"   # file gốc tiếng Việt
DEST_FILE = "locale/en/LC_MESSAGES/django.po"  # file đích tiếng Anh

def translate_po(src_path, dest_path):
    if not os.path.exists(src_path):
        print(f"❌ Không tìm thấy file: {src_path}")
        return

    print("🚀 Đang đọc file .po ...")
    po = polib.pofile(src_path)
    translator = Translator()

    total = len(po)
    translated_count = 0

    for entry in po:
        if not entry.msgstr and entry.msgid.strip():
            try:
                # Dịch chuỗi
                translated = translator.translate(entry.msgid, src='vi', dest='en').text
                entry.msgstr = translated
                translated_count += 1
                print(f"✅ {entry.msgid} → {translated}")
            except Exception as e:
                print(f"⚠️ Lỗi khi dịch: {entry.msgid} ({e})")

    # Lưu file mới
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    po.save(dest_path)
    print(f"\n🎉 Đã dịch xong {translated_count}/{total} chuỗi.")
    print(f"📁 File lưu tại: {dest_path}")

if __name__ == "__main__":
    translate_po(SRC_FILE, DEST_FILE)
