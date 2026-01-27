"""Module containing models for the product management app."""

from sqlalchemy import Column, ForeignKey, String, Table, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

protocol = "sqlite"
db_name = "product_management.db"

DATABASE_URL = f"{protocol}:///{db_name}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


product_allergen = Table(
    "product_allergen",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("allergen_id", ForeignKey("allergens.id"), primary_key=True),
)


class Allergen(Base):
    __tablename__ = "allergens"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description_en: Mapped[str] = mapped_column(String(200), nullable=False)
    description_nl: Mapped[str] = mapped_column(String(200), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        secondary=product_allergen,
        back_populates="allergens",
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    allergens: Mapped[list[Allergen]] = relationship(
        secondary=product_allergen,
        back_populates="products",
    )
