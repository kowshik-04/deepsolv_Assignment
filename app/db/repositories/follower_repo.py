from app.db.mongo import mongo

class FollowerRepository:

    async def bulk_insert(self, followers: list):
        if followers:
            await mongo.db.followers.insert_many(followers)

    async def get_by_page(self, page_id: str, relation: str, skip: int, limit: int):
        query = {"page_id": page_id, "relation": relation}
        cursor = (
            mongo.db.followers
            .find(query)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
