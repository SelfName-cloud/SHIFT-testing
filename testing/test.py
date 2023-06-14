from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from main import app, get_db
from temp.generate_data import GenData
from db.crud import create_user, create_salary_info
from db.schemas import UserCreate, SalaryInfoCreate
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

db = TestingSessionLocal()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def test_generate_data_length():

    gendata = GenData(10)

    assert len(gendata.data_user()) == 10
    assert len(gendata.data_salary()) == 10


def test_generate_data():

    gendata = GenData(1)

    assert type(gendata.data_user()[0]['user_login']) == str
    assert type(gendata.data_user()[0]['user_password']) == str
    assert gendata.data_user()[0]['email'].split('@')[1].split('.')[0] == 'example'

    assert gendata.data_salary()[0]['salary'] > 9999
    assert gendata.data_salary()[0]['salary'] < 200_001
    assert type(gendata.data_salary()[0]['date_raising']) == str


def test_add_data():

    gendata = GenData(100)

    data_users = gendata.data_user()
    data_salaries = gendata.data_salary()

    data_users.append({'user_login': 'login', 'user_password': 'password', 'email': 'password@mail.ru'})
    data_salaries.append({'salary': 20_000, 'date_raising': '2022-07-03'})

    for idx, (user, salary) in enumerate(zip(data_users, data_salaries)):
        user_schemas = UserCreate(user_login=user['user_login'], user_password=user['user_password'],
                                           email=user['email'])
        salary_schemas = SalaryInfoCreate(salary=salary['salary'], date_raising=salary['date_raising'])

        create_user(db=db, user=user_schemas)

        create_salary_info(db=db, salary=salary_schemas, user_id=idx+1)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user_404():
    response = client.post("/api/user", params={"login": "l", "password": "p"})
    assert response.status_code == 404


def test_create_user_200():
    response = client.post("/api/user", params={"login": 'login', "password": 'password'})
    assert response.status_code == 200
    assert type(json.loads(response.text)) == dict


def test_create_token_not_valid():
    response = client.post("/api/token", params={'token': '123'})
    assert response.status_code == 404


def test_create_token_valid():
    token = client.post("/api/user", params={"login": 'login', "password": 'password'})
    valid_token = json.loads(token.text)['token']
    response = client.post("/api/token", params={'token': valid_token})
    assert response.status_code == 200
    assert type(json.loads(response.text)) == dict


if __name__ == '__main__':
    test_generate_data_length()
    test_generate_data()
    test_add_data()
    test_create_user_404()
    test_create_user_200()
    test_create_token_not_valid()
    test_create_token_valid()