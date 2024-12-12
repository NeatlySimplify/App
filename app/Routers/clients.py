from . import *


router = APIRouter(
    prefix="/client",
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
async def get_template_page(template_page: str, request: Request):
    return template.TemplateResponse(f"{template_page}", {"request": request})


@router.get("/pf")
async def get_pf_clients():
    return 0


@router.get("/pj")
async def get_pj_clients():
    return 0


@router.get("/{id}")
async def read_client(id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put("/{id}", responses={403: {"description": "Operation forbidden"}})
async def update_client(id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


@router.post("/{id}", responses={403: {"description": "Operation forbidden"}})
async def post_client(id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


@router.delete("/{id}", responses={403: {"description": "Operation forbidden"}})
async def delete_client(id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
