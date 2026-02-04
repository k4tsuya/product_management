"""Main module for the product management app."""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from pathlib import Path
from src.product_management.data import load_allergens, load_products
from src.product_management.models import Base, SessionLocal, engine
from src.product_management.schemas import ProductResponse
from src.product_management.queries import list_allergens, list_products, get_gluten_free_products, pdf_list_products
from src.product_management.pdf_generator import AllergenMatrixPDF
from fastapi.responses import FileResponse

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
def list_all_products(db: Session = Depends(get_db)):
    """Return all products."""
    return list_products(db)

@app.get("/gluten-free", response_model=list[ProductResponse])
def list_gluten_free_products(db: Session = Depends(get_db)):
    """Return all gluten-free products."""
    return get_gluten_free_products(db)


@app.get("/allergens")
def list_all_allergens(db: Session = Depends(get_db)):
    """Return all allergens."""
    return list_allergens(db)



BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "generated"
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/products/pdf", response_class=FileResponse)
def download_products_pdf(db: Session = Depends(get_db)):
    """Save a PDF of all products and their allergens."""

    # Set language with "en" for English or "nl" for Dutch
    language = "nl"

    products = pdf_list_products(db)
    file_path = OUTPUT_DIR / "product_allergens.pdf"

    pdf = AllergenMatrixPDF(orientation="L")
    pdf.set_language(language)
    pdf.generate_allergen_matrix_pdf(
        data=products,
        output_path=str(file_path),
        language=language
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="products_allergens.pdf",
    )