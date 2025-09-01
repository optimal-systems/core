from application.dtos.product_query import ProductResponse, SearchProductsResponse
from domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(
        self,
        offset: int = 0,
        limit: int | None = None,
        supermarket: str | None = None,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> SearchProductsResponse:
        # Por ahora usamos el mismo método del repositorio
        # En el futuro podrías crear un método específico para listar
        products = self._repo.search_by_term("", offset=offset, limit=limit)

        # Aplicar filtros
        if supermarket:
            products = [p for p in products if p.supermarket == supermarket]

        # Aplicar ordenamiento
        if sort_by == "name":
            products.sort(key=lambda x: x.name, reverse=(sort_order == "desc"))
        elif sort_by == "price":
            products.sort(key=lambda x: x.price, reverse=(sort_order == "desc"))
        elif sort_by == "supermarket":
            products.sort(key=lambda x: x.supermarket, reverse=(sort_order == "desc"))

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
