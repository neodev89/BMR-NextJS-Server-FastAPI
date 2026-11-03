import json
from pathlib import Path
from typing import Any, Dict
from fastapi import HTTPException, status


# Percorso del file JSON
DATA_FILE = Path("data/foods.json")


def load_json_data() -> Dict[str, Any]:
    """Utility per leggere il file JSON in sicurezza."""
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore nel formato del file JSON locale.",
        )


def save_json_data(data: Dict[str, Any]) -> None:
    """Utility per scrivere dati su file JSON."""
    # Assicurati che la cartella esista
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# # --- ENDPOINT PER LA LETTURA ---
# @app.get("/foods")
# def get_foods():
#     """Legge e restituisce il contenuto del file JSON."""
#     data = load_json_data()
#     return data


# # --- ENDPOINT PER LA SCRITTURA ---
# class FoodItem(BaseModel):
#     name: str
#     calories_100g: float


# @app.post("/foods", status_code=status.HTTP_201_CREATED)
# def add_food(item: FoodItem):
#     """Aggiunge un nuovo elemento e aggiorna il file JSON locale."""
#     data = load_json_data()

#     if "foods" not in data:
#         data["foods"] = []

#     # Convertiamo il modello Pydantic in dizionario
#     data["foods"].append(item.model_dump())

#     # Salviamo le modifiche su file
#     save_json_data(data)

#     return {"message": "Elemento salvato con successo", "data": item}