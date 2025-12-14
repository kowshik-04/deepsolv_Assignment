from fastapi import APIRouter
from typing import Optional

from app.services.page_service import PageService
from app.db.repositories.page_repo import PageRepository
from app.db.repositories.post_repo import PostRepository
from app.db.repositories.employee_repo import EmployeeRepository
from app.db.repositories.comment_repo import CommentRepository
from app.db.repositories.follower_repo import FollowerRepository
from app.utils.pagination import get_pagination
from app.utils.mongo_serializer import serialize_mongo

router = APIRouter()


# ✅ STATIC ROUTES FIRST
@router.get("/pages/search")
async def search_pages(
    industry: Optional[str] = None,
    name: Optional[str] = None,
    min_followers: int = 0,
    max_followers: int = 1_000_000,
    page: int = 1,
    limit: int = 10,
):
    query = {"followers": {"$gte": min_followers, "$lte": max_followers}}
    if industry:
        query["industry"] = {"$regex": industry, "$options": "i"}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    skip, limit = get_pagination(page, limit)
    pages = await PageRepository().search(query, skip, limit)
    return serialize_mongo(pages)


@router.get("/pages/{page_id}/posts")
async def get_posts(page_id: str, page: int = 1, limit: int = 15):
    skip, limit = get_pagination(page, limit)
    posts = await PostRepository().get_recent(page_id, skip, limit)
    return serialize_mongo(posts)


@router.get("/pages/{page_id}/employees")
async def get_employees(page_id: str, page: int = 1, limit: int = 20):
    skip, limit = get_pagination(page, limit)
    employees = await EmployeeRepository().get_by_page(page_id, skip, limit)
    return serialize_mongo(employees)


@router.get("/pages/{page_id}/comments")
async def get_comments(page_id: str, post_id: Optional[str] = None, page: int = 1, limit: int = 20):
    skip, limit = get_pagination(page, limit)
    comments = await CommentRepository().get_by_page(page_id, skip, limit, post_id=post_id)
    return serialize_mongo(comments)


@router.get("/pages/{page_id}/followers")
async def get_followers(page_id: str, page: int = 1, limit: int = 25):
    skip, limit = get_pagination(page, limit)
    followers = await FollowerRepository().get_by_page(page_id, relation="follower", skip=skip, limit=limit)
    return serialize_mongo(followers)


@router.get("/pages/{page_id}/following")
async def get_following(page_id: str, page: int = 1, limit: int = 25):
    skip, limit = get_pagination(page, limit)
    following = await FollowerRepository().get_by_page(page_id, relation="following", skip=skip, limit=limit)
    return serialize_mongo(following)


@router.get("/pages/{page_id}/ai-insights")
async def get_ai_insights(page_id: str):
    return await PageService().get_ai_insights(page_id)


# ✅ DYNAMIC ROUTE LAST
@router.get("/pages/{page_id}")
async def get_page(page_id: str):
    return await PageService().get_or_scrape_page(page_id)
