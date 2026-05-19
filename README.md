markdown
# VK Bot Parser

Бот для мониторинга постов и комментариев VK, парсинга товаров (название, артикул, цена) и сохранения в Google Sheets.

## Возможности
- Отслеживание новых постов в группе VK
- Парсинг текста поста (заголовок, артикул, цена)
- Сохранение в SQLite и синхронизация с Google Sheets
- Мониторинг комментариев к постам

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/smir0181-code/Vk-bot-parser.git
   cd vk-bot-parser
Создайте виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Установите зависимости:

bash
pip install -r requirements.txt
Настройте config.py по примеру config.py.example.

Настройте Google Sheets API (инструкция в docs/).

Запуск
bash
python bot.py
Лицензия
MIT

text

### 6. Создайте `requirements.txt`

Зафиксируйте зависимости:
```bash
pip freeze > requirements.txt