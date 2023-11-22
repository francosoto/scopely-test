from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import __version__
from app.middleware.access_log_middleware import LogMiddleware


def init_app() -> FastAPI:
    """
    Initialise a FastApi app, with all the required routes and the
    :return: FastAPI initialized app
    """
    app_ = FastAPI(version=__version__)
    app_.add_middleware(LogMiddleware)
    origins = ["*"]

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app_
