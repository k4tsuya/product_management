"""Main module for the product management app."""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.product_management.data import load_allergens, load_products
from src.product_management.models import Allergen, Base, Product, SessionLocal, engine
from src.product_management.schemas import ProductResponse

app = FastAPI(title="Snack Bar Product API")


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        load_allergens(db)
        load_products(db)


@app.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """Return all products."""
    return db.query(Product).all()


@app.get("/allergens")
def list_allergens(db: Session = Depends(get_db)):
    """Return all allergens."""
    return db.query(Allergen).order_by(Allergen.description_en).all()
