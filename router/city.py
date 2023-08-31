from fastapi import APIRouter

from query.view.view_city import view_city
from query_elastic import create_index_if_not_exists, search_all_documents, get_document
from utility.decorator_limiter import rate_limit

router = APIRouter()


@router.get("/city/")
@rate_limit(limit=5, interval=300)
def get_list_city():
    return view_city()

