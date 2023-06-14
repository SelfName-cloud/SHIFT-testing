from sqlalchemy.orm import Session
from fastapi import Depends
from db.models import Base
from db.schemas import UserCreate, SalaryInfoCreate
from db.crud import create_user, create_salary_info
from db.database import SessionLocal, engine
from temp.generate_data import GenData

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_users(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


gendata = GenData(20)

data = gendata.data_user()

"""[{'user_login': 'nikita', 'user_password': 'nikita', 'email': 'nikita@mail.ru'},
        {'user_login': 'selfname', 'user_password': 'selfname', 'email': 'selfname@mail.ru'},
        {'user_login': 'ksenya', 'user_password': 'ksen2002', 'email': 'ksenya@mail.ru'},
        {'user_login': 'pavel', 'user_password': 'pasha', 'email': 'pavel@mail.ru'},
        {'user_login': 'alex', 'user_password': 'alexxx', 'email': 'alex@mail.ru'},
        {'user_login': 'login', 'user_password': 'password', 'email': 'login@mail.ru'},
        {'user_login': 'jack', 'user_password': 'jack2020', 'email': '2020@mail.ru'},
        {'user_login': 'natalya', 'user_password': 'nata', 'email': 'nata@mail.ru'},
        {'user_login': 'nikolay', 'user_password': 'kola', 'email': 'kols@mail.ru'},
        {'user_login': 'danil', 'user_password': 'danya', 'email': 'danya@mail.ru'}]"""

data_salary = gendata.data_salary()

""" [
    {'salary': '30000', 'date_raising': '12-09-2023'},
    {'salary': '50000', 'date_raising': '30-12-2022'},
    {'salary': '35000', 'date_raising': '01-01-2022'},
    {'salary': '56000', 'date_raising': '05-08-2023'},
    {'salary': '40000', 'date_raising': '04-05-2022'},
    {'salary': '34000', 'date_raising': '11-11-2023'},
    {'salary': '67000', 'date_raising': '06-05-2022'},
    {'salary': '46000', 'date_raising': '04-08-2021'},
    {'salary': '45000', 'date_raising': '02-07-2024'},
    {'salary': '40000', 'date_raising': '30-02-2025'}]"""

#users_id = [2, 1, 4, 5, 3, 7, 6, 9, 8, 10, 16, 19, 11, 20, 14, 15, 17, 18]

if __name__ == '__main__':
    if len(data) == len(data_salary):
        for user_data in data:
            print(user_data)
            user_data_schemas = UserCreate(user_login=user_data['user_login'], user_password=user_data['user_password'],
                                           email=user_data['email'])
            create_users(db=db, user=user_data_schemas)

        for idx, data_sal in enumerate(data_salary):
            salary_data_schemas = SalaryInfoCreate(salary=data_sal['salary'], date_raising=data_sal['date_raising'])
            print(data_sal)
            create_salary_info(db=db, salary=salary_data_schemas, user_id=idx+1)
    else:
        raise Exception('Check length data user and salary!')

