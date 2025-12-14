from app.db.repositories.page_repo import PageRepository
from app.db.repositories.post_repo import PostRepository
from app.db.repositories.employee_repo import EmployeeRepository
from app.db.repositories.comment_repo import CommentRepository
from app.db.repositories.follower_repo import FollowerRepository
from app.services.scraper_service import LinkedInScraperService
from app.services.ai_service import AIService
from app.core.cache import get_cache, set_cache
from app.utils.mongo_serializer import serialize_mongo


class PageService:
    """
    Handles Page-related business logic:
    - Fetch from cache / DB
    - Scrape if missing
    - Serialize Mongo objects safely
    - Generate AI insights
    """

    def __init__(self):
        self.page_repo = PageRepository()
        self.post_repo = PostRepository()
        self.employee_repo = EmployeeRepository()
        self.comment_repo = CommentRepository()
        self.follower_repo = FollowerRepository()
        self.scraper = LinkedInScraperService()

    async def get_or_scrape_page(self, page_id: str):
        """
        Fetch page from cache → DB → scrape (fallback).
        Always returns JSON-serializable data.
        """
        cache_key = f"page:{page_id}"

        # 1️⃣ Check Redis cache
        cached = await get_cache(cache_key)
        if cached:
            return cached

        page = await self.page_repo.get_by_page_id(page_id)
        if page:
            serialized = serialize_mongo(page)
            await set_cache(cache_key, serialized)
            return serialized

        scraped = await self.scraper.scrape_page(page_id)

        await self.page_repo.create(scraped)
        await self.post_repo.bulk_insert(scraped.get("posts", []))
        await self.employee_repo.bulk_insert(scraped.get("employees", []))
        await self.comment_repo.bulk_insert(scraped.get("comments", []))
        await self.follower_repo.bulk_insert(scraped.get("followers_list", []))
        await self.follower_repo.bulk_insert(scraped.get("following_list", []))

        serialized = serialize_mongo(scraped)

        await set_cache(cache_key, serialized)
        return serialized

    async def get_ai_insights(self, page_id: str):
        
        cache_key = f"ai_insights:{page_id}"

        cached = await get_cache(cache_key)
        if cached:
            return cached

        page = await self.page_repo.get_by_page_id(page_id)
        if not page:
            raise ValueError("Page not found. Fetch page first.")

        serialized_page = serialize_mongo(page)

        ai_service = AIService()
        insights = await ai_service.generate_page_insights(serialized_page)

        await set_cache(cache_key, insights)

        return insights
