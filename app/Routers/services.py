from . import *


router = APIRouter(
    prefix="/service",
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_service():
    return 0


@router.get("/process")
async def get_process_service():
    return 0


@router.get("/{id}")
async def read_service(id: str):
    if id not in fake_services_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_services_db[id]["name"], "id": id}


@router.put("/{id}", responses={403: {"description": "Operation forbidden"}})
async def update_service(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the service: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.post("/{id}", responses={403: {"description": "Operation forbidden"}})
async def post_service(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the service: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.delete("/{id}", responses={403: {"description": "Operation forbidden"}})
async def delete_service(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the service: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


