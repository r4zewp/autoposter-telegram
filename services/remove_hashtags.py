import re

def remove_hashtags(title: str, summary: str) -> tuple:
    """
    Удаляет хештеги из строк title и summary.
    
    Аргументы:
        title (str): строка заголовка, возможно содержащая хештеги.
        summary (str): строка описания, возможно содержащая хештеги.
    
    Возвращает:
        tuple: кортеж из двух строк (очищенный заголовок, очищенное описание).
    """

    # Удаляем хештеги: ищем слова, начинающиеся с #
    clean_title = re.sub(r'#\w+', '', title)
    clean_summary = re.sub(r'#\w+', '', summary)
    
    # Убираем лишние пробелы
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()
    clean_summary = re.sub(r'\s+', ' ', clean_summary).strip()

    clean_title = clean_title.replace('/', '')
    
    return clean_title, clean_summary