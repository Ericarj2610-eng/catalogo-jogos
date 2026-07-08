from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Genero(Base):
    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]

    jogos: Mapped[list["Jogo"]] = relationship(
        back_populates="genero"
    )


class Jogo(Base):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    desenvolvedora: Mapped[str]

    data_lancamento: Mapped[date] = mapped_column(Date)

    genero_id: Mapped[int] = mapped_column(
        ForeignKey("generos.id")
    )

    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    genero: Mapped["Genero"] = relationship(
        back_populates="jogos"
    )