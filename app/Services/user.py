
from http import HTTPStatus
import json
from app.Model.user import User
from app.queries import User as QUser
import bcrypt
from . import db_client
from edgedb import errors


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt())


def compare_password(hashed, password) -> bool:
    return bcrypt.checkpw(password, hashed)

query = QUser()

async def create_user(user: User):
    hashed_password = hash_password(user.password)
    try:
        await query.create(
            executor=db_client,
            email=user.email,
            name=user.name,
            password=hashed_password,
        )
    except errors.ClientConnectionError:
        raise HTTPStatus.SERVICE_UNAVAILABLE


async def login(email) -> User:
    try:
        result = User.model_validate_json(
            await query.retrieveUser(
                executor=db_client,
                email=email
                )
            )
        validate = compare_password(result.password, login.password)
        if not result:
            return HTTPStatus.NOT_FOUND
        elif not validate:
            return HTTPStatus.UNAUTHORIZED
        else:
            return result
    except errors.ClientConnectionError:
        raise HTTPStatus.SERVICE_UNAVAILABLE


async def update(user: User):
    try:
        userDB = query.update(
            executor=db_client,
            *user
            )
        
        return bool(userDB)
    except:
        raise _503


async def delete(id):
    pass

async def addBank(id, conta: Conta_Bancaria):
    pass


async def updateBank(id, conta: Conta_Bancaria):
    pass


async def deleteBank(id):
    """Deleta a conta de banco

    Args:
        id (Conta.id)
    """
    pass


async def saldo(id) -> json:
    """Recupera o saldo Bancario

    Args:
        id (User.id): _description_

    Returns:
        json
    """
    return retrieve_saldo.retrieve_saldo(id)