"""creature routes"""

from fastapi import APIRouter
from model.creature import Creature
import service.creature as service

router = APIRouter(prefix = '/creature')

@router.get("/")
def get_all()-> list[Creature]:
    return service.get_all()

@router.get("/{name}")
def get_one(name:str) -> Creature | None:
    return service.get_one(name)



# dummy endpoint. dont do nothing yet
@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)

@router.patch("/")
def modify(creature: Creature)-> Creature:
    return service.modify(creature)


@router.delete("/{name}")
def delete(name: str):
    return None