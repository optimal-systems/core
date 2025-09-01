from abc import ABC, abstractmethod

from domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def search_by_term(self, term: str, offset: int = 0, limit: int | None = None) -> list[Product]: ...

    @abstractmethod
    def list_products(
        self,
        offset: int = 0,
        limit: int | None = None,
        supermarket: str | None = None,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> list[Product]: ...
