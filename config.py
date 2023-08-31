import datetime
import os
import time

from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from database.database import engine, Base
from router import book, city, genre, author

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library")

app.include_router(book.router, tags=['book'])
app.include_router(city.router, tags=['city'])
app.include_router(genre.router, tags=['genre'])
app.include_router(author.router, tags=['author'])



@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    print(request.client.host)
    ip = request.headers.get("x-forwarded-for")
    print(ip)
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
        log.write(70 * "=" + '\n')
        log.write(f'Application started at: {datetime.datetime.now()} \n')


@app.on_event('shutdown')
def shutdown_event():
    log_dir = 'logs'
    log_file = 'sever_time_log.log'
    log_path = os.path.join(log_dir, log_file)
    os.makedirs(log_dir, exist_ok=True)
    with open(log_path, 'a') as log:
        log.write(f'Application shutdown at: {datetime.datetime.now()} \n')
