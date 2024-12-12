from .model import *
from app.helper import get_token_header
from fastapi import APIRouter, Depends
from http import HTTPStatus
from .model import *
from .service import *


router = APIRouter(
    prefix="/user",
    dependencies=[Depends(get_token_header)],
    responses={
        HTTPStatus.NOT_FOUND: {"description": "Not found"},
        HTTPStatus.ACCEPTED: {"description": "Success"},
        HTTPStatus.BAD_REQUEST: {"description": "Bad Request"},
        HTTPStatus.CREATED: {"description": "Created with Success"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Error on Server"},
        HTTPStatus.REQUEST_TIMEOUT: {"description": "The server is late"},
    },
)


@router.get("/")
async def get_perfil():
    user = await 


@router.get("/templates")
async def get_templates():
    pass


@router.get("/{id}")
async def read_user(id: str):
    userData = await user.retrieve(id)
    if !(userData):
        raise HTTPException(
            status_code=404, 
            detail="Item not found"
            )
    return {
        "name": fake_users_db[id]["name"], 
        "id": id
        }


@router.put("/{id}", responses={403: {"description": "Operation forbidden"}})
async def update_user(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the user: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.post("/{id}", responses={403: {"description": "Operation forbidden"}})
async def post_user(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the user: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.delete("/{id}", responses={403: {"description": "Operation forbidden"}})
async def delete_user(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the user: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}
