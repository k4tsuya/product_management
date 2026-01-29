"""Module for generating pdfs."""

from collections.abc import Sequence
from dataclasses import dataclass
from fpdf import FPDF


ALLERGEN_COLUMNS = [
    "gluten",
    "crustaceans",
    "eggs",
    "fish",
    "peanuts",
    "soy",
    "milk",
    "nuts",
    "celery",
    "mustard",
    "sesame",
    "sulphites",
    "lupin",
    "molluscs",
]


@dataclass
class ProductAllergenView:
    name: str
    allergens: list[str]


def generate_allergen_matrix_pdf(
    data: Sequence[ProductAllergenView],
    output_path: str,
) -> None:
    """Generate a PDF of all products and their allergens."""
    pdf = FPDF(orientation="L")  # landscape
    pdf.add_page()
    pdf.set_font("Arial", size=8)

    # Title
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Allergen Matrix", ln=True)
    pdf.ln(3)

    # Column sizes
    product_col_width = 30
    allergen_col_width = 18
    row_height = 8

    # Header
    pdf.set_font("Arial", "B", 8)
    pdf.cell(product_col_width, row_height, "Product", border=1)

    for allergen in ALLERGEN_COLUMNS:
        pdf.cell(allergen_col_width, row_height, allergen.capitalize(), border=1)

    pdf.ln()


    # Rows
    pdf.set_font("Arial", size=8)


    fill = False
    for product in data:
        pdf.set_fill_color(255, 255, 255) if fill else pdf.set_fill_color(235, 235, 235)
        fill = not fill

        pdf.cell(product_col_width, row_height, product.name, border=1)

        for allergen in ALLERGEN_COLUMNS:
            mark = "x" if allergen in product.allergens else ""
            pdf.cell(allergen_col_width, row_height, mark, border=1, align="C", fill=True)

        pdf.ln()

    pdf.output(output_path)
