from pydantic import BaseModel

from api.dtos.product_dto import ProductDTO


class SearchResponseDTO(BaseModel):
    products: list[ProductDTO]
