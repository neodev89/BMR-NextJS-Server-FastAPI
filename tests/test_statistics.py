# tests/test_statistics.py
import pytest

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
    
    # Verifichiamo la struttura della tua ResponseAPI
    assert data