from bson import ObjectId
from datetime import datetime


def serialize_mongo(obj):
    """
    Recursively convert MongoDB objects into JSON-serializable formats.
    - ObjectId → str
    - datetime → ISO string
    """
    if isinstance(obj, list):
        return [serialize_mongo(item) for item in obj]

    if isinstance(obj, dict):
        return {
            key: serialize_mongo(value)
            for key, value in obj.items()
            if key != "_id"
        }

    if isinstance(obj, ObjectId):
        return str(obj)

    if isinstance(obj, datetime):
        return obj.isoformat()

    return obj
