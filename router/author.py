from fastapi import APIRouter

from query.view.view_author import view_author
from utility.decorator_limiter import rate_limit

router = APIRouter()


@router.get("/author/")
@rate_limit(limit=5, interval=300)
def get_list_author():
    return view_author()
