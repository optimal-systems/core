from pydantic import BaseModel


class SearchProductsRequest(BaseModel):
    term: str


class ProductResponse(BaseModel):
    name: str
    url: str
    image: str | None
    price: float
    price_per_unit: str | None
    supermarket: str


class SearchProductsResponse(BaseModel):
    items: list[ProductResponse]
