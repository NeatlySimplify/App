from . import *


router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_schedule():
    return 0


@router.get("/finance")
async def get_finance_schedule():
    return 0


@router.get("/service")
async def get_service_schedule():
    return 0


@router.get("/{id}")
async def read_schedule(id: str):
    if id not in fake_schedules_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_schedules_db[id]["name"], "id": id}


@router.put("/{id}", responses={403: {"description": "Operation forbidden"}})
async def update_schedule(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the schedule: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.post("/{id}", responses={403: {"description": "Operation forbidden"}})
async def post_schedule(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the schedule: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.delete("/{id}", responses={403: {"description": "Operation forbidden"}})
async def delete_schedule(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the schedule: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


