"""Module for inserting data into the database."""

from sqlalchemy.orm import Session

from src.product_management.models import Allergen, Product

# NVWA allergen list (simplified)
ALLERGENS = [
    ("gluten", "Cereals containing gluten", "Glutenbevattende granen"),
    ("crustaceans", "Crustaceans", "Schaaldieren"),
    ("eggs", "Eggs", "Eieren"),
    ("fish", "Fish", "Vis"),
    ("peanuts", "Peanuts", "Pinda's"),
    ("soy", "Soybeans", "Sojabonen"),
    ("milk", "Milk", "Melk"),
    ("nuts", "Nuts", "Noten"),
    ("celery", "Celery", "Selderij"),
    ("mustard", "Mustard", "Mosterd"),
    ("sesame", "Sesame seeds", "Sesamzaad"),
    ("sulphites", "Sulphur dioxide and sulphites", "Zwaveldioxide en sulfieten"),
    ("lupin", "Lupin", "Lupine"),
    ("molluscs", "Molluscs", "Weekdieren"),
]


PRODUCTS = {
    "Frikandel": ["gluten", "soy", "mustard"],
    "Kroket": ["gluten", "milk"],
    "Bread": ["gluten"],
}

def load_allergens(db: Session) -> None:
    """Insert allergens into the db if they don't exist."""
    for code, en, nl in ALLERGENS:
        if db.query(Allergen).filter_by(code=code).first():
            continue

        db.add(
            Allergen(
                code=code,
                description_en=en,
                description_nl=nl,
            )
        )

    db.commit()


def load_products(db: Session) -> None:
    """Insert products into the db with the corresponding allergens."""
    allergens_by_code = {
        allergen.code: allergen
        for allergen in db.query(Allergen).all()
    }

    for name, allergen_codes in PRODUCTS.items():
        if db.query(Product).filter_by(name=name).first():
            continue

        product = Product(name=name)

        for code in allergen_codes:
            product.allergens.append(allergens_by_code[code])

        db.add(product)

    db.commit()