from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from secrets import token_hex

from db import crud, schemas
from db.database import SessionLocal
import time

app = FastAPI(debug=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/user", response_model=schemas.TokenBase)
def read_user(login: str, password: str, db: Session = Depends(get_db)): #Depends(get_db)
    db_user = crud.get_user_by_login_and_password(db, login=login, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    token = token_hex(20)
    start_time = time.time()
    crud.create_token(db=db, token=token, time=start_time, user_id=db_user.user_id)
    return {'token': token}


@app.post("/api/token", response_model=schemas.SalaryInfo)
def read_token(token: str, db: Session = Depends(get_db)):
    db_token = crud.get_token_by_token(db=db, token=token)
    if db_token is None:
        raise HTTPException(status_code=404, detail="Token don`t find")
    end_time = time.time()
    if (end_time - db_token.time) > 180:
        crud.delete_token_by_token(db=db, token=token)
        raise HTTPException(status_code=404, detail="Token don`t activate")
    return crud.get_salary_info_by_user_id(db=db, user_id=db_token.user_id)

