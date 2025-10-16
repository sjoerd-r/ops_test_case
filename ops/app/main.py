from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ops.app.api.graphql.router import router as graphql_router


def create_app() -> FastAPI:
    app = FastAPI(title="ops", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(graphql_router)

    return app

app = create_app()

