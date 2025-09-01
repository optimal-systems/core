from typing import Any

import httpx
from jose import jwk, jwt
from jose.exceptions import JWTError

from config.vars import JWKS_URL, KEYCLOAK_CLIENT_ID


class KeycloakClient:
    def __init__(self, jwks_url: str = JWKS_URL, audience: str = KEYCLOAK_CLIENT_ID):
        self._jwks_url = jwks_url
        self._aud = audience

    async def validate(self, token: str) -> dict[str, Any]:
        """
        Valida y decodifica el JWT con JWKS (Keycloak 26.x).
        Devuelve el payload si es válido o lanza JWTError.
        """
        async with httpx.AsyncClient() as client:
            resp = await client.get(self._jwks_url)
            resp.raise_for_status()
            jwks = resp.json()

        headers = jwt.get_unverified_headers(token)
        kid = headers.get("kid")
        key_data = next((k for k in jwks["keys"] if k.get("kid") == kid), None)
        if not key_data:
            raise JWTError("JWK no encontrado para kid")

        public_key = jwk.construct(key_data).public_key()

        payload = jwt.decode(token, key=public_key, algorithms=["RS256"], audience=self._aud)
        return payload

    @staticmethod
    def extract_username_and_roles(payload: dict[str, Any]) -> tuple[str, list[str]]:
        username = payload.get("preferred_username") or payload.get("sub")
        realm_roles = payload.get("realm_access", {}).get("roles", [])
        client_roles = []
        ra = payload.get("resource_access", {})
        if isinstance(ra, dict):
            for _client, data in ra.items():
                if isinstance(data, dict):
                    client_roles.extend(data.get("roles", []))
        roles = sorted(set(realm_roles + client_roles))
        return username, roles
