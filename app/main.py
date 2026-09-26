from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.controllers.calculation_controller import router as calculation_router
from app.controllers.history_controller import router as history_router
from app.database import create_database, get_db
from app.errors import install_exception_handlers


def create_app(database_url: str | None = None) -> FastAPI:
    settings = get_settings()
    engine, session_factory = create_database(database_url or settings.database_url)
    app = FastAPI(title="Calculator API", version="1.0.0")

    def override_get_db():
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    app.include_router(calculation_router)
    app.include_router(history_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    install_exception_handlers(app)
    app.state.engine = engine
    return app


app = create_app()
