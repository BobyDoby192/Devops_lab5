from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    # Отправляем email, которого нет в списке users
    response = client.get("/api/v1/user", params={'email': 'unknown@mail.com'})
    # В роутере прописано: raise HTTPException(status_code=404, detail="User not found")
    assert response.status_code == 404[cite: 1]
    assert response.json() == {"detail": "User not found"}[cite: 1]

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user_data = {"name": "New User", "email": "new.user@mail.com"}
    response = client.post("/api/v1/user", json=new_user_data)
    # В роутере указан статус 201_CREATED и возвращается ID (int)
    assert response.status_code == 201[cite: 1]
    assert isinstance(response.json(), int)[cite: 1]

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    # Берем email первого существующего пользователя
    existing_user_data = {"name": "Duplicate", "email": users[0]['email']}
    response = client.post("/api/v1/user", json=existing_user_data)
    # В роутере прописано: raise HTTPException(status_code=409, detail="User with this email already exists")
    assert response.status_code == 409[cite: 1]
    assert response.json() == {"detail": "User with this email already exists"}[cite: 1]

def test_delete_user():
    '''Удаление пользователя'''
    # Удаляем пользователя, который есть в базе
    response = client.delete("/api/v1/user", params={'email': users[1]['email']})
    # В роутере указан статус 204_NO_CONTENT
    assert response.status_code == 204[cite: 1]
