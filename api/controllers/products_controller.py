from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from api.dtos.product_dto import ProductDTO
from application.dtos.product_query import ProductResponse, SearchProductsResponse
from application.use_cases.search_products import SearchProductsUseCase
from config.vars import AUTH_URL, TOKEN_URL
from domain.repositories.product_repository import ProductRepository
from infrastructure.auth.keycloak_client import KeycloakClient
from infrastructure.repositories.postgres_product_repository import PostgresProductRepository

router = APIRouter(prefix="/api/products", tags=["products"])

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl=AUTH_URL, tokenUrl=TOKEN_URL, auto_error=False)

kc = KeycloakClient()
use_case = SearchProductsUseCase(PostgresProductRepository())


async def require_role(token: str = Security(oauth2_scheme), role: str = "optimal_reader"):
    if not token:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        payload = await kc.validate(token)
        username, roles = kc.extract_username_and_roles(payload)
        if role not in roles:
            raise HTTPException(HTTP_403_FORBIDDEN, detail="Unauthorized")
        return {"username": username, "roles": roles}
    except Exception as e:  # JWTError or others
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=str(e)) from e


@router.get("/search", summary="Search products by term")
async def search_products(
    term: str, page: int = 1, pagesize: int = 12, include_total: bool = False, _: dict = Depends(require_role)
):
    """
    Search products by term with pagination.

    Args:
        term: Search term
        page: Page number (starts at 1, defaults to 1)
        pagesize: Number of items per page (0-100, defaults to 12)
        include_total: Whether to include total count (expensive operation)
    """
    # Validate parameters
    if page < 1:
        page = 1
    if pagesize < 0 or pagesize > 100:
        pagesize = 12

    # Calculate offset
    offset = (page - 1) * pagesize

    # Get paginated results
    result = use_case.execute(term, offset=offset, limit=pagesize)
    products = [ProductDTO(**p.model_dump()) for p in result.items]

    # Calculate has_more
    has_more = len(products) == pagesize

    # Get total if requested
    total = None
    if include_total:
        total_result = use_case.execute(term, offset=0, limit=None)
        total = len(total_result.items)

    # Build response excluding None fields
    response_data = {
        "products": [product.model_dump() for product in products],
        "page": page,
        "pagesize": pagesize,
        "has_more": has_more,
    }

    # Solo incluir total si se solicitó
    if include_total and total is not None:
        response_data["total"] = total

    return response_data


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
        # For now we use the same method from the repository
        # In the future you could create a specific method to list
        products = self._repo.search_by_term("", offset=offset, limit=limit)

        # Apply filters
        if supermarket:
            products = [p for p in products if p.supermarket == supermarket]

        # Apply sorting
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


@router.get("/", summary="List products for dashboard")
async def list_products(
    page: int = 1,
    pagesize: int = 12,
    supermarket: str | None = None,
    sort_by: str = "name",  # name, price, supermarket
    sort_order: str = "asc",  # asc, desc
    include_total: bool = False,
    _: dict = Depends(require_role),
):
    """
    List products for dashboard with filtering and sorting.

    Args:
        page: Page number (starts at 1, defaults to 1)
        pagesize: Number of items per page (0-100, defaults to 12)
        supermarket: Filter by supermarket (ahorramas, carrefour)
        sort_by: Sort field (name, price, supermarket)
        sort_order: Sort order (asc, desc)
        include_total: Whether to include total count
    """
    # Check params
    if page < 1:
        page = 1
    if pagesize < 0 or pagesize > 100:
        pagesize = 12
    if sort_by not in ["name", "price", "supermarket"]:
        sort_by = "name"
    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    # Calculate offset
    offset = (page - 1) * pagesize

    # Get products (use a different use case or the same with parameters)
    # For now we use the same use case but with an empty term to get all products
    result = use_case.execute("", offset=offset, limit=pagesize)
    products = [ProductDTO(**p.model_dump()) for p in result.items]

    # Apply filters and sorting
    if supermarket:
        products = [p for p in products if p.supermarket == supermarket]

    # Sort products
    if sort_by == "name":
        products.sort(key=lambda x: x.name, reverse=(sort_order == "desc"))
    elif sort_by == "price":
        products.sort(key=lambda x: x.price, reverse=(sort_order == "desc"))
    elif sort_by == "supermarket":
        products.sort(key=lambda x: x.supermarket, reverse=(sort_order == "desc"))

    # Calculate has_more
    has_more = len(products) == pagesize

    # Get total if requested
    total = None
    if include_total:
        total_result = use_case.execute("", offset=0, limit=None)
        total = len(total_result.items)

    # Build response
    response_data = {
        "products": [product.model_dump() for product in products],
        "page": page,
        "pagesize": pagesize,
        "has_more": has_more,
        "filters": {"supermarket": supermarket, "sort_by": sort_by, "sort_order": sort_order},
    }

    # Only include total if requested
    if include_total and total is not None:
        response_data["total"] = total

    return response_data
