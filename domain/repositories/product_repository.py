from abc import ABC, abstractmethod

from domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def search_by_term(self, term: str) -> list[Product]: ...
