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


async def require_role(token: str = Security(oauth2_scheme), role: str = None):
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


@router.get("/search", response_model=list[ProductDTO], summary="Search products by term")
async def search_products(term: str, _: dict = Depends(require_role)):
    result = use_case.execute(term)
    return [ProductDTO(**p.model_dump()) for p in result.items]
