from . import *


router = APIRouter(
    prefix="/finance",
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_finance():
    return 0


@router.get("/entry")
async def get_entries():
    return 0


@router.get("/exit")
async def get_exits():
    return 0


@router.get("/transfer")
async def get_transfers():
    return 0



@router.get("/{id}")
async def read_finance(id: str):
    if id not in fake_finances_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_finances_db[id]["name"], "id": id}


@router.put("/{id}", responses={403: {"description": "Operation forbidden"}})
async def update_finance(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the finance: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.post("/{id}", responses={403: {"description": "Operation forbidden"}})
async def post_finance(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the finance: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.delete("/{id}", responses={403: {"description": "Operation forbidden"}})
async def delete_finance(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the finance: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}
