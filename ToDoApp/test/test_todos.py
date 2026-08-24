
from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'description': 'Need to learn everyday', 'id': 1, 'owner_id': 1, 'priority': 5, 'title': 'Learn to code!'}] 


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == 200
    assert response.json() == {'complete': False, 'description': 'Need to learn everyday', 'id': 1, 'owner_id': 1, 'priority': 5, 'title': 'Learn to code!'}


def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}


def test_create_todo(test_todo):
    response_data = {
        'title': 'New Todo',
        'description': 'This is a new todo',    
        'priority': 3,
        'complete': False
    }
    response = client.post("/todos/todo/", json=response_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == response_data.get('title')
    assert model.description == response_data.get('description')
    assert model.priority == response_data.get('priority')
    assert model.complete == response_data.get('complete')


def test_update_todo(test_todo):
    response_data = {
        'title': 'Updated Todo',
        'description': 'This is an updated todo',    
        'priority': 4,
        'complete': True
    }
    response = client.put("/todos/todo/1", json=response_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Updated Todo'

def test_update_todo_not_found():
    response_data = {
        'title': 'Updated Todo',
        'description': 'This is an updated todo',    
        'priority': 4,
        'complete': True
    }
    response = client.put("/todos/todo/999", json=response_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}


def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}
  