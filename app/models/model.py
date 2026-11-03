# qui inserire le classi per inferire le Response API
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from pydantic.generics import GenericModel
from typing import Optional, TypeVar, Generic, List, Annotated, Any
import uuid
from datetime import datetime
from dataclasses import dataclass
import io

T = TypeVar("T")

class ResponseAPI(GenericModel, Generic[T]):
    success: bool
    message: str
    data: T
    status: int
    
class UserModel(BaseModel):
    id: uuid.UUID
    created_at: datetime
    user_name: str
    password: str
    name: str
    token: str
    
@dataclass
class CSVResult:
    filename: str
    output: io.StringIO
    
def parse_italian_float(value: Any) -> float:
    """Validator che converte stringhe da form 
    (es. '70,5' o '70.5') o numeri in float."""
    if isinstance(value, str):
        # Normalizza sostituendo la virgola con il punto e rimuove spazi bianchi
        cleaned_str = value.replace(",", ".").strip()
        return float(cleaned_str)
    return float(value)

Italian_float = Annotated[float, BeforeValidator(parse_italian_float)]
    
class UserValueModel(BaseModel):
    id: int
    created_at: datetime
    user_name: str
    token_user: str
    gender: str
    order: int

    # Questi campi ORA ACCETTANO sia stringhe ("70,5", "70.5") che float (70.5),
    # ma dopo la validazione saranno SEMPRE float!
    weight: Italian_float = Field(..., gt=0, description="Peso in kg")
    height: Italian_float = Field(..., gt=0, description="Altezza in cm")
    age: int = Field(..., ge=0, le=120, description="Età in anni")
    bmr: Italian_float = Field(..., gt=0, description="BMR in kcal")
    activity: str
    
class JoinedUserTabModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    user_value: List[UserValueModel]
    name: str  
    
class StatisticUser(BaseModel):
    token: str
    email: str
    name: str

    # Liste numeriche (float per pesi/altezze/bmr, int per età)
    list_weight: List[float]
    list_height: List[float]
    list_age: List[int]
    list_activity: List[str]
    list_bmr: List[float]

    # Medie numeriche
    average_weight: float
    average_height: float
    average_age: int
    average_activity: str
    average_bmr: float

    # datetime nativo (Pydantic lo serializzerà in ISO-8601 string nel JSON finale)
    creations_date: datetime = Field(default_factory=datetime.now)
    list_order: List[int]
       
class PropsFoodModel(BaseModel):
    nome: str
    calorie_100g: int
    unita: str
    
class VociListaFood(BaseModel):
    primi_e_cereali: List[PropsFoodModel]
    carni_e_salumi: List[PropsFoodModel]
    pesce_e_frutti_di_mare: List[PropsFoodModel]
    latticini_e_formaggi: List[PropsFoodModel]
    verdure_e_legumi: List[PropsFoodModel]
    frutta: List[PropsFoodModel]
    condimenti_e_grassi: List[PropsFoodModel]
    dolci_e_colazioni: List[PropsFoodModel]
    
class FoodValueModel(BaseModel):
    cibi_italiani_calorie_100g: VociListaFood
    
    model_config = ConfigDict(from_attributes=True)