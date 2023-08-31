from celery import Celery

from query_elastic import create_documents, search_documents

celery_app = Celery("fast-lib", broker="amqp://guest:guest@rabbitmq:5672", backend="rpc://")
celery_app.autodiscover_tasks()


@celery_app.task(name="celery_conf.create_doc_task")
def create_doc_task(id, BookID, title, descriptions, price, genre_id, author_id, city_id):
    create_documents(id=id, BookID=BookID, title=title, descriptions=descriptions, price=price,
                     genre_id=genre_id, author_id=author_id, city_id=city_id)


@celery_app.task(name="celery_conf.search_documents_task")
def search_documents_task(index_name, per_page, page, must, should, sort):
    try:
        return search_documents(index_name, per_page, page, must, should, sort)
    except ValueError as e:
        return {"error": "does not exist"}
    # return 1 + 2
