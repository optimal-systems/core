from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository
from infrastructure.database.postgres import execute_query


class PostgresProductRepository(ProductRepository):
    def search_by_term(self, term: str) -> list[Product]:
        rows = execute_query("SELECT * FROM prod.search_products(%s);", (term,))
        return [
            Product(
                id=row["id"],
                name=row["name"],
                supermarket=row["supermarket"],
                price=float(row["price"]),
                url=row["url"],
                rank=float(row["rank"]) if row.get("rank") is not None else None,
            )
            for row in rows or []
        ]
