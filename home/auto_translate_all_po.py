import os
import polib
from googletrans import Translator

def find_po_files(base_dir):
    """Tìm tất cả file .po trong project."""
    po_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.po'):
                po_files.append(os.path.join(root, file))
    return po_files


def translate_po_file(file_path, src_lang='vi', dest_lang='en'):
    print(f"\n🌍 Đang xử lý file: {file_path}")
    po = polib.pofile(file_path)
    translator = Translator()
    translated_count = 0

    for entry in po:
        if not entry.msgstr and entry.msgid.strip():
            try:
                translated = translator.translate(entry.msgid, src=src_lang, dest=dest_lang).text
                entry.msgstr = translated
                translated_count += 1
                print(f"✅ {entry.msgid} → {translated}")
            except Exception as e:
                print(f"⚠️ Lỗi khi dịch '{entry.msgid}': {e}")

    if translated_count > 0:
        po.save(file_path)
        print(f"💾 Đã lưu {translated_count} bản dịch vào: {file_path}")
    else:
        print("ℹ️ Không có chuỗi nào cần dịch.")


def auto_translate_project_locale(base_locale='locale', src_lang='vi', dest_lang='en'):
    """Tự động dịch tất cả file .po trong thư mục locale."""
    base_dir = os.path.abspath(base_locale)
    if not os.path.exists(base_dir):
        print(f"❌ Không tìm thấy thư mục: {base_dir}")
        return

    po_files = find_po_files(base_dir)
    if not po_files:
        print("❌ Không tìm thấy file .po nào trong project.")
        return

    print(f"🚀 Tìm thấy {len(po_files)} file .po cần xử lý.")
    for po_file in po_files:
        translate_po_file(po_file, src_lang, dest_lang)

    print("\n🎉 Hoàn tất dịch toàn bộ project Django!")


if __name__ == "__main__":
    # Dịch từ tiếng Việt (vi) sang tiếng Anh (en)
    auto_translate_project_locale(base_locale='locale', src_lang='vi', dest_lang='en')
