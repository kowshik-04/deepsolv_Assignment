from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from typing import Optional


class Mongo:
    client: Optional[AsyncIOMotorClient] = None
    db = None


mongo = Mongo()


async def connect_to_mongo():
    mongo.client = AsyncIOMotorClient(settings.MONGO_URI)
    mongo.db = mongo.client[settings.DB_NAME]
    await _ensure_indexes()


async def close_mongo_connection():
    if mongo.client:
        mongo.client.close()


async def _ensure_indexes():
    # Pages: unique page_id; text search on name/industry
    await mongo.db.pages.create_index("page_id", unique=True)
    await mongo.db.pages.create_index([
        ("name", "text"),
        ("industry", "text")
    ])

    # Posts: filter/sort by page and date
    await mongo.db.posts.create_index([("page_id", 1), ("posted_at", -1)])
    await mongo.db.posts.create_index("post_id", unique=True)

    # Comments: by page/post
    await mongo.db.comments.create_index([("page_id", 1), ("post_id", 1), ("posted_at", -1)])

    # Employees: lookup by page
    await mongo.db.employees.create_index("page_id")

    # Followers/Following: by page + relation
    await mongo.db.followers.create_index([("page_id", 1), ("relation", 1)])
