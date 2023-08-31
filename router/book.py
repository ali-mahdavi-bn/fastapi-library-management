from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from celery_conf import create_doc_task, search_documents_task
from models.DBRB import BookReposetory
from query_elastic import index_name
from schemas.BaseResponse import BaseResponse
from schemas.BooksSchemas import BookCreate, BookUpdate
from utility.decorator_limiter import rate_limit
from utility.get_db import get_db
from utility.response import custom_response

router = APIRouter()


@router.post("/book/create/")
@rate_limit(limit=5, interval=300)
def create_book_api(book: BookCreate, db: Session = Depends(get_db)):
    try:

        book_reposetory = BookReposetory()
        book_reposetory.create(title=book.title, descriptions=book.descriptions, author_id=book.author_id,
                               genre_id=book.genre_id,
                               publication_date=book.publication_date,
                               isbn=book.isbn, price=book.price, is_active=book.is_active, soft_delete=book.soft_delete,
                               created_at=book.created_at, updated_at=book.updated_at)
        book_reposetory.add()
        response = book_reposetory.commit()
        data_for_elastic = response["data"][0]
        city = response["result"].author.city_id

        create_doc_task.apply_async(
            args=[data_for_elastic["id"], data_for_elastic["id"], data_for_elastic["title"],
                  data_for_elastic["descriptions"], data_for_elastic["price"], data_for_elastic["genre_id"],
                  data_for_elastic["author_id"], city],
            countdown=1)
        book_reposetory.refresh()
        return custom_response(data=response["data"], message="created Book Successful")
    except Exception as e:
        book_reposetory.session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error:{e}")
    except ValueError as e:
        book_reposetory.session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get("/book/{book_id}")
@rate_limit(limit=5, interval=300)
def get_book_api(book_id: int):
    book_reposetory = BookReposetory()
    try:
        return book_reposetory.reade(book_id)
    except Exception as e:
        raise HTTPException(detail=f"{e}", status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/book/{book_id}")
@rate_limit(limit=5, interval=300)
def update_book(book_id: int, book: BookUpdate):
    try:
        book_reposetory = BookReposetory()
        book_reposetory.get_book(book_id)
        book_reposetory.update(title=book.title, author_id=book.author_id, publication_date=book.publication_date,
                               isbn=book.isbn, price=book.price, is_active=book.is_active, soft_delete=book.soft_delete,
                               created_at=book.created_at, updated_at=book.updated_at)

        data = book_reposetory.commit()
        return data
    except SQLAlchemyError as e:
        book_reposetory.session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error:{e}")
    except ValueError as e:
        book_reposetory.session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.delete("/book/{book_id}")
@rate_limit(limit=5, interval=300)
def delete_borrowing_api(book_id: int):
    book_reposetory = BookReposetory()
    try:
        data = book_reposetory.get_book(book_id)
    except ValueError as e:
        book_reposetory.session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")

    book_reposetory.delete(data)
    book_reposetory.commit()
    response = BaseResponse(
        message={'field': '', 'message': 'deleted successfully'},
        data=[]
    )

    return response


@router.get("/book/list/")
@rate_limit(limit=5, interval=300)
def book_list_api():
    result = BookReposetory()
    # return result.list()


@router.get("/books/search/")
@rate_limit(limit=5, interval=300)
def search_books(
        q: str = Query(None, description="جستجو در عنوان و توضیحات کتاب"),
        price_range: str = Query(None, description="رنج قیمت (از-تا)"),
        genre_id: str = Query(None, description="ژانر"),
        city: int = Query(None, description="شهر   (با استفاده از id)"),
        page: int = Query(1, description="شماره صفحه"),
        per_page: int = Query(10, description="تعداد آیتم ها در هر صفحه")
):
    must = []
    should = []
    sort = []
    if price_range:
        price_from, price_to = price_range.split("-")
        must.append({"range": {"price": {"gte": price_from, "lte": price_to}}})
    if genre_id:
        should.append({"match": {"genre_id": genre_id}})
    if city:
        must.append({"term": {"city_id": city}})
    if q:
        must.append({"match_phrase": {"title": {"query": q}}})
        should.append({"match_phrase": {"description": {"query": q}}})
    sort.append({"price": {"order": "asc"}})
    try:
        result = search_documents_task.delay(index_name, per_page, page, must, should, sort)
        data = result.get()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")

    try:
        res_data = data["data"]
        return custom_response(data=res_data, message="Success")
    except Exception as e:
        error = data["error"]
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{error}")
