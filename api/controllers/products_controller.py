from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from api.dtos.product_dto import ProductDTO
from application.use_cases.search_products import SearchProductsUseCase
from config.vars import AUTH_URL, TOKEN_URL
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
    except Exception as e:  # JWTError u otros
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
    # Validar parámetros
    if page < 1:
        page = 1
    if pagesize < 0 or pagesize > 100:
        pagesize = 12

    # Calcular offset
    offset = (page - 1) * pagesize

    # Obtener resultados paginados
    result = use_case.execute(term, offset=offset, limit=pagesize)
    products = [ProductDTO(**p.model_dump()) for p in result.items]

    # Calcular has_more
    has_more = len(products) == pagesize

    # Obtener total si se solicita
    total = None
    if include_total:
        total_result = use_case.execute(term, offset=0, limit=None)
        total = len(total_result.items)

    # Construir respuesta excluyendo campos None
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
