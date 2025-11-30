def clean_cell(text: str) -> str:
    """Убирает переносы строк и лишние пробелы."""
    if text is None:
        return ""
    return str(text).replace("\n", " ").replace("\r", " ").strip()