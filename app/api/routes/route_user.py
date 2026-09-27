# qui le routes per gestire le API utente
from fastapi import APIRouter, Body, Response, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model import (
    ResponseAPI,
    UserModel,
    UserValueModel,
    JoinedUserTabModel,
    StatisticUser,
)
from app.models.user_value import UserValue
from app.models.users import User
from app.utils.hash_pw import hash_password, verify_password
from app.core.database import get_db
from sqlalchemy import select
from urllib.parse import unquote
import hashlib
from typing import Any
from datetime import datetime

from app.utils.response_example import make_response_example
from app.utils.statistic_words import (
    statistic_words,
    statistic_number,
    statistic_number_average,
    statistic_age_average,
)
from app.utils.replace_dots import replace_dots_words
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import io
import asyncio

from collections import Counter

routes = APIRouter()

env = Environment(loader=FileSystemLoader("templates"))

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
                success=False,
                message="Nessuna email valida",
                data=None,
                status=400
            )
            
        email_user = unquote(email).strip().lower()

        # Query con il filtro WHERE per prendere solo l'utente richiesto
        stmt = (
            select(UserValue, User.name)
            .join(User, User.token == UserValue.token_user)
            .where(UserValue.user_name == email_user)
        )

        res = await db.execute(stmt)
        rows = res.all()

        print("ROWS DB: ", rows)

        if not rows:
            return ResponseAPI[None](
                success=False,
                message="La lista da DB è vuota!",
                data=None,
                status=404,
            )

        # 1. Raccogliamo tutti i record UserValueModel nella lista
        list_user_value: list[UserValueModel] = []
        user_name_from_db = rows[0][1]  # Il nome dell'utente dalla prima riga

        for uv, _ in rows:
            uv_item = UserValueModel(
                id=uv.id,
                created_at=str(uv.created_at),
                user_name=uv.user_name,
                weight=str(uv.weight),
                height=str(uv.height),
                age=str(uv.age),
                token_user=uv.token_user,
                activity=uv.activity,
                bmr=str(uv.bmr),
                gender=uv.gender,
                order=uv.order,
            )
            list_user_value.append(uv_item)

        # 2. Creiamo UN UNICO oggetto JoinedUserTabModel!
        user_joined = JoinedUserTabModel(
            user_value=list_user_value,
            name=user_name_from_db
        )

        # Ora user_joined.user_value è davvero la lista di tutti i BMR!
        if len(user_joined.user_value) == 0:
            return ResponseAPI[None](
                success=False,
                message="La lista BMR dell'utente è vuota",
                data=None,
                status=404,
            )

        new_s_u = replace_dots_words(user_joined)
        if (new_s_u is None):
            return ResponseAPI[Any](
               success=False, message="Chiamata API fallita!", data=str(e), status=500
            )
        
        print("User Value RITORNA: ", new_s_u)
        return ResponseAPI[StatisticUser](
            success=True,
            message="Statistiche dell'utente presenti",
            data=new_s_u,
            status=200,
        )

    except Exception as e:
        return ResponseAPI[Any](
            success=False, message="Chiamata API fallita!", data=str(e), status=500
        )


def render_pdf(html: str) -> bytes:
    return HTML(string=html).write_pdf()

@routes.post("/api/stat-pdf")
async def stat_pdf(stat: StatisticUser):
    template = env.get_template("bmr_template.html")
    stat.list_order = list(range(len(stat.list_bmr)))
    html = template.render(stat=stat)

    # WeasyPrint è sincrono → lo spostiamo in threadpool
    pdf_bytes = await asyncio.to_thread(render_pdf, html)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=bmr_statistiche.pdf"}
    )
    
    