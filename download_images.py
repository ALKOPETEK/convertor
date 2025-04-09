import os
import requests
import xml.etree.ElementTree as ET

# Путь к XML-файлу с фидом
XML_FEED_PATH = "feed.xml"

# Папка для скачанных изображений
DOWNLOAD_FOLDER = "downloaded_webp"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Парсим XML
tree = ET.parse(XML_FEED_PATH)
root = tree.getroot()

# Пространство имен (если нужно)
namespace = {"y": "yml_catalog"}

# Собираем все ссылки из <picture>
pictures = root.findall(".//picture")

# Скачиваем каждое изображение
for pic in pictures:
    url = pic.text
    filename = os.path.basename(url)
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    print(f"Скачиваю: {url} -> {filepath}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")

print("✅ Все изображения скачаны.")
