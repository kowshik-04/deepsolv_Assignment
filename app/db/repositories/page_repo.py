from app.db.mongo import mongo

class PageRepository:

    async def get_by_page_id(self, page_id: str):
        return await mongo.db.pages.find_one({"page_id": page_id})

    async def create(self, page: dict):
        await mongo.db.pages.insert_one(page)

    async def search(self, query: dict, skip: int, limit: int):
        cursor = mongo.db.pages.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
