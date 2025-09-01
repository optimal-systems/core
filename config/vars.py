import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Keycloak
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
REALM_NAME = os.getenv("KEYCLOAK_REALM", "master")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi")

JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/certs"
TOKEN_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
AUTH_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth"

# Postgres
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "optimal"),
    "user": os.getenv("POSTGRES_USER", "optimal_backend"),
    "password": os.getenv("POSTGRES_PASSWORD", "backend_supersecret"),
    "minconn": int(os.getenv("POSTGRES_MIN_CONN", "1")),
    "maxconn": int(os.getenv("POSTGRES_MAX_CONN", "10")),
}
