from abc import ABC, abstractmethod

from domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def search_by_term(self, term: str, offset: int = 0, limit: int | None = None) -> list[Product]: ...
