import requests
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine

index_name = "users"


def create_index_if_not_exists(index_name):
    response = requests.head(f"http://elasticsearch:9200/{index_name}")

    if response.status_code == 200:
        print(f"The index {index_name} already exists.")
        return
    elif response.status_code == 404:
        print(f"The index {index_name} does not exist.")
        response = requests.put(f"http://elasticsearch:9200/{index_name}")

        print(response.status_code)
        print(response.json())
        return
    else:
        print(f"An error occurred: {response.status_code}")
        return


def create_documents(id, BookID, title, descriptions, price, genre_id, author_id, city_id):
    create_index_if_not_exists(index_name)
    doc_body = {
        'BookID': BookID,
        'title': title,
        'descriptions': descriptions,
        'price': price,
        'city_id': city_id,
        'genre_id': genre_id,
        'author_id': author_id,
    }
    response = requests.post(f"http://elasticsearch:9200/{index_name}/_doc/{id}", json=doc_body)
    print(response.status_code)
    print(response.json())


def search_all_documents():
    doc = {
        "size": 1000,
        "query": {
            "match_all": {}
        }
    }

    response = requests.get(f"http://elasticsearch:9200/{index_name}/_search", json=doc)
    # print(response.status_code)
    # print(response.json()["hits"]["hits"])


def get_document(id: int) -> None:
    response = requests.get(f"http://elasticsearch:9200/{index_name}/_doc/{id}")
    print(response.status_code)
    print(response.json()["_source"])
    return response.json()["_source"]


def delete_document(id: int) -> None:
    response = requests.delete(f"http://elasticsearch:9200/{index_name}/_doc/{id}")
    print(response.status_code)
    print(response.json()["_source"])
    return response.json()["_source"]


def search_documents(index_name, per_page, page, must, should, sort):
    response = requests.get(f"http://elasticsearch:9200/{index_name}/_search/", json={
        "size": per_page,
        "from": (page - 1) * per_page,
        "query": {
            "bool": {
                "must": must,
                "should": should,
            }
        },
        "sort": sort,
    })

    ids = []

    for k in iter(response.json()['hits']['hits']):
        # print(50 * "===")
        ids.append(k["_source"]["BookID"])

    # print(50 * "===")

    with Session(bind=engine) as session:
        try:
            result = session.execute(text(
                "SELECT * FROM books WHERE id IN :id and is_active = TRUE and soft_delete = FALSE"), {"id": tuple(ids)})
            data = [
                {
                    "id": row.id,
                    "title": row.title,
                    "publication_date": row.publication_date,
                    "isbn": row.isbn,
                    "price": row.price,
                    "author_id": row.author_id,
                    "genre_id": row.genre_id,
                    "is_active": row.is_active,
                    "soft_delete": row.soft_delete,
                    "created_at": row.created_at,
                    "updated_at": row.updated_at,
                }
                for row in result
            ]
        except Exception as e:
            raise ValueError("does not exist")
    return {
        "total": response.json()['hits']['total']['value'],
        "data": data,
        "ttt": "tttt"
    }
