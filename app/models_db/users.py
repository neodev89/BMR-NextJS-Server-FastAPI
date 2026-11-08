import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, String, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "registered_bmr_table"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    
