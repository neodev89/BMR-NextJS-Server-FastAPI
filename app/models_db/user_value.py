from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime

class UserValue(Base):
    __tablename__ = "user_value_bmr_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[str] = mapped_column(String, nullable=False)
    height: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[str] = mapped_column(String, nullable=False)
    token_user: Mapped[str] = mapped_column(String, nullable=False)
    activity: Mapped[str] = mapped_column(String, nullable=False)
    bmr: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
