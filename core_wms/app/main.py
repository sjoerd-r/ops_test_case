from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core_wms.app.config.settings import settings
from core_wms.app.graphql.app import create_graphql_app

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app.name, version=settings.app.version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    graphql_router = create_graphql_app()
    app.include_router(graphql_router)

    return app

app = create_app()