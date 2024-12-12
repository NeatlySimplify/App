from faker import Faker
from fastapi.testclient import TestClient
from app.main import app
import pytest


fake = Faker("pt_BR")


@pytest.fixture
def test_client():
    return TestClient(
    app,
    raise_server_exceptions=True,
    root_path="",
    backend="asyncio",
    backend_options=None,
    cookies=None,
    headers=None,
    follow_redirects=True,
)


@pytest.fixture(scope="session")
def admin_uuid():
    admin = {
        "name": fake.name_male(),
        "email": fake.free_email(),
        "senha": fake.password(10, False, True, True)
    }
    return admin


@pytest.fixture(scope="session")
def common_user_uuid():
    user = {
        "name": fake.name_male(),
        "email": fake.free_email(),
        "senha": fake.password(10, False, True, True)
    }
    return user
