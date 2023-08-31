import uvicorn
if __name__ == '__main__':
    uvicorn.run('config:app', host='0.0.0.0', port=8000, reload=True)
    # uvicorn.run('config:app', host='127.0.0.1', port=8000, reload=True)
from celery_conf import celery_app
