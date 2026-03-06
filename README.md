# Portfolio Project

A full-stack investment portfolio management and analysis platform with ML-powered stock price forecasting, benchmark comparison, and an AI fund manager chatbot.

## Features

- **Portfolio Management** — Add, edit, and track stock holdings with real-time portfolio value calculation, diversification pie charts, and automatic USD/INR currency detection.
- **Stock Price Forecasting** — Generate future price predictions using Facebook Prophet with configurable periods (1–365 days), confidence intervals, optional hyperparameter tuning, and model persistence.
- **Benchmark Comparison** — Compare portfolio performance against Nifty 50 over 1 week / 1 month / 1 year with return, outperformance, and volatility metrics.
- **AI Fund Manager** — Chat with a portfolio-aware AI advisor powered by Google Gemini that maintains conversational memory and delivers sector-based analysis.
- **Multi-User Support** — Create and manage multiple users with isolated portfolios, chat histories, and cascade deletes.

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python 3.13+, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic, Uvicorn |
| **Frontend** | React 19, TypeScript, Vite, Recharts, Axios |
| **ML / Data** | Facebook Prophet, pandas, NumPy, scikit-learn, yfinance |
| **AI** | Google Gemini (google-generativeai) |
| **Database** | SQLite (aiosqlite) |
| **Package Managers** | uv (Python), npm (Node.js) |

## Architecture

```
┌──────────────────────┐
│   React + TypeScript  │  :5173
│   (Vite)              │
└──────────┬───────────┘
           │ REST / JSON
┌──────────▼───────────┐
│   FastAPI (async)     │  :8000
│   Python 3.13+        │
└──────────┬───────────┘
           │
   ┌───────┼──────────┬──────────────┐
   │       │          │              │
┌──▼──┐ ┌──▼───┐ ┌────▼─────┐ ┌─────▼────┐
│SQLite│ │yfinance│ │ Gemini  │ │ Prophet  │
│  DB  │ │  API   │ │  API    │ │  Models  │
└──────┘ └───────┘ └─────────┘ └──────────┘
```

## Getting Started

### Prerequisites

- **Python** >= 3.13
- **Node.js** >= 18
- [**uv**](https://docs.astral.sh/uv/) — fast Python package manager
- A [Google Gemini API key](https://makersuite.google.com/app/apikey) (for the AI chat feature)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/portfolio-project.git
cd portfolio-project
```

### 2. Backend setup

```bash
# Install Python dependencies
uv sync

# Create your environment file
cp env.example .env
# Then edit .env and add your GEMINI_API_KEY

# Run database migrations
uv run alembic upgrade head

# Start the API server
uv run python main.py
```

The API will be available at **http://127.0.0.1:8000** with interactive docs at **/docs**.

### 3. Frontend setup

```bash
cd frontend

# Install Node dependencies
npm install

# (Optional) Override the API base URL
cp env.example .env

# Start the dev server
npm run dev
```

The dashboard will be available at **http://localhost:5173**.

## Environment Variables

### Backend (`.env` in project root)

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for the AI Fund Manager | Yes |
| `DATABASE_URL` | SQLAlchemy async DB URL (default: `sqlite+aiosqlite:///./portfolio.db`) | No |
| `FRONTEND_URL` | CORS allowed origin (default: `http://localhost:5173`) | No |

### Frontend (`frontend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users` | Create a new user |
| GET | `/api/users` | List all users |
| GET | `/api/users/{id}` | Get user by ID |
| PUT | `/api/users/{id}` | Update user |
| DELETE | `/api/users/{id}` | Delete user and all associated data |

### Stocks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/stocks` | Add a stock holding |
| GET | `/api/stocks` | List all stocks |
| GET | `/api/stocks/{id}` | Get stock by ID |
| PUT | `/api/stocks/{id}` | Update stock |
| DELETE | `/api/stocks/{id}` | Delete stock |

### Predictions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predictions/train` | Train a Prophet model for a symbol |
| POST | `/api/predictions/predict` | Generate future price predictions |
| GET | `/api/predictions/{symbol}` | Prediction history for a symbol |
| GET | `/api/predictions/{symbol}/latest` | Latest prediction |
| GET | `/api/predictions/models` | List saved models |
| DELETE | `/api/predictions/models/{symbol}` | Delete a saved model |

### Comparison

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/portfolio/{user_id}/comparison?period=1y` | Portfolio vs Nifty 50 (`1w`, `1m`, `1y`) |

### AI Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat?message=...&user_id=...` | Send a message to the AI Fund Manager |
| GET | `/api/chat/history/{user_id}` | Retrieve chat history |
| DELETE | `/api/chat/history/{user_id}` | Clear chat history |

## Project Structure

```
portfolio-project/
├── app/
│   ├── app.py                 # FastAPI routes and middleware
│   └── database.py            # Async SQLAlchemy engine and session
│
├── models/
│   ├── users.py               # User ORM model
│   ├── stocks.py              # Stock holdings ORM model
│   ├── prediction.py          # Prediction history ORM model
│   ├── chat_history.py        # Chat history ORM model
│   └── prophet/               # Prophet ML implementation
│       ├── prophet_model.py   # Model wrapper
│       ├── prophet_trainer.py # Training, validation, tuning
│       └── prophet_predictor.py # Forecasting
│
├── services/
│   ├── data_service.py        # Stock data fetching (yfinance)
│   ├── prediction_service.py  # Prediction persistence
│   ├── comparison_service.py  # Portfolio vs Nifty comparison
│   ├── gemini_service.py      # Gemini AI chat integration
│   └── model_service.py       # Model save / load / list
│
├── schemas/                   # Pydantic request/response schemas
│   ├── user.py
│   ├── stock.py
│   ├── prediction.py
│   ├── chat.py
│   └── comparison.py
│
├── utils/
│   ├── decorators.py          # Logging and timing decorators
│   ├── exceptions.py          # Custom exception classes
│   ├── validation.py          # Input validation helpers
│   └── metrics.py             # ML evaluation metrics
│
├── alembic/                   # Database migrations
│   ├── env.py
│   └── versions/
│
├── frontend/                  # React + TypeScript dashboard
│   ├── src/
│   │   ├── App.tsx            # Main app with tab navigation
│   │   ├── api/client.ts      # Axios API client
│   │   ├── components/
│   │   │   ├── AIChatInterface.tsx
│   │   │   ├── ComparisonChart.tsx
│   │   │   ├── PortfolioPieChart.tsx
│   │   │   ├── PredictionChart.tsx
│   │   │   └── StatCard.tsx
│   │   ├── hooks/
│   │   │   ├── usePortfolio.ts
│   │   │   └── usePrediction.ts
│   │   └── types/index.ts
│   ├── package.json
│   └── vite.config.ts
│
├── scripts/                   # Utility / seed scripts
├── main.py                    # Uvicorn entry point
├── pyproject.toml             # Python project metadata and dependencies
├── alembic.ini                # Alembic configuration
├── env.example                # Backend env template
└── .gitignore
```

## Database Migrations

Schema changes are managed exclusively through Alembic — tables are never created at runtime.

```bash
# Generate a new migration after editing models
uv run alembic revision --autogenerate -m "describe your change"

# Apply all pending migrations
uv run alembic upgrade head

# Roll back one migration
uv run alembic downgrade -1

# Show current revision
uv run alembic current
```

## License

This project is for educational and personal use.
