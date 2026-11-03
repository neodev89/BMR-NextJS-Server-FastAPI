from datetime import datetime
from typing import List

from app.models.model import (
    StatisticUser,
    JoinedUserTabModel
)
from app.utils.statistic_words import (
    statistic_words,
    statistic_number,
    statistic_number_average,
    statistic_age_average,
)


ACTIVITY_LEVELS: List[str] = [
    "Sedentario",
    "Leggermente attivo",
    "Moderatamente attivo",
    "Molto attivo",
    "Atleta",
]
    

def calculate_user_statistics(user_joined: JoinedUserTabModel) -> StatisticUser:
    if not user_joined.user_value:
        raise ValueError("La lista 'user_value' non può essere vuota.")

    first_uv = user_joined.user_value[0]

    # I dati sono già float e int grazie a Pydantic!
    weights = [uv.weight for uv in user_joined.user_value]
    heights = [uv.height for uv in user_joined.user_value]
    ages = [uv.age for uv in user_joined.user_value]
    bmrs = [uv.bmr for uv in user_joined.user_value]

    return StatisticUser(
        token=first_uv.token_user,
        email=first_uv.user_name,
        name=user_joined.name,
        list_weight=weights,
        list_height=heights,
        list_age=ages,
        list_activity=[uv.activity for uv in user_joined.user_value],
        list_bmr=bmrs,
        average_weight=statistic_number_average(weights),
        average_height=statistic_number_average(heights),
        average_age=statistic_age_average(ages),
        average_activity=statistic_words(
            [uv.activity for uv in user_joined.user_value], ACTIVITY_LEVELS
        ),
        average_bmr=statistic_number_average(bmrs),
        creations_date=datetime.now(),
        list_order=[uv.order - 1 for uv in user_joined.user_value],
    )    