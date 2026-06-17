import pytest
from playwright.sync_api import APIRequestContext
from faker import Faker

faker = Faker()

def test_api_ping(api_client: APIRequestContext):
    """
    Завдання 2: Перший E2E тест
    Перевіряє, чи відповідає сервер на запит пінгу.
    """
    response = api_client.get("/app/ping")
    assert response.ok
    assert response.status == 200
    assert response.json() == {"text": "app is working"}


def test_full_business_workflow(api_client: APIRequestContext):
    """
    Завдання 4: Тестування бізнес-процесу
    Повний сценарій: Реєстрація -> Авторизація -> Створення завдання -> Перевірка списку завдань.
    """
    # 1. Генерація унікальних даних для користувача
    username = f"e2e_user_{faker.random_int(min=10000, max=99999)}"
    password = "e2e_secure_password"
    
    # 2. Реєстрація нового користувача
    register_payload = {
        "username": username,
        "password": password
    }
    register_response = api_client.post("/user", data=register_payload)
    assert register_response.ok, f"Register failed: {register_response.text()}"
    register_data = register_response.json()
    assert "access_token" in register_data
    assert "user_id" in register_data
    
    # 3. Авторизація (Вхід) для отримання токену
    login_payload = {
        "username": username,
        "password": password
    }
    login_response = api_client.post("/auth/login", data=login_payload)
    assert login_response.ok, f"Login failed: {login_response.text()}"
    login_data = login_response.json()
    access_token = login_data["access_token"]
    assert access_token is not None
    
    # 4. Створення нового завдання за допомогою отриманого JWT-токену
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    task_payload = {
        "name": "Playwright E2E Task",
        "pomodoro_count": 3,
        "category_id": 1
    }
    create_task_response = api_client.post("/task/", data=task_payload, headers=headers)
    assert create_task_response.ok, f"Create task failed: {create_task_response.text()}"
    task_data = create_task_response.json()
    assert task_data["name"] == "Playwright E2E Task"
    assert task_data["pomodoro_count"] == 3
    assert task_data["category_id"] == 1
    assert "id" in task_data
    
    # 5. Отримання списку завдань та перевірка наявності створеного завдання
    get_tasks_response = api_client.get("/task/all", headers=headers)
    assert get_tasks_response.ok, f"Get tasks failed: {get_tasks_response.text()}"
    tasks_list = get_tasks_response.json()
    
    # Перевіряємо, що наше завдання є у повернутому списку
    task_ids = [t["id"] for t in tasks_list]
    assert task_data["id"] in task_ids
