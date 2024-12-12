import edgedb
from fastapi import Request

def db_client(request: Request) -> edgedb.AsyncIOClient:
    return request.app.state