from http import HTTPStatus
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import functools
import edgedb
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
#from app.Routers import user

async def setup_edgedb(app: FastAPI):
    client = app.state = edgedb.create_async_client()
    await client.ensure_connected()


async def shutdown_edgedb(app: FastAPI):
    client, app.state = app.state, None
    await client.aclose()


# async def get_token_header(x_token: Annotated[str, Header()]):
#     if x_token != "fake-super-secret-token":
#         raise HTTPStatus.BAD_REQUEST


# async def get_query_token(token: str):
#     if token != "jessica":
#         raise HTTPStatus.BAD_REQUEST


app = FastAPI()

templates = Jinja2Templates(directory=f"./app/static/templates")

app.mount("/img", StaticFiles(directory="app/static/img"), name="img")


#app.add_event_handler("startup")(functools.partial(setup_edgedb, app))
#app.add_event_handler("shutdown")(functools.partial(shutdown_edgedb, app))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(user)

@app.get("/", response_class=HTMLResponse)
async def getDashBoard(request: Request):
    cards = {
        'row1': {
            'Clientes Registrados': 17,
            'Serviços Ativos': 8,
            'Saldo Atual': 'R$ 1507,89'
        },
        'row2': {
            'Entrada': {
                'Entrada Consolidada': 'R$ 107,89',
                'Entrada Prevista': 'R$ 1507,89' ,
            },
            'Saída': {
                'Saída Consolidada': 'R$ 107,89',
                'Saída Prevista': 'R$ 1507,89' ,
            },
            'Saldo do Mês': {
                'Saldo Consolidado': 'R$ 107,89',
                'Saldo Previsto': 'R$ 900,89' ,
            }
        }
    }
    sidebar = {
        'user': {
            'title': 'Usuário',
            'children': {
                'perfil': 'Perfil',
                'template': 'Templates',
                'logout': 'Logout'
            }
            
        },
        'clients' : {
            'title': 'Clientes',
            'children': {
                'pf':'Pessoa Física',
                'pj': 'Pessoa Jurídica'
                }
            },
        'services': {
            'title': 'Serviços',
            'children': {
                'investigation': 'Investigação',
                'process': 'Processos',
                'consult': 'Consultoria'
            }
        },
        'schedule': {
            'title': 'Agenda',
            'children': {
                'from_user': 'From User',
                'from_services': 'From Services',
                'from_action': 'From Actions' 
            }
        }
    }
    return templates.TemplateResponse(
        request=request,
        name='dashboard.html',
        context={
            'sidebar': sidebar,
            'card': cards
        }
    )




from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

app = FastAPI()

# Adding SessionMiddleware to manage sessions
app.add_middleware(SessionMiddleware, secret_key="your_secret_key", max_age=3600)

# Mock database for users
user_balances = {
    1: 1000,  # User 1
    2: 500    # User 2
}

# Dependency to get current user session
def get_current_user(request: Request):
    user_id = request.session.get('user_id')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not logged in"
        )
    return user_id

@app.post("/login")
async def login(user_id: int):
    if user_id in user_balances:
        # Store the user_id in session
        request.session['user_id'] = user_id
        return JSONResponse({"message": "Logged in successfully"})
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/update_balance")
async def update_balance(balance: int, user_id: int = Depends(get_current_user)):
    # Update balance for the logged-in user
    user_balances[user_id] = balance
    request.session['balance_updated'] = True
    return JSONResponse({"message": "Balance updated successfully"})

@app.get("/get_balance")
async def get_balance(user_id: int = Depends(get_current_user)):
    # Retrieve the balance for the current user
    balance = user_balances[user_id]
    balance_updated = request.session.get('balance_updated', False)
    
    if balance_updated:
        request.session['cached_balance'] = balance
        request.session['balance_updated'] = False  # Reset the flag
    
    return JSONResponse({"balance": request.session.get('cached_balance', balance)})

@app.post("/logout")
async def logout():
    # Clear session to logout the user
    request.session.clear()
    return JSONResponse({"message": "Logged out successfully"})

