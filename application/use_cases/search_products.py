from application.dtos.product_query import ProductResponse, SearchProductsResponse
from domain.repositories.product_repository import ProductRepository


class SearchProductsUseCase:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self, term: str) -> SearchProductsResponse:
        products = self._repo.search_by_term(term)
        return SearchProductsResponse(
            items=[
                ProductResponse(
                    name=p.name,
                    url=p.url,
                    image=p.image,
                    price=p.price,
                    price_per_unit=p.price_per_unit,
                    supermarket=p.supermarket,
                )
                for p in products
            ]
        )
