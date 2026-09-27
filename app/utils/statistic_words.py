from collections import Counter
from typing import List


def statistic_words(word: List[str], list_w: List[str]) -> str:
    # Filtra eventuali None
    cleaned = [w for w in word if w is not None]

    if not cleaned:
        return ""

    counter = Counter(cleaned)

    # max(list_w) fallisce se counter.get(x) è None → lo gestiamo
    much_present = max(list_w, key=lambda w: counter.get(w, 0))

    return much_present


def statistic_number(value: List[str]) -> str:
    # Converti tutto a numeri e filtra None
    cleaned = []

    for v in value:
        if v is None:
            continue
        try:
            cleaned.append(float(v))
        except ValueError:
            continue

    if not cleaned:
        return ""

    counter = Counter(cleaned)
    result = counter.most_common(1)[0][0]

    # Ritorna come stringa (il tuo modello usa str)
    return str(result.replace(".", ","))

def statistic_number_average(value: List[str]) -> str:
    cleaned = []

    for v in value:
        if v is None:
            continue
        try:
            cleaned.append(float(v))
        except ValueError:
            continue

    if not cleaned:
        return ""

    # Se c'è un solo valore, restituisci comunque il float formattato
    if len(cleaned) == 1:
        return f"{cleaned[0]:.2f}"

    media = sum(cleaned) / len(cleaned)
    return f"{media:.2f}"

def statistic_age_average(value: List[str]) -> str:
    cleaned = []

    for v in value:
        if v is None:
            continue
        try:
            # Salva il valore come float senza arrotondarlo ora
            cleaned.append(float(v))
        except (ValueError, TypeError):
            continue

    if not cleaned:
        return ""

    # Calcola la media numerica
    media = sum(cleaned) / len(cleaned)
    
    # Arrotonda il risultato finale e convertilo in stringa
    return str(round(media))