from sqlalchemy import Integer, String, Float, ARRAY, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from typing import List
from datetime import datetime


class StatisticUserMapped(Base):
    __tablename__ = "statistic_user"
    
    # Aggiungiamo un ID come chiave primaria (best practice in SQLAlchemy/Postgres)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    token: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Correzione delle liste con l'uso corretto di ARRAY(...) di SQLAlchemy
    list_weight: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=False)
    list_height: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=False)
    list_age: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=False)
    list_activity: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    list_bmr: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=False)

    average_weight: Mapped[float] = mapped_column(Float, nullable=False)
    average_height: Mapped[float] = mapped_column(Float, nullable=False)
    average_age: Mapped[int] = mapped_column(Integer, nullable=False)
    average_activity: Mapped[str] = mapped_column(String, nullable=False)
    average_bmr: Mapped[float] = mapped_column(Float, nullable=False)

    creations_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    
    list_order: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=False)