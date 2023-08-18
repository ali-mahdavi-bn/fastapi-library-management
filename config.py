import datetime
import os
import time

from fastapi import FastAPI

from auth import auth_handler
from database.database import engine, Base
from router import users, books, authors, borrowing

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router, tags=['users'])
app.include_router(books.router, tags=['books'])
app.include_router(authors.router, tags=['author'])
app.include_router(borrowing.router, tags=['borrowing'])
app.include_router(auth_handler.router, tags=['tocken'])


@app.middleware('http')
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.on_event('startup')
def startup_event():
    log_dir = 'logs'
    log_file = 'sever_time_log.log'
    log_path = os.path.join(log_dir, log_file)

    os.makedirs(log_dir, exist_ok=True)
    with open(log_path, 'a') as log:
        log.write(70*"=" + '\n')
        log.write(f'Application started at: {datetime.datetime.now()} \n')


@app.on_event('shutdown')
def shutdown_event():
    log_dir = 'logs'
    log_file = 'sever_time_log.log'
    log_path = os.path.join(log_dir, log_file)
    os.makedirs(log_dir, exist_ok=True)
    with open(log_path, 'a') as log:
        log.write(f'Application shutdown at: {datetime.datetime.now()} \n')
