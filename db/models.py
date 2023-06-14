from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    user_login = Column(String, unique=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)

    dl = relationship('SalaryInfo', backref='owner', uselist=False)
    ti = relationship('Token')


class SalaryInfo(Base):

    __tablename__ = 'salary_info'

    salary_id = Column(Integer, primary_key=True, index=True)
    salary = Column(Float)
    date_raising = Column(String)

    user_id = Column(Integer(), ForeignKey('users.user_id'))


class Token(Base):

    __tablename__ = 'token'

    token_id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    time = Column(Float)
    user_id = Column(Integer, ForeignKey('users.user_id'))