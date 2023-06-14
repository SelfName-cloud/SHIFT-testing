from sqlalchemy.orm import Session
from . import models, schemas
import hashlib


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_login_and_password(db: Session, login: str, password: str):
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    return db.query(models.User).filter(models.User.user_login == login or models.User.hashed_password == hashed_password).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashlib.sha512(user.user_password.encode()).hexdigest()
    db_user = models.User(user_login=user.user_login, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_salary_info(db: Session, salary_id: int):
    return db.query(models.SalaryInfo).filter(models.SalaryInfo.salary_id == salary_id).first()


def get_salary_info_by_user_id(db: Session, user_id: int):
    return db.query(models.SalaryInfo).filter(models.SalaryInfo.user_id == user_id).first()


def create_salary_info(db: Session, salary: schemas.SalaryInfoCreate, user_id: int):
    db_salary = models.SalaryInfo(**salary.dict(), user_id=user_id)
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


def get_token_by_token(db: Session, token: str):
    return db.query(models.Token).filter(models.Token.token == token).first()


def get_token_by_token_id(db: Session, token_id: int):
    return db.query(models.Token).filter(models.Token.token_id == token_id).first()


def get_token_by_user_id(db: Session, user_id: int):
    return db.query(models.Token).filter(models.Token.user_id == user_id).first()


def create_token(db: Session, token: schemas.TokenCreate, time: float, user_id: int):
    db_token = models.Token(token=token, time=time, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def delete_token(db: Session, token_id: int):
    return db.query(models.Token).filter(models.Token.token_id == token_id).delete()


def delete_token_by_token(db: Session, token: str):
    return db.query(models.Token).filter(models.Token.token == token).delete()