from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Todos, Users
from ..routers.auth import bcrypt_context
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest




SQLALCHEMY_DATABASE_URI = 'sqlite:///./testdb.db' 

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()    

def override_get_current_user():
    return {'username': 'vamsi163', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title  ="Learn to code!",
        description = "Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username = "vamsi163",
        email = "vamsidevarapalli2003@gmail.com",
        first_name = "Vamsi",
        last_name = "Devarapalli",
        hashed_password = bcrypt_context.hash("Vamsi1@2003"),
        role = "admin",
        phone_number = "1234567890",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
