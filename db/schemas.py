from pydantic import BaseModel


class SalaryInfoBase(BaseModel):
    salary: float
    date_raising: str


class SalaryInfoCreate(SalaryInfoBase):
    pass

    class Config:
        orm_mode = True


class SalaryInfo(SalaryInfoBase):
    salary_id: int
    user_id: int

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    token: str


class TokenCreate(TokenBase):
    time: int

    class Config:
        orm_mode = True


class Token(TokenBase):
    token_id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    user_login: str
    user_password: str


class UserCreate(UserBase):
    email: str


class User(UserBase):
    user_id: int
    salary_info: SalaryInfo
    token: Token

    class Config:
        orm_mode = True
