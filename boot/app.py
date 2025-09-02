from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.controllers.products_controller import router as products_router
from api.errors import register_handlers
from config.logger import configure_logging
from config.vars import DEBUG


def create_app() -> FastAPI:
    configure_logging(DEBUG)
    app = FastAPI(title="Optimal Backend")

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React dev server
            "http://localhost:4173",  # Vite dev server
            "http://localhost:5173",  # Vite dev server (dev port)
        ],
        allow_credentials=True,
        allow_methods=["GET", "OPTIONS"],
        allow_headers=["*"],
    )

    # API Routers
    app.include_router(products_router)

    # Exception Handlers
    register_handlers(app)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
