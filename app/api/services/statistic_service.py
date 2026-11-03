from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model import UserValueModel, JoinedUserTabModel, StatisticUser
from app.models.statistic_users import StatisticUserMapped
from app.utils.calculate_statistic import calculate_user_statistics
from app.api.crud import statistic_crud

async def process_and_save_statistic(email_user: str, db: AsyncSession) -> tuple[StatisticUser | None, str]:
    """
    Gestisce l'intera logica di business: recupero dati, calcolo, 
    controllo duplicati e salvataggio condizionale.
    Ritorna una tupla (dati_statistica, messaggio).
    """
    # 1. Recupero dati dal CRUD
    rows = await statistic_crud.get_user_values_with_name(db, email_user)
    if not rows:
        raise ValueError("USER_NOT_FOUND")

    list_user_value: list[UserValueModel] = []
    user_name_from_db = rows[0][1]

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

    user_joined = JoinedUserTabModel(
        user_value=list_user_value,
        name=user_name_from_db
    )

    if not user_joined.user_value:
        raise ValueError("EMPTY_BMR_LIST")

    # 2. Calcolo statistiche
    new_s_u = calculate_user_statistics(user_joined)
    if not new_s_u:
        raise RuntimeError("CALCULATION_FAILED")

    # 3. Controllo duplicati tramite l'ultimo record salvato
    last_stat = await statistic_crud.get_last_user_statistic(db, email_user)
    
    is_duplicate = False
    if last_stat:
        if last_stat.list_bmr == new_s_u.list_bmr and last_stat.list_weight == new_s_u.list_weight:
            is_duplicate = True

    if is_duplicate:
        message_text = "Statistiche già aggiornate all'ultimo stato disponibile (nessun nuovo inserimento)"
    else:
        # 4. Creazione e salvataggio del nuovo snapshot
        db_statistic = StatisticUserMapped(
            token=new_s_u.token,
            email=email_user,
            name=user_name_from_db,
            list_weight=new_s_u.list_weight,
            list_height=new_s_u.list_height,
            list_age=new_s_u.list_age,
            list_activity=new_s_u.list_activity,
            list_bmr=new_s_u.list_bmr,
            average_weight=new_s_u.average_weight,
            average_height=new_s_u.average_height,
            average_age=new_s_u.average_age,
            average_activity=new_s_u.average_activity,
            average_bmr=new_s_u.average_bmr,
            creations_date=datetime.now(timezone.utc),
            list_order=new_s_u.list_order
        )
        await statistic_crud.create_user_statistic(db, db_statistic)
        message_text = "Nuova riga di statistica inserita con successo nello storico"

    return new_s_u, message_text