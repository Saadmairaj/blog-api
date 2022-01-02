from typing import Optional
from api.models import Post
from api.database import Blog
from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

blog = Blog()
blog_router = APIRouter()


@blog_router.get("/ping", status_code=200)
def ping():
    """Checks for connection"""
    return {"success": True}


@blog_router.get("/posts", status_code=200)
async def get_data(
    tags: str = Query(None),
    sortBy: Optional[str] = Query("id"),
    direction: Optional[str] = Query("asc")
):
    """Returns blog posts from the given tags"""
    try:
        data = Post(
            tags=tags,
            sort_by=sortBy,
            direction=direction
        )
    except ValueError as e:
        return JSONResponse({"error": e.errors()[0]['msg']}, 400)

    return {"posts": await blog.get_posts(**data.dict())}
