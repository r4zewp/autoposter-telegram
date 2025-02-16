from aiogram.utils.markdown import text, hlink

def generate_message(link: str, title: str, summary: str) -> str:
    # Creates a markdown-formatted message
    return text(
        title,
        "",
        summary,
        "",
        hlink("Смотреть на Youtube", link),
        sep="\n"
    )