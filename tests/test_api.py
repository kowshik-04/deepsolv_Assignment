import pytest
import httpx

from app.main import app
from app.api import pages as pages_api
from app.services.page_service import PageService
from app.db.repositories.page_repo import PageRepository
from app.db.repositories.post_repo import PostRepository
from app.db.repositories.employee_repo import EmployeeRepository
from app.db.repositories.comment_repo import CommentRepository
from app.db.repositories.follower_repo import FollowerRepository


@pytest.mark.anyio
async def test_get_page(monkeypatch):
    async def fake_get_or_scrape(self, page_id: str):
        return {"page_id": page_id, "name": "TestCo"}

    monkeypatch.setattr(PageService, "get_or_scrape_page", fake_get_or_scrape)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/pages/deepsolv")
        assert resp.status_code == 200
        assert resp.json()["page_id"] == "deepsolv"


@pytest.mark.anyio
async def test_search_pages(monkeypatch):
    async def fake_search(self, query: dict, skip: int, limit: int):
        # Ensure filters are applied
        assert query["followers"]["$gte"] == 1000
        assert query["followers"]["$lte"] == 5000
        assert "name" in query and "$regex" in query["name"]
        assert "industry" in query and "$regex" in query["industry"]
        return [{"page_id": "p1", "followers": 2000, "industry": "Software", "name": "Test"}]

    monkeypatch.setattr(PageRepository, "search", fake_search)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get(
            "/api/pages/search",
            params={"industry": "soft", "name": "test", "min_followers": 1000, "max_followers": 5000, "page": 1, "limit": 5},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert data[0]["page_id"] == "p1"


@pytest.mark.anyio
async def test_posts_pagination(monkeypatch):
    async def fake_get_recent(self, page_id: str, skip: int, limit: int):
        assert skip == 5
        assert limit == 5
        return [{"post_id": f"post_{i}", "page_id": page_id} for i in range(limit)]

    monkeypatch.setattr(PostRepository, "get_recent", fake_get_recent)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/pages/deepsolv/posts", params={"page": 2, "limit": 5})
        assert resp.status_code == 200
        assert len(resp.json()) == 5


@pytest.mark.anyio
async def test_employees_pagination(monkeypatch):
    async def fake_get_by_page(self, page_id: str, skip: int, limit: int):
        assert skip == 10
        assert limit == 10
        return [{"name": f"Emp{i}", "page_id": page_id} for i in range(limit)]

    monkeypatch.setattr(EmployeeRepository, "get_by_page", fake_get_by_page)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/pages/deepsolv/employees", params={"page": 2, "limit": 10})
        assert resp.status_code == 200
        assert len(resp.json()) == 10


@pytest.mark.anyio
async def test_comments_filter(monkeypatch):
    async def fake_get_by_page(self, page_id: str, skip: int, limit: int, post_id=None):
        assert post_id == "post_1"
        return [{"comment_id": "c1", "post_id": post_id, "page_id": page_id}]

    monkeypatch.setattr(CommentRepository, "get_by_page", fake_get_by_page)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get(
            "/api/pages/deepsolv/comments",
            params={"post_id": "post_1", "page": 1, "limit": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data[0]["post_id"] == "post_1"


@pytest.mark.anyio
async def test_followers_and_following(monkeypatch):
    async def fake_get_by_page(self, page_id: str, relation: str, skip: int, limit: int):
        assert relation in {"follower", "following"}
        return [{"profile_id": f"{relation}_1", "relation": relation, "page_id": page_id}]

    monkeypatch.setattr(FollowerRepository, "get_by_page", fake_get_by_page)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp1 = await client.get(
            "/api/pages/deepsolv/followers",
            params={"page": 1, "limit": 5},
        )
        resp2 = await client.get(
            "/api/pages/deepsolv/following",
            params={"page": 1, "limit": 5},
        )
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        assert resp1.json()[0]["relation"] == "follower"
        assert resp2.json()[0]["relation"] == "following"
