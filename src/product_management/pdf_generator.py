from dataclasses import dataclass
from fpdf import FPDF


@dataclass
class ProductAllergenView:
    name: str
    allergens: list[str]


def generate_allergen_pdf(
    data: list[ProductAllergenView],
    file_path: str,
) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Allergen List", align="L", ln=True)
    pdf.cell(0, 5, "_"*60, ln=True, align="L")
    pdf.ln(5)

    for item in data:
        allergens = ", ".join(item.allergens) or "No allergens"
        pdf.multi_cell(0, 8, f"{item.name}: {allergens}", ln=True)

    pdf.output(file_path)