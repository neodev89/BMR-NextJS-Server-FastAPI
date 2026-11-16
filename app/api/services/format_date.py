from datetime import datetime


def format_italian_date(
    value: str | datetime | None, format_str: str = "%d/%m/%Y"
) -> str:
    """
    Converte una stringa ISO o un oggetto datetime nel formato data italiano (es. 15/11/2026).
    Se il valore è vuoto o non valido, restituisce una stringa vuota o un fallback.
    """
    if not value:
        return ""

    # Se è già una stringa ISO, la converte in oggetto datetime
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value)
        except ValueError:
            # Se la stringa non è in formato ISO valido, restituisce la stringa originale o gestisce l'errore
            return value
    elif isinstance(value, datetime):
        dt = value
    else:
        return str(value)

    # Restituisce la data formattata
    return dt.strftime(format_str)
