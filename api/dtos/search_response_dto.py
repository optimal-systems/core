from pydantic import BaseModel

from api.dtos.product_dto import ProductDTO


class SearchResponseDTO(BaseModel):
    products: list[ProductDTO]
    page: int
    pagesize: int
    has_more: bool
    total: int | None = None
