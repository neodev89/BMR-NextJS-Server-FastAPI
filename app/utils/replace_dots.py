from app.models.model import (
    StatisticUser,
    JoinedUserTabModel
)
from datetime import datetime
from app.utils.statistic_words import (
    statistic_words,
    statistic_number,
    statistic_number_average,
    statistic_age_average,
)

def replace_dots_words(user_joined: JoinedUserTabModel) -> StatisticUser:
    # 3. Inizializziamo l'oggetto per le statistiche prendendo i dati dal primo record
    first_uv = user_joined.user_value[0]
    new_statistic_user = StatisticUser(
        token=first_uv.token_user,
        email=first_uv.user_name,
        name=user_joined.name,
        list_weight=[],
        list_height=[],
        list_age=[],
        list_activity=[],
        list_bmr=[],
        average_weight="",
        average_height="",
        average_age="",
        average_activity="",
        average_bmr="",
        creation_date="",
        list_order=[],
    )
    
    r_list_weight = []
    r_list_height = []
    r_list_bmr = []
    r_a_weight = ""
    r_a_height = ""
    r_a_bmr = ""

    new_statistic_user.creation_date = datetime.now().strftime("%d/%m/%Y")

    # 4. Popoliamo le liste iterando direttamente su user_joined.user_value!
    for row in user_joined.user_value:
        int_age = int(row.age)
        round_age = round(int_age)
        parsed_age = str(round_age)

        new_statistic_user.list_weight.append(row.weight)
        new_statistic_user.list_height.append(row.height)
        new_statistic_user.list_age.append(parsed_age)
        new_statistic_user.list_activity.append(row.activity)
        new_statistic_user.list_bmr.append(row.bmr)
        new_statistic_user.list_order.append(row.order - 1)
        
    print("ORDER INIZIALE: ", row.order)
    print("ORDER: ", new_statistic_user.list_order)
    # 5. Calcoliamo le medie
    words = [
        "Sedentario",
        "Leggermente attivo",
        "Moderatamente attivo",
        "Molto attivo",
        "Atleta",
    ]
    new_statistic_user.average_activity = statistic_words(
        new_statistic_user.list_activity, words
    )
    new_statistic_user.average_weight = statistic_number_average(
        new_statistic_user.list_weight
    )
    new_statistic_user.average_height = statistic_number_average(
        new_statistic_user.list_height
    )
    new_statistic_user.average_age = statistic_age_average(
        new_statistic_user.list_age
    )
            
    new_statistic_user.average_bmr = statistic_number_average(new_statistic_user.list_bmr)
       
    for w in new_statistic_user.list_weight:
        r_list_weight.append(w.replace(".", ","))
        
    for h in new_statistic_user.list_height:
        r_list_height.append(h.replace(".", ","))
    
    for b in new_statistic_user.list_bmr:
        r_list_bmr.append(b.replace(".", ","))
        
    r_a_weight = new_statistic_user.average_weight.replace(".", ",")
    r_a_bmr = new_statistic_user.average_bmr.replace(".", ",")
    r_a_height = new_statistic_user.average_height.replace(".", ",")
    
    final_statistic = StatisticUser(
        token=first_uv.token_user,
        email=first_uv.user_name,
        name=user_joined.name,
        list_weight=r_list_weight,
        list_height=r_list_height,
        list_age=new_statistic_user.list_age,
        list_activity=new_statistic_user.list_activity,
        list_bmr=r_list_bmr,
        average_weight=r_a_weight,
        average_height=r_a_height,
        average_age=new_statistic_user.average_age,
        average_activity=new_statistic_user.average_activity,
        average_bmr=r_a_bmr,
        creation_date=new_statistic_user.creation_date,
        list_order=new_statistic_user.list_order,
    )    
    
    return final_statistic

    