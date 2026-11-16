# qui le routes per gestire le API utente
from fastapi import (
    APIRouter, 
    Body, 
    Response, 
    status, 
    HTTPException, 
    Depends
)
from fastapi.responses import StreamingResponse
import resend
import csv
import io
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model import (
    ResponseAPI,
    UserModel,
    UserValueModel,
    JoinedUserTabModel,
    StatisticUser,
    PDFStatisticData,
)
from app.models_db.user_value import UserValue
from app.models_db.users import User
from app.models_db.statistic_users import StatisticUserMapped
from app.utils.hash_pw import hash_password, verify_password
from app.core.database import get_db
from sqlalchemy import select
from urllib.parse import unquote
import hashlib
from typing import Any
from datetime import datetime, timezone

from app.utils.response_example import make_response_example
from app.utils.statistic_words import (
    statistic_words,
    statistic_number,
    statistic_number_average,
    statistic_age_average,
)
from app.utils.calculate_statistic import calculate_user_statistics
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import io
import os
import asyncio
from app.api.services.statistic_service import process_and_save_statistic
from app.api.services.csv_service import csv_process_service
from app.api.crud.statistic_crud import (
    get_last_user_statistic,
    get_all_statistic_user,
    get_user_values_with_name
)
from app.api.services.replace_dec_separator import replace_dec_separator
from app.api.services.format_date import format_italian_date
from app.utils.response_example import make_response_example
from app.api.services.send_pdf_email import creation_email
from collections import Counter
from dotenv import load_dotenv
from pathlib import Path

# Trova la cartella corrente del file in cui ti trovi
current_file_dir = Path(__file__).resolve().parent
print(f"ci troviamo nella rotta {current_file_dir}")

# Se questo codice è in /app/api/routes/file.py, dobbiamo salire di 3 livelli per arrivare alla root,
# oppure se è nel main.py alla root basta .parent
# Usiamo un metodo robusto che cerca il file .env risalendo le cartelle:
env_path = current_file_dir
while env_path != env_path.parent:
    if (env_path / ".env").exists():
        env_path = env_path / ".env"
        break
    env_path = env_path.parent

print(f"la rotta parent è {env_path.parent}")
print(f"la rotta Resend nelle env è {env_path}")

# 2. Carica esplicitamente il .env trovato
load_dotenv(dotenv_path=env_path)
resend_from = os.environ.get("RESEND_FROM")

# 3. Test immediato per verificare se ora lo legge
print("✅ RESEND_FROM caricato correttamente:", resend_from)

# Test immediato per vedere se ora lo legge
print("DEBUG RESEND_FROM:", resend_from)

routes = APIRouter()

env = Environment(loader=FileSystemLoader("templates"))
resend.api_key = os.environ.get("RESEND_KEY")

