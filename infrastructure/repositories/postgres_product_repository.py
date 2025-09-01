from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository
from infrastructure.database.postgres import execute_query


class PostgresProductRepository(ProductRepository):
    def search_by_term(self, term: str, offset: int = 0, limit: int | None = None) -> list[Product]:
        # Construir la consulta con paginación
        if limit is not None:
            query = "SELECT * FROM prod.search_products(%s) LIMIT %s OFFSET %s;"
            params = (term, limit, offset)
        else:
            query = "SELECT * FROM prod.search_products(%s) OFFSET %s;"
            params = (term, offset)

        rows = execute_query(query, params)
        return [
            Product(
                name=row["name"],
                supermarket=row["supermarket"],
                price=float(row["price"]),
                url=row["url"],
                image=row.get("image", None),
                price_per_unit=row.get("price_per_unit", None),
            )
            for row in rows or []
        ]
