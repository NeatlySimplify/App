from http import HTTPStatus
from urllib import response
from .conftest import common_user_uuid, test_client

client = test_client()

def test_get_register_route(client):
    response = client.get('/register')
    assert response.status_code == HTTPStatus.OK


def test_post_register(client):
    response = client.post('/register',
                            json={
                                'nome': common_user_uuid['name'],
                                'email': common_user_uuid['email'],
                                'senha': common_user_uuid['senha']
                            })
    assert response.status_code == HTTPStatus.CREATED


def test_get_login(client):
    response = client.post('/login')
    assert response.status_code == HTTPStatus.OK


def test_login(client):
    response = client.post('/login',
                            json={
                                'email': common_user_uuid['email'],
                                'senha': common_user_uuid['senha']
                            })
    assert response.status_code == HTTPStatus.OK


def test_add_bank_account(client):
    pass


def test_get_bank_account(client):
    pass


def test_update_bank_account(client):
    pass


def test_update_user(client):
    pass


def test_delete_user(client):
    pass

############################# END     ########################################


####################### tests on services route ##############################

def test_add_client(client):
    pass


def test_update_client(client):
    pass


def test_delete_client(client):
    pass

############################# END     ########################################


####################### tests on services route ##############################

############################# END     ########################################


####################### tests on transactions route ##########################

############################# END     ########################################


####################### tests on schedule route ##############################

############################# END     ########################################








def test_add_transaction(client):
    pass


