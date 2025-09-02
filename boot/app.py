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
            "http://127.0.0.1:4173",  # Alternative localhost
            "http://127.0.0.1:5173",  # Alternative localhost
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
        ],
        expose_headers=["*"],
        max_age=3600,
    )

    # API Routers
    app.include_router(products_router)

    # Exception Handlers
    register_handlers(app)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
