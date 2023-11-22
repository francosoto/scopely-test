import logging

from app.app import app_create_player, app_get_player
from app.initializers import init_app
from app.utils.db_connector import get_db, DbConnector
from app.utils.cache_connector import get_cache
from fastapi import Depends
from starlette import status
from app.containers.dto import (
    PlayerResponse,
    CreatePlayerRequest,
)

# Disable uvicorn access log
logging.getLogger("uvicorn.access").disabled = True
logging.getLogger("uvicorn").handlers.clear()
app = init_app()


@app.get("/player/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int, db: DbConnector = Depends(get_db), cache=Depends(get_cache)
):
    """
    HTTP GET endpoint to obtain player data by id
    :param player_id: The player identifier
    :param db: A database connection to perform the relevants query
    :param cache: A cache connection to get some data faster
    :returns: JSON blob player object
        {
          "id": 2,
          "name": "player name",
          "gold": 12234
        }
    Also if some error happened:
        {
          "detail": "Cannot create player, try it again"
        }
    """
    return app_get_player(db, cache, player_id)


@app.post("/player", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def post_player(
    request: CreatePlayerRequest,
    db: DbConnector = Depends(get_db),
    cache=Depends(get_cache),
):
    """
    :param request: A dictionary with relevant player data like this:
        {
            "name": "player name",
            "gold": 1234
        }
    :param db: A database connection to perform the relevants query
    :param cache: A cache connection to get some data faster
    :returns: JSON blob new player object
        {
          "id": 2,
          "name": "player name",
          "gold": 1234
        }
    Also if some error happened:
        {
          "detail": "Cannot create player, try it again"
        }
    """
    return app_create_player(db, cache, request)
