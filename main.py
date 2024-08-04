import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from tqdm import tqdm
import time


def split_text(text, max_length):
    words = text.split()
    parts = []
    current_part = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            parts.append(' '.join(current_part))
            current_part = [word]
            current_length = len(word)
        else:
            current_part.append(word)
            current_length += len(word) + 1

    parts.append(' '.join(current_part))
    return parts


def parse_page(url, chapter_number):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Помилка при отриманні сторінки {url}: {e}\n\n"

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    text_to_translate = "\n\n".join([paragraph.get_text() for paragraph in paragraphs])

    translations = [f"Розділ {chapter_number}\n\n"]

    parts = split_text(text_to_translate, 4500)

    for part in parts:
        try:
            translation = GoogleTranslator(source='en', target='uk').translate(part)
            translations.append(f"{translation}\n\n")
        except Exception as e:
            translations.append(f"Помилка перекладу: {e}\n\n")

    return ''.join(translations)


base_url = str(input("Url:"))
chapter_count = int(input("Кількість розділів: "))
updated_file = str(input("Назва вихідного файлу(з розширенням .txt): "))

with open(updated_file, 'w', encoding='utf-8') as file:
    for i in tqdm(range(1, chapter_count + 1), desc="Парсинг сторінок"):
        url = f'{base_url}{i}'
        result = parse_page(url, i)
        file.write(result)
        time.sleep(1)

print(f"Перекладений текст збережено у файл {updated_file}")
