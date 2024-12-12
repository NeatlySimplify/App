from . import *
import json

# classe para log de ações.
class Auditable(BaseModel):
    user: str
    action: str
    details: json