import os
import cloudinary
import cloudinary.uploader
import json

# Папка с JPG-картинками
CONVERTED_FOLDER = "converted_jpg"

# Cloudinary конфигурация (вставь свои значения)
cloudinary.config(
    cloud_name="dezpcr3vd",
    api_key="339112911764535",
    api_secret="oh7nCDmO2xK51u8N-xGILYYHrKg",
    secure=True
)

# Словарь для сохранения соответствия оригинальных webp/пнг URL → новый Cloudinary JPG URL
url_mapping = {}

# Получим список оригинальных webp-файлов
original_folder = "downloaded_webp"
original_files = {
    os.path.splitext(f)[0]: f for f in os.listdir(original_folder)
    if f.lower().endswith((".webp", ".png", ".jpeg", ".jpg"))
}

# Загрузка в Cloudinary
for filename in os.listdir(CONVERTED_FOLDER):
    if filename.lower().endswith(".jpg"):
        local_path = os.path.join(CONVERTED_FOLDER, filename)
        public_id = os.path.splitext(filename)[0]  # Без .jpg

        try:
            response = cloudinary.uploader.upload(
                local_path,
                public_id=public_id,  # Сохраняем оригинальное имя
                folder="tilda_uploads",  # Можно изменить путь в Cloudinary
                overwrite=True,
                resource_type="image"
            )
            cloudinary_url = response['secure_url']
            original_file = original_files.get(public_id)

            if original_file:
                original_url = f"https://acon.ru/storage/catalog/products/{original_file}"
                url_mapping[original_url] = cloudinary_url
                print(f"✅ {original_url} → {cloudinary_url}")
            else:
                print(f"⚠️ Не найден оригинал для {public_id}")

        except Exception as e:
            print(f"❌ Ошибка загрузки {filename}: {e}")

# Сохраняем mapping для следующего шага
with open("url_mapping.json", "w", encoding="utf-8") as f:
    json.dump(url_mapping, f, ensure_ascii=False, indent=2)

print("🎉 Все изображения загружены в Cloudinary и соответствие сохранено в url_mapping.json")
