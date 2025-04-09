import xml.etree.ElementTree as ET
import json

# Пути к файлам
XML_INPUT_PATH = "feed.xml"
XML_OUTPUT_PATH = "updated_feed.xml"
MAPPING_PATH = "url_mapping.json"

# Загружаем mapping
with open(MAPPING_PATH, "r", encoding="utf-8") as f:
    url_map = json.load(f)

# Парсим XML
tree = ET.parse(XML_INPUT_PATH)
root = tree.getroot()

заменено = 0
не_заменено = 0

# Проходим по всем тегам <picture>
for offer in root.findall(".//offer"):
    pic_tag = offer.find("picture")
    if pic_tag is not None:
        original_url = pic_tag.text.strip()

        if original_url in url_map:
            new_url = url_map[original_url]
            print(f"🔁 Заменяем: {original_url} -> {new_url}")
            pic_tag.text = new_url
            заменено += 1
        else:
            print(f"⚠️ Нет замены для: {original_url}")
            не_заменено += 1

# Сохраняем обновлённый XML
tree.write(XML_OUTPUT_PATH, encoding="utf-8", xml_declaration=True)

print(f"\n✅ Ссылки обновлены! Сохранили как: {XML_OUTPUT_PATH}")
print(f"🔢 Всего замен: {заменено}, без замены: {не_заменено}")
