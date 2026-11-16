import asyncio
import os
import io
from urllib.parse import unquote
from fastapi import BackgroundTasks, Depends, FastAPI 
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from app.models.model import StatisticUser

# il metodo FileSystemLoader accetta il nome della cartella da usare per
# caricare il file corretto
env = Environment(loader=FileSystemLoader("templates"))

def render_pdf(html: str) -> bytes:
    return HTML(string=html).write_pdf()

async def creation_email(statistic: StatisticUser, resend_from: str):
    print(f"🔄 Avvio background task: generazione PDF e invio email per {statistic.email}")

    try:
        email_user = unquote(statistic.email).strip().lower()
        # Genero il mio HTML usando il template in mio possesso
        template = env.get_template("bmr_template.html")
        html = template.render(stat=statistic)
        # Genero il PDF a partire dal contenuto HTML
        pdf_bytes = await asyncio.to_thread(render_pdf, html)

        # 2 converto il file grezzo in un file "aperto"
        pdf_stream = io.BytesIO(pdf_bytes)
               
        # 3. Invio dell'email tramite l'SDK ufficiale di Resend
        params = {
            "from": resend_from,  # O il tuo dominio verificato su Resend
            "to": [email_user],
            "subject": "Il tuo Report BMR Personalizzato 📊",
            "html": f"<p>Ciao <strong>{statistic.name}</strong>,</p><p>In allegato trovi il report con le tue statistiche BMR aggiornate.</p>",
            "attachments": [
                {
                    "filename": "bmr_report.pdf",
                    "content": pdf_stream,
                }
            ],
        }
        print(f"La mail è stata inviata all'indirizzo {email_user}")
        return params
    except Exception as exc:
        print(f"❌ Errore durante la generazione o la spedizione dell'email: {exc}")
