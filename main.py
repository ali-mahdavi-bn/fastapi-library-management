import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from models.Model import User
from schemas import UserSchemas as schemas
from utility.get_db import get_db


if __name__ == '__main__':
    # uvicorn.run('config:app', host='0.0.0.0', port=8000, reload=True)
    uvicorn.run('config:app', host='127.0.0.1', port=8003, reload=True)
