from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str


class PlayerResponse(Player):
    gold: int


class CreatePlayerRequest(BaseModel):
    name: str
    gold: int
