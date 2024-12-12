from . import *


class Service(BaseModel):
    user: str
    status: bool
    valor: float
    categoria: str
    details: str = ''


class Process(Service):
    fase: str
    classe: str
    tipo: str
    rito: str
    forum: str
    comarca: str
    vara: str