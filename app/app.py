import structlog

from app.containers.player import Player
from app.containers.dto import PlayerResponse
from fastapi import HTTPException
from starlette import status
from app.utils.db_connector import DBException, DataIntegrityException, DataException

logger = structlog.get_logger(logger_name=__name__)


def app_get_player(db, cache, player_id: int) -> PlayerResponse:
    db_player = db.fetch_one_by_id(Player, player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found."
        )

    player = PlayerResponse
    player.name = db_player.name
    player.id = db_player.id
    cached_gold = cache.get(player_id)
    if cached_gold:
        logger.info("Cached gold getted, replace it by sql stored")
        player.gold = cached_gold

    return player


def app_create_player(db, cache, player_obj) -> PlayerResponse:
    if player_obj.gold >= 1000000000:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Too many gold for this player, you need to set less",
        )

    try:
        player = Player(name=player_obj.name)
        db_player = db.add(player)
    except DataIntegrityException as e:
        logger.error(
            "There was an error trying to create a player into DB", error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Choose a different player name, it is already used.",
        )
    except DataException as e:
        logger.error(
            "There was an error trying to create a player into DB", error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Player name too long, please insert another shorter",
        )
    except DBException as e:
        logger.error(
            "There was an error trying to create a player into DB", error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot create player, try it again",
        )

    cached_gold = cache.set(db_player.id, player_obj.gold)
    if cached_gold:
        player = PlayerResponse
        player.name = player_obj.name
        player.gold = player_obj.gold
        player.id = db_player.id
        return player

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Error trying to save gold into cache",
    )
