from PIL import Image
import os

# Папка с исходными изображениями
INPUT_FOLDER = "downloaded_webp"
# Папка для JPG-версий
OUTPUT_FOLDER = "converted_jpg"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Поддерживаемые форматы
SUPPORTED_FORMATS = (".webp", ".png", ".jpeg", ".jpg")

for filename in os.listdir(INPUT_FOLDER):
    file_lower = filename.lower()
    if file_lower.endswith(SUPPORTED_FORMATS):
        input_path = os.path.join(INPUT_FOLDER, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_FOLDER, base_name + ".jpg")

        try:
            with Image.open(input_path) as img:
                # Обработка прозрачности
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    background = Image.new("RGB", img.size, (255, 255, 255))  # Белый фон
                    background.paste(img, mask=img.convert("RGBA").split()[-1])
                    background.save(output_path, "JPEG", quality=95)
                else:
                    rgb_img = img.convert("RGB")
                    rgb_img.save(output_path, "JPEG", quality=95)

            print(f"✅ Конвертировано: {filename} -> {base_name}.jpg")

        except Exception as e:
            print(f"❌ Ошибка при обработке {filename}: {e}")

print("🎉 Все изображения успешно конвертированы в JPG.")
