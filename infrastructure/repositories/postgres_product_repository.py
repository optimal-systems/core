from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository
from infrastructure.database.postgres import execute_query


class PostgresProductRepository(ProductRepository):
    def search_by_term(self, term: str, offset: int = 0, limit: int | None = None) -> list[Product]:
        # Build the query with pagination
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

    def list_products(
        self,
        offset: int = 0,
        limit: int | None = None,
        supermarket: str | None = None,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> list[Product]:
        # Build the base query
        base_query = """
        SELECT id, name, supermarket, price, url, image, price_per_unit
        FROM prod.products
        WHERE is_active = true
        """

        # Add filter by supermarket if specified
        if supermarket:
            base_query += " AND supermarket = %s"
            params = [supermarket]
        else:
            params = []

        # Add sorting
        valid_sort_fields = {"name": "name", "price": "price", "supermarket": "supermarket"}
        sort_field = valid_sort_fields.get(sort_by, "name")
        sort_direction = "DESC" if sort_order == "desc" else "ASC"
        base_query += f" ORDER BY {sort_field} {sort_direction}"

        # Add pagination
        if limit is not None:
            base_query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
        else:
            base_query += " OFFSET %s"
            params.append(offset)

        # Execute query
        rows = execute_query(base_query, params)
        return [
            Product(
                name=row["name"],
                supermarket=row["supermarket"],
                price=float(row["price"]),
                url=row["url"],
                image=row.get("image"),
                price_per_unit=row.get("price_per_unit"),
            )
            for row in rows or []
        ]
