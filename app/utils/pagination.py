def get_pagination(page: int, limit: int):
    page = max(page, 1)
    limit = min(max(limit, 1), 50)
    skip = (page - 1) * limit
    return skip, limit
