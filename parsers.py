import re

def parse_post_text(text):
    """Извлекает наименование, артикул, цену из текста поста."""
    # Примеры: "Товар:" , "Артикул:" , "Цена:"
    name_match = re.search(r'(?:Товар|Наименование)[:\s]+(.+)', text, re.IGNORECASE)
    article_match = re.search(r'Артикул[:\s]+(\S+)', text, re.IGNORECASE)
    price_match = re.search(r'Цена[:\s]+(.+)', text, re.IGNORECASE)
    title = name_match.group(1).strip() if name_match else ''
    article = article_match.group(1).strip() if article_match else ''
    price = price_match.group(1).strip() if price_match else ''
    return title, article, price