from app.db.mongo import mongo

class PostRepository:

    async def bulk_insert(self, posts: list):
        if posts:
            await mongo.db.posts.insert_many(posts)

    async def get_recent(self, page_id: str, skip: int, limit: int):
        cursor = (
            mongo.db.posts
            .find({"page_id": page_id})
            .sort("posted_at", -1)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
