from fastapi import APIRouter

from query.view.view_genre import view_gerne
from utility.decorator_limiter import rate_limit

router = APIRouter()

@router.get("/gerne/")
@rate_limit(limit=5, interval=300)
def get_list_gerne():
    return view_gerne()