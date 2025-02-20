import pytest
from app import schemas
from jose import jwt
from app.config import settings



def test_login_user(test_user, client):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    response_data = response.json()
    
    # Adjust the response data to match the expected schema
    response_data['access_token'] = response_data.pop('token')
    
    login_response = schemas.Token(**response_data)
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200  # Check if the status code is 200 (OK)

# Test: Create a new user and verify the response
def test_create_user(client):
    # Send a POST request to create a new user
    response = client.post("/users/", json={"email": "user@gmail.com", "password": "123456"})
    
    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201  
    
    # Deserialize the response JSON into the ResponseUser schema
    new_user = schemas.ResponseUser(**response.json())
    
    # Check if the user's email matches the expected email
    assert new_user.email == "user@gmail.com"
    assert response.status_code == 201  # Check if the status code is 201 (Created)



import pytest

@pytest.mark.parametrize("email, password, status_code", [
    ("user@gmail.com", "wrongpassword", 403),  
    ("wrongeamil@gmail.com", "123456", 403),
    (None, "123456", 422),  # Missing email
    ("user@gmail.com", None, 422),  # Missing password
    (None, None, 422)  # Missing both
])
def test_incorrect_login(test_user, client, email, password, status_code):
    data = {}
    if email is not None:
        data["username"] = email
    if password is not None:
        data["password"] = password

    response = client.post("/login", data=data)
    assert response.status_code == status_code
