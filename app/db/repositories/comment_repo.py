from typing import Optional

from app.db.mongo import mongo


class CommentRepository:

    async def bulk_insert(self, comments: list):
        if comments:
            await mongo.db.comments.insert_many(comments)

    async def get_by_page(self, page_id: str, skip: int, limit: int, post_id: Optional[str] = None):
        query = {"page_id": page_id}
        if post_id:
            query["post_id"] = post_id
        cursor = (
            mongo.db.comments
            .find(query)
            .sort("posted_at", -1)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
