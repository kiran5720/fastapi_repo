from app  import schemas,oauth2
from .data_base import client,session
from jose import jwt
import pytest
from app.config import settings    


def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') ==  'Hello byddy go learn from mistakeeeeeeee'
    assert res.status_code == 200
    # return {"mesage"}

def test_create_user(client):
    res = client.post("/users/",json={ "email":"bcb@gmail.com",
    "password":"kiran123"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == "bcb@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login",
                      data={ "username":test_user['email'],"password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    print(res.json())
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "pass123", 403),
    ("bcb@gmail.com", "wrongpassword", 403),
    (None, "pass123", 403)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login",
                      data={"username": email, "password": password})

    assert res.status_code == status_code


