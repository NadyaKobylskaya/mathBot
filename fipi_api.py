import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

# 🔕 Отключаем предупреждения о небезопасных сертификатах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 🔧 Константы
BASE_URL = "https://oge.fipi.ru/bank/"
START_URL = urljoin(BASE_URL, "index.php?proj=DE0E276E497AB3784C3FC4CC20248DC0")
QUESTIONS_URL = urljoin(BASE_URL, "questions.php")

OUTPUT_DIR = 'oge_tasks'
TEXTS_DIR = os.path.join(OUTPUT_DIR, 'texts')
IMAGES_DIR = os.path.join(OUTPUT_DIR, 'images')

# 🗂 Создание директорий
os.makedirs(TEXTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# 🔄 Сессия
session = requests.Session()

def save_image(img_url, task_id):
    try:
        response = session.get(img_url, verify=False)
        with open(os.path.join(IMAGES_DIR, f"{task_id}.jpg"), 'wb') as f:
            f.write(response.content)
        print(f"[+] Сохранено изображение: {task_id}.jpg")
    except Exception as e:
        print(f"[!] Ошибка при загрузке изображения {img_url}: {e}")

def parse_task(task_html, task_id):
    text = task_html.get_text(separator="\n", strip=True)
    with open(os.path.join(TEXTS_DIR, f"{task_id}.txt"), 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[+] Сохранено задание: {task_id}.txt")

    img = task_html.find('img')
    if img and img.get('src'):
        img_url = urljoin(BASE_URL, img['src'])
        save_image(img_url, task_id)

def get_csrf_tokens():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://oge.fipi.ru/"
    }
    resp = session.get(START_URL, headers=headers, verify=False)
    resp.encoding = 'windows-1251'
    html = resp.text

    # 💡 Поиск токенов через регулярные выражения
    name_match = re.search(r"<meta\s+name=['\"]csrf-token-name['\"]\s+content=['\"]([^'\"]+)['\"]", html)
    value_match = re.search(r"<meta\s+name=['\"]csrf-token-value['\"]\s+content=['\"]([^'\"]+)['\"]", html)

    if name_match and value_match:
        return name_match.group(1), value_match.group(1)
    raise Exception("❌ Не удалось найти CSRF-токены")

def fetch_tasks(page_offset, csrf_name, csrf_value):
    data = {
        csrf_name: csrf_value,
        "search": "1",
        "pagesize": "10",
        "proj": "DE0E276E497AB3784C3FC4CC20248DC0",
        "qpos": str(page_offset)
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": START_URL,
    }

    try:
        response = session.post(QUESTIONS_URL, data=data, headers=headers, verify=False)
        response.encoding = 'windows-1251'
        soup = BeautifulSoup(response.text, 'html.parser')
        tasks = soup.find_all('div', class_='prob_row')

        if not tasks:
            print(f"[!] Задания не найдены на смещении {page_offset}")
            return

        print(f"[+] Найдено заданий: {len(tasks)} на смещении {page_offset}")
        for i, task in enumerate(tasks, 1):
            task_id = f"page{page_offset}_task{i}"
            parse_task(task, task_id)

    except Exception as e:
        print(f"[!] Ошибка при загрузке заданий: {e}")

def main():
    print("[.] Получение CSRF-токенов...")
    csrf_name, csrf_value = get_csrf_tokens()

    for offset in range(0, 30, 10):  # 🔁 Проверь сначала 3 страницы
        print(f"\n[.] Обработка смещения {offset}...")
        fetch_tasks(offset, csrf_name, csrf_value)
