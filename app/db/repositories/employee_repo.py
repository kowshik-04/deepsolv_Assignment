from app.db.mongo import mongo

class EmployeeRepository:

    async def bulk_insert(self, employees: list):
        if employees:
            await mongo.db.employees.insert_many(employees)

    async def get_by_page(self, page_id: str, skip: int, limit: int):
        cursor = (
            mongo.db.employees
            .find({"page_id": page_id})
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
