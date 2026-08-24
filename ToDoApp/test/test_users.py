from .utils import *
from  ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'vamsi163'
    assert response.json()['email'] == 'vamsidevarapalli2003@gmail.com'
    assert response.json()['first_name'] == 'Vamsi'
    assert response.json()['last_name'] == 'Devarapalli'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '1234567890'


def test_change_password_success(test_user):
    response_data = {
        'password': 'Vamsi1@2003',
        'new_password': 'vamsi1@2003',
    }
    response = client.put("/user/password", json=response_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response_data = {
        'password': 'Vamsi1@2004',
        'new_password': 'vamsi1@2003',
    }
    response = client.put("/user/password", json=response_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number/9876543219")
    assert response.status_code == status.HTTP_204_NO_CONTENT


