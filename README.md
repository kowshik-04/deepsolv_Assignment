LinkedIn Insights Microservice

A production-grade FastAPI + MongoDB + Redis + OpenAI backend that scrapes, stores, analyzes, and serves insights for LinkedIn company pages. Built with clean architecture, async I/O, caching, and an optional AI enrichment layer.

## Highlights
- Scrape LinkedIn company pages by Page ID; persist companies, posts (15–25 recent), and employees.
- RESTful APIs with pagination, filters, and OpenAPI docs.
- Async-first stack (FastAPI, Motor) with Redis cache (300s TTL) to reduce scraping and AI calls.
- AI-generated business insights via OpenAI, returned as structured JSON.
- Dockerized for quick runs; cloud-storage abstraction ready for S3/GCS/MinIO.

## Architecture
- Client
  -> FastAPI routes
  -> Service layer (business logic)
  -> Repository layer (MongoDB)
  -> MongoDB / Redis
- Services encapsulate scraping and AI; repositories isolate DB access; cache sits in front of expensive calls.

## Tech Stack
| Layer | Technology |
| --- | --- |
| Framework | FastAPI |
| Language | Python 3.9 |
| Database | MongoDB (Motor async) |
| Cache | Redis |
| AI | OpenAI (ChatGPT) |
| Container | Docker |
| Docs | Swagger / OpenAPI |

## Project Structure
```
linkedin-insights/
├── app/
│   ├── api/
│   │   └── pages.py
│   ├── core/
│   │   ├── cache.py
│   │   └── dependencies.py
│   ├── db/
│   │   ├── mongo.py
│   │   └── repositories/
│   │       ├── page_repo.py
│   │       ├── post_repo.py
│   │       ├── employee_repo.py
│   │       ├── comment_repo.py
│   │       └── follower_repo.py
│   ├── models/
│   │   ├── page.py
│   │   ├── post.py
│   │   ├── employee.py
│   │   ├── comment.py
│   │   └── follower.py
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── page_service.py
│   │   ├── scraper_service.py
│   │   └── storage_service.py
│   ├── utils/
│   │   └── pagination.py
│   ├── config.py
│   └── main.py
├── postman/
│   └── LinkedIn-Insights.postman_collection.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Prerequisites
- Python 3.9+
- MongoDB and Redis running locally (or reachable URIs)
- OpenAI API key
- Docker (optional, for containerized runs)

## Environment Variables
Set via `.env` or shell exports:

| Name | Description | Example |
| --- | --- | --- |
| MONGO_URI | Mongo connection string | mongodb://localhost:27017 |
| REDIS_URL | Redis connection string | redis://localhost:6379 |
| OPENAI_API_KEY | OpenAI API key | sk-xxxx |

## Run Locally (without Docker)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Docker
```bash
docker build -t linkedin-insights-backend .
docker run -p 8000:8000 --env-file .env linkedin-insights-backend
```
Docs available at http://localhost:8000/docs.

### Docker Compose (Mongo + Redis + App)
```bash
docker compose up --build
# or detach
docker compose up -d --build
```
Services: FastAPI on 8000, Mongo on 27017, Redis on 6379. Provide your .env so the app can start.

### Postman Collection
Import postman/LinkedIn-Insights.postman_collection.json. Base URL defaults to http://localhost:8000; override base_url variable as needed.

## API Endpoints (summary)
- GET /api/pages/{page_id}: Fetch or scrape a page; persists if missing.
- GET /api/pages/search?industry=&min_followers=&max_followers=&page=&limit=: Filtered search with pagination.
- GET /api/pages/{page_id}/posts?page=&limit=: Recent posts (paginated).
- GET /api/pages/{page_id}/employees?page=&limit=: Employees linked to the page (paginated).
- GET /api/pages/{page_id}/comments?post_id=&page=&limit=: Comments (optionally filter by post; paginated).
- GET /api/pages/{page_id}/followers?page=&limit=: Followers list (paginated).
- GET /api/pages/{page_id}/following?page=&limit=: Following list (paginated).
- GET /api/pages/{page_id}/ai-insights: AI-generated JSON insights (followers, headcount, industry, description, specialties, engagement signals).

## Caching
- Redis caches page details, search results, and AI insights.
- Default TTL: 300 seconds.
- Cuts scraping overhead, DB load, and OpenAI cost.

## AI Insights
- Uses OpenAI to produce structured business insights: positioning, maturity, hiring signals, growth indicators, and recommendations.
- Responses are valid JSON for frontend or analytics consumption.

## Notes on Scraping
- Individual employee profile URLs are not scraped; employees are linked to the company People page to respect LinkedIn ToS.

## Design Decisions
- Async-first for I/O bound work.
- Service–Repository separation for testability and clarity.
- Cache-first reads where applicable; AI is additive, not required for core flows.
- Cloud-ready storage abstraction; credentials intentionally omitted.

## Status
| Requirement | Status |
| --- | --- |
| Mandatory requirements | Completed |
| AI integration | Completed |
| Caching | Completed |
| Async programming | Completed |
| Cloud storage | Architected |
| Docker | Completed |

## Author
Rama Naga Kowshik Mente — Backend / AI Engineer
