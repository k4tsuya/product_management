"""Module containing schemas for the product management app."""

from pydantic import BaseModel


class AllergenResponse(BaseModel):
    id: int
    code: str
    description_en: str
    description_nl: str

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    allergens: list[AllergenResponse]

    class Config:
        from_attributes = True
