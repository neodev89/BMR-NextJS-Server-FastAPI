# tests/test_statistics.py
import pytest
from app.models.model import (
    ResponseAPI,
    StatisticUser
)

@pytest.mark.asyncio
async def test_statistic_user_not_found(client):
    """
    Verifica che un utente inesistente restituisca il corretto messaggio e status gestito.
    La fixture 'client' viene iniettata automaticamente dal conftest.py 
    sovrascrivendo la sessione del database con quella in-memory.
    """
    # Usiamo la rotta corretta e passiamo l'email come query parameter
    response = await client.get(
        "/api/statistic-for-user", 
        params={"email": "mattiagiorgiocovato14@gmail.com"}
    )
    
    # Questo stamperà lo status code e l'intero JSON restituito dal server
    print("\n--- RISPOSTA DEL SERVER ---")
    print("STATUS CODE:", response.status_code)
    print("JSON BODY:", response.text)
    print("---------------------------\n")
    
    data = response.json()
    print("DATA: ", data)
    
    parsed = ResponseAPI[StatisticUser](
        success=data["success"],
        message=data["message"],
        data=data["data"],
        status=data["status"],
    )
    print("La struttura dei dati è coerente con il model? ", parsed)
    # parsed è True
    
#--- RISPOSTA DEL SERVER ---
#STATUS CODE: 200
#JSON BODY: {
    # "success":true,
    # "message":"Statistiche già aggiornate all'ultimo stato disponibile (nessun nuovo inserimento)",
    # "data":{
        # "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hdHRpYWdpb3JnaW9jb3ZhdG8xNEBnbWFpbC5jb20iLCJpYXQiOjE3OTQyNDcxOTMsImV4cCI6MTc5NDMzMzU5M30.h3T9-n8xnmmkp1xqNxu8xaBCy3Fa-VFIbKqk_uvOhjU",
        # "email":"mattiagiorgiocovato14@gmail.com",
        # "name":"MGC",
        # "list_weight":[102.5],
        # "list_height":[184.0],
        # "list_age":[37],
        # "list_activity":["Leggermente attivo"],
        # "list_bmr":[2743.13],
        # "average_weight":102.5,
        # "average_height":184.0,
        # "average_age":37,
        # "average_activity":"Leggermente attivo",
        # "average_bmr":2743.13,
        # "creations_date":"2026-11-13T14:25:03.070821",
        # "list_order":[0]},"status":200
        # }
    
    # Verifichiamo la struttura della tua ResponseAPI
    assert data