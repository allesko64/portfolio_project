## Current State Analysis

The backend is running with:
- FastAPI app with async routes (`/ping`, `/portfolio`)
- Async SQLAlchemy 2.0 using `sqlite+aiosqlite` and `AsyncSession`
- Tables auto-created on startup via FastAPI lifespan handler
- Models: `User`, `Stock`, `PredictionHistory`, `ChatHistory`
- Alembic configured (sync URL) for migrations
- Decorators (`log_call`, `time_execution`) compatible with async

## Next Steps (Short-term)

1) Database migrations (Alembic)
- Create the initial migration and apply it:
```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
- Commit the generated versions under `alembic/versions`.

2) Core CRUD APIs (async)
- Users:
  - POST /api/users
  - GET /api/users
  - GET /api/users/{id}
  - PUT /api/users/{id}
  - DELETE /api/users/{id}
- Stocks:
  - POST /api/portfolio/stock
  - GET /api/portfolio
  - GET /api/portfolio/stock/{id}
  - PUT /api/portfolio/stock/{id}
  - DELETE /api/portfolio/stock/{id}
- Use `AsyncSession` + `await db.execute(select(...))` and Pydantic schemas for I/O.

3) CORS configuration
- Allow local frontend origin(s):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

4) Settings & environment
- Add `.env` (DB URL, CORS origins, API keys if needed).
- Create `config.py` using `pydantic-settings` to load env.

5) Testing
- Add pytest and an async test client:
```bash
pip install pytest pytest-asyncio httpx
```
- Write smoke tests for `/ping`, `/portfolio`, and one CRUD flow.

6) CI (GitHub Actions)
- Add a workflow to run `pip install`, `pytest`, and (optionally) `ruff`/`black` on every PR.

## How to Run (Backend)

```bash
python -m venv .venv
. .venv/Scripts/activate     # Windows (PowerShell) or source .venv/bin/activate on Unix
pip install fastapi uvicorn sqlalchemy aiosqlite alembic pydantic pydantic-settings

# Run DB migrations
alembic upgrade head

# Start server
python main.py
# App: http://127.0.0.1:8000  |  Docs: http://127.0.0.1:8000/docs
```

## Long-term Roadmap (Precise)

- AI Predictions: Prophet, LSTM, ARIMA, and an ensemble with backtesting and accuracy tracking.
- Background Jobs: Daily retraining and data refresh via APScheduler/Celery; model registry and caching.
- Chatbot RAG: LangChain + ChromaDB, local embeddings, Ollama/OpenAI LLMs, portfolio-aware answers.
- Frontend App: React + TypeScript dashboard (portfolio, stock details, predictions, chatbot widget).
- Auth & Multi-user: JWT-based auth, roles/permissions, rate limiting, per-user portfolios.
- Observability: Structured logging, metrics, tracing; error reporting (e.g., Sentry).
- Deployment: Docker/docker-compose, optional Kubernetes; CI/CD pipeline with tests and lint gates.
- Performance & Security: Redis caching, DB indexes/pagination, strict validation, secure headers, CORS hardening.
