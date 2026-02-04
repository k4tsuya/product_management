"""Module for generating pdfs."""

from collections.abc import Sequence, Callable
from dataclasses import dataclass
from fpdf import FPDF
from src.product_management.allergens import ALLERGENS


TEXTS = {
    "en": { "title": "Allergen Matrix",
           "footer": "Page ",
    },
    "nl": { "title": "Allergenen Lijst",
           "footer": "Pagina "
    }}


@dataclass
class ProductAllergenView:
    name: str
    allergens: list[str]


class AllergenMatrixPDF(FPDF):
    def set_language(self, language: str) -> None:
        if language not in {"nl", "en"}:
            raise ValueError("language must be 'nl' or 'en'")
        self.language = language
        self.texts = TEXTS[language]

    def get_allergen_labels(self, language: str) -> dict[str, dict[str, str]]:
        if language not in {"nl", "en"}:
            raise ValueError("language must be 'nl' or 'en'")
        language = language
        return {
            code: {
            "label": data[language],
            "icon": data["icon"],
            }
            for code, data in ALLERGENS.items()
        }


    # ---------- Page setup ----------
    def start_new_page(
        self,
        allergen_codes: list[str],
        allergen_labels: dict[str, dict],
        product_col_width: int,
        allergen_col_width: int,
        row_height: int,
    ) -> None:
        self.add_page()

        # Title
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"{self.texts["title"]}", ln=True)

        self.ln(3)

        # Icon header row
        self.set_font("Arial", "B", 8)
        self.cell(product_col_width, row_height, "", border=1)

        for code in allergen_codes:
            x = self.get_x()
            y = self.get_y()

            self.cell(allergen_col_width, row_height, "", border=1)

            icon_size = 7
            icon_path = allergen_labels[code]["icon"]

            self.image(
                str(icon_path),
                x + (allergen_col_width - icon_size) / 2,
                y + (row_height - icon_size) / 2,
                w=icon_size,
                h=icon_size,
            )

        self.ln()

        # Label header row
        self.cell(product_col_width, row_height, "Product", border=1)

        for code in allergen_codes:
            label = allergen_labels[code]["label"]
            self.cell(allergen_col_width, row_height, label, border=1, align="C")

        self.ln()

        # Reset font for rows
        self.set_font("Arial", size=8)

    # ---------- Page break helper ----------
    def check_page_break(
        self,
        next_row_height: int,
        start_page: Callable[[], None],
    ) -> None:
        if self.get_y() + next_row_height > self.h - self.b_margin:
            start_page()

    # ---------- Footer ----------
    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"{self.texts["footer"]} {self.page_no()} / {{nb}}", ln=True, align="C")

    # ---------- Main generator ----------
    def generate_allergen_matrix_pdf(
        self,
        data: Sequence["ProductAllergenView"],
        output_path: str,
        language: str
    ) -> None:
        allergen_labels = self.get_allergen_labels(language)
        allergen_codes = list(allergen_labels.keys())

        # Layout constants
        product_col_width = 30
        allergen_col_width = 18
        row_height = 10

        self.alias_nb_pages()

        # First page
        self.start_new_page(
            allergen_codes,
            allergen_labels,
            product_col_width,
            allergen_col_width,
            row_height,
        )

        fill = False
        for product in data:
            self.check_page_break(
                row_height,
                lambda: self.start_new_page(
                    allergen_codes,
                    allergen_labels,
                    product_col_width,
                    allergen_col_width,
                    row_height,
                ),
            )

            self.set_fill_color(235, 235, 235 if fill else 255)
            fill = not fill

            self.cell(
                product_col_width,
                row_height,
                product.name,
                border=1,
                fill=True,
            )

            for code in allergen_codes:
                mark = "x" if code in product.allergens else ""
                self.cell(
                    allergen_col_width,
                    row_height,
                    mark,
                    border=1,
                    align="C",
                    fill=True,
                )

            self.ln()

        self.output(output_path)