@routes.get(
    "/api/get-user",
    response_model=ResponseAPI[UserModel | None],
    responses={
        **make_response_example(
            success=False, message="utente non registrato!", data=None, statusRes=404
        ),
    },
)
async def get_user(email: str, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        row = result.scalar_one_or_none()

        if row is None:
            return ResponseAPI[None](
                success=False,
                message="L'utente non risulta registrato",
                data=None,
                status=409,
            )

        return ResponseAPI[UserModel](
            success=True, message="Utente caricato correttamente", data=row, status=200
        )
    except Exception as e:
        return ResponseAPI[Any](
            success=False, message="Errore nella chiamata API", data=str(e), status=500
        )


@routes.post(
    "/api/sign-up",
    response_model=ResponseAPI[UserModel | None],
    responses={
        **make_response_example(
            success=False,
            message="Registrazione utente fallita!",
            data=None,
            statusRes=500,
        ),
        **make_response_example(
            success=False, message="Utente già registrato!", data=None, statusRes=409
        ),
        **make_response_example(
            success=False, message="Dati input non validi!", data=None, statusRes=400
        ),
    },
)
async def sign_up_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    try:
        # 1) Validazione input
        if not isinstance(email, str) or not isinstance(password, str):
            return ResponseAPI[None](
                success=False, message="Dati input non validi", data=None, status=400
            )

        # 2) Controllo utente esistente
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        raw = result.scalar_one_or_none()

        if raw is not None:
            return ResponseAPI[None](
                success=False,
                message="L'utente risulta già registrato",
                data=None,
                status=409,
            )

        # 3) Hash password
        hashed_pw = hash_password(password)

        # 4) Token basato sull'email
        hashed_email = hashlib.sha256(email.encode()).hexdigest()

        # 5) UUID corretto
        id = uuid.uuid4()

        # 6) Creazione nuovo utente
        new_user = UserModel(
            id=id,
            created_at=datetime.now(),
            user_name=email,
            password=hashed_pw,
            token=hashed_email,
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return ResponseAPI[UserModel](
            success=True,
            message="Utente registrato correttamente!",
            data=new_user,
            status=200,
        )

    except Exception as e:
        return ResponseAPI[Any](
            success=False, message="API Fallita!", data=str(e), status=500
        )


@routes.post(
    "/api/login-user",
    response_model=ResponseAPI[UserModel | None],
    responses={
        **make_response_example(
            success=False,
            message="Utente non ancora registrato!",
            data=None,
            statusRes=404,
        ),
    },
)
async def login_user(email: str, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(User).where(User.email == email)
        res = await db.execute(stmt)
        row = res.scalar_one_or_none()

        if row is None:
            return ResponseAPI[None](
                success=False,
                message="L'utente non risulta registrato",
                data=None,
                status=404,
            )

        return ResponseAPI[UserModel](
            success=True,
            message="Utente loggato!",
            data=row,
            status=200,
        )

    except Exception as e:
        return ResponseAPI[Any](
            success=False, message="Errore chiamata API", data=str(e), status=500
        )


@routes.get(
    "/api/statistic-for-user",
    response_model=ResponseAPI[StatisticUser | None | Any],
    responses={
        **make_response_example(
            success=False,
            message="L'utente non ha mai usato l'App",
            data=None,
            statusRes=404,
        ),
    },
)
async def statistic_for_user(email: str, db: AsyncSession = Depends(get_db)):
    try:
        if not email or not email.strip():
            return ResponseAPI[None](
                success=False, message="Nessuna email valida", data=None, status=400
            )
            
        email_user = unquote(email).strip().lower()

        # Deleghiamo tutto al Service Layer
        statistic_data, message = await process_and_save_statistic(email_user, db)

        return ResponseAPI[StatisticUser](
            success=True,
            message=message,
            data=statistic_data,
            status=200,
        )

    except ValueError as ve:
        error_msg = str(ve)
        if error_msg == "USER_NOT_FOUND":
            return ResponseAPI[None](
                success=False, 
                message="La lista da DB è vuota!", 
                data=None, 
                status=404
            )
        if error_msg == "EMPTY_BMR_LIST":
            return ResponseAPI[None](
                success=False, 
                message="La lista BMR dell'utente è vuota", 
                data=None, 
                status=404
            )
        raise ve

    except Exception as e:
        return ResponseAPI[Any](
            success=False, 
            message="Chiamata API fallita e utente non salvato a database!", 
            data=str(e), 
            status=500
        )

def render_pdf(html: str) -> bytes:
    return HTML(string=html).write_pdf()

@routes.post("/api/stat-pdf")
async def stat_pdf(stat: StatisticUser):
    
    new_statistic = PDFStatisticData(
        token=stat.token,
        email=stat.email,
        name=stat.name,
        list_weight=replace_dec_separator(stat.list_weight),
        list_height=replace_dec_separator(stat.list_height),
        list_age=stat.list_age,
        list_activity=stat.list_activity,
        list_bmr=replace_dec_separator(stat.list_bmr),
        average_weight=replace_dec_separator(stat.average_weight),
        average_height=replace_dec_separator(stat.average_height),
        average_age=stat.average_age,
        average_activity=stat.average_activity,
        average_bmr=replace_dec_separator(stat.average_bmr),
        creations_date=format_italian_date(stat.creations_date),
        list_order=stat.list_order,
    )
    
    template = env.get_template("bmr_template.html")
    stat.list_order = list(range(len(new_statistic.list_bmr)))
    html = template.render(stat=new_statistic)

    # WeasyPrint è sincrono → lo spostiamo in threadpool
    pdf_bytes = await asyncio.to_thread(render_pdf, html)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=bmr_statistiche.pdf"}
    )
    
    
@routes.get("/api/export-statistic-for-user/csv")
async def download_statistic_csv(email: str, db: AsyncSession = Depends(get_db)):
    try:
        # Controllo se l'email è None o una stringa vuota
        if not email or not email.strip():
            return ResponseAPI[None](
                success=False,
                message="Email non definita",
                data=None,
                status=400,
            )
            
        email_user = unquote(email).strip().lower()
        
        records = await get_all_statistic_user(db, email_user)
        
        if not records:
            return ResponseAPI[None](
                success=False,
                message="Nessun utente corrispondente alla mail",
                data=None,
                status=404
            )
                   
        csv_service_def = await csv_process_service(records=records, email_user=email_user)
        if not csv_service_def:
            return ResponseAPI[None](
                success=False,
                message="il CSV non è stato creato!",
                data=None,
                status=400
            )
        
        return StreamingResponse(
            iter([csv_service_def.output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={csv_service_def.filename}"
            }
        )
        
    except Exception as e:
        return ResponseAPI[Any](
            success=False,
            message=f"API Fallita a causa dell'errore {e}",
            data=None,
            status=500,
        )
        
@routes.post("/api/send-statistic-pdf")
async def send_statistic_user_pdf(stat_user: StatisticUser):
    try:
        # 1. Genera il PDF in memoria e prepara il dizionario per Resend tramite il servizio
        params = await creation_email(stat_user, resend_from=resend_from)
        
        # 2. Invia effettivamente l'email tramite l'SDK di Resend
        email_response = resend.Emails.send(params)
        print("✅ Email inviata con successo! Risposta grezza di Resend:", email_response)

        # 3. Restituisci la risposta di successo al client
        return ResponseAPI[dict](
            success=True,
            message="Report BMR generato e inviato via email con successo!",
            data={"resend_response": email_response},
            status=200
        )
        
    except Exception as e:
        print(f"❌ Errore critico durante l'invio: {str(e)}")
        return ResponseAPI[None](
            success=False,
            message=f"Invio API fallito a causa di: {str(e)}",
            data=None,
            status=500,
        )