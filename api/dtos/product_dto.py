from pydantic import BaseModel


class ProductDTO(BaseModel):
    name: str
    supermarket: str
    price: float
    url: str
    image: str | None
    price_per_unit: str | None
