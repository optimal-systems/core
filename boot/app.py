from fastapi import FastAPI

from api.controllers.products_controller import router as products_router
from api.errors import register_handlers
from config.logger import configure_logging
from config.vars import DEBUG


def create_app() -> FastAPI:
    configure_logging(DEBUG)
    app = FastAPI(title="Optimal Backend")

    # API Routers
    app.include_router(products_router)

    # Exception Handlers
    register_handlers(app)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
