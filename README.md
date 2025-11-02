## Current State Analysis

The backend is running with:
- FastAPI app with async routes (`/ping`, `/portfolio`)
- Async SQLAlchemy 2.0 using `sqlite+aiosqlite` and `AsyncSession`
- Schema managed by Alembic migrations (runtime Base.metadata.create_all disabled)
- Models: `User`, `Stock`, `PredictionHistory`, `ChatHistory`
- Alembic configured (sync URL) for migrations
- Decorators (`log_call`, `time_execution`) compatible with async

## Database migrations (Alembic)

Alembic is the migration tool for SQLAlchemy. It versions your database schema so you can upgrade/downgrade safely and keep all environments in sync.

### Workflow
1) Edit models in `models/*.py`.
2) Generate a migration from model changes:
```bash
uv run alembic revision --autogenerate -m "describe your change"
```
3) Review the generated script under `alembic/versions/`.
4) Apply the migration:
```bash
uv run alembic upgrade head
```
5) Roll back if needed:
```bash
uv run alembic downgrade -1
```

### Useful commands
```bash
uv run alembic current     # show current DB revision
uv run alembic history     # list migration history
uv run alembic stamp head  # mark DB as up-to-date (no changes applied)
```

### Notes
- Config: `alembic.ini` points to `sqlite:///./portfolio.db`.
- `alembic/env.py` loads `Base` and all models and enables:
  - `render_as_batch=True` (SQLite-friendly ALTER behavior)
  - `compare_type=True` (detect column type changes)
- Do not create tables at runtime; use Alembic migrations exclusively.

<!-- 2) Core CRUD APIs (async)
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
- Use `AsyncSession` + `await db.execute(select(...))` and Pydantic schemas for I/O. -->

<!-- 3) CORS configuration
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
``` -->

<!-- 4) Settings & environment
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
# Install dependencies
uv sync

# Run DB migrations
uv run alembic upgrade head

# Start server
uv run python main.py
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
