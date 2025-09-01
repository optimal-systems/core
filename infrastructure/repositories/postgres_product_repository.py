import logging

from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository
from infrastructure.database.postgres import execute_query


class PostgresProductRepository(ProductRepository):
    def search_by_term(self, term: str) -> list[Product]:
        rows = execute_query("SELECT * FROM prod.search_products(%s);", (term,))
        logging.debug(f"Rows: {rows[0]}")
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
