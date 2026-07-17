from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db import Base


class Contest(Base):
    __tablename__ = "contests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fingerprint: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    source: Mapped[str] = mapped_column(String(50), default="pciconcursos", index=True)

    orgao: Mapped[str] = mapped_column(String(255))
    info: Mapped[str] = mapped_column(String(255), default="")
    cargo: Mapped[str] = mapped_column(String(255), default="")
    nivel: Mapped[str] = mapped_column(String(100), default="")
    data_limite: Mapped[str] = mapped_column(String(50), default="")
    link: Mapped[str] = mapped_column(String(1024))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    editais: Mapped[list["Edital"]] = relationship(
        back_populates="contest",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Edital(Base):
    __tablename__ = "editais"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contest_id: Mapped[int] = mapped_column(ForeignKey("contests.id", ondelete="CASCADE"), index=True)
    s3_url: Mapped[str] = mapped_column(String(1024))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    contest: Mapped["Contest"] = relationship(back_populates="editais")
