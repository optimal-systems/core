from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: int
    name: str
    supermarket: str
    price: float
    url: str
    rank: float | None = None
