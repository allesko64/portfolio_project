# Full Stack Stock Portfolio with AI Predictions & Chatbot

## Current State Analysis

The project has a basic FastAPI backend with:

- `Stock` class: Represents individual stocks with name, buy_price, and quantity
- `Portfolio` class: Manages a collection of stocks (add, delete, get all, total value)
- Two endpoints: `/ping` (health check) and `/portfolio` (returns all stocks)
- Custom decorators for logging and timing execution
- No database persistence (in-memory only)
- No frontend
- No AI/ML capabilities

## Implementation Plan

### Phase 1: Backend Enhancement - Database & Core APIs

**1.1 Database Layer (SQLite)**

- Create `models/` directory with SQLAlchemy ORM models:
  - `Stock` model: id, name, symbol, buy_price, quantity, purchase_date, user_id
  - `User` model: id, username, email (for future multi-user support)
  - `PredictionHistory` model: id, stock_symbol, predicted_date, predicted_price, model_used, created_at
  - `ChatHistory` model: id, user_id, message, response, timestamp
- Create `database.py` for database connection and session management
- Add Alembic for database migrations
- Update `Portfolio` class to work with database operations

**1.2 Stock Data Integration**

- Create `services/stock_data_service.py`:
  - Integrate with yfinance API for real-time stock data
  - Fetch historical stock prices (for training ML models)
  - Get current market prices
  - Functions: `get_stock_history()`, `get_current_price()`, `validate_stock_symbol()`

**1.3 REST API Endpoints**

Extend `app.py` with comprehensive endpoints:

- Portfolio Management:
  - `POST /api/portfolio/stock` - Add stock to portfolio
  - `DELETE /api/portfolio/stock/{id}` - Remove stock
  - `GET /api/portfolio` - Get all stocks with current values
  - `GET /api/portfolio/total` - Get total portfolio value
  - `PUT /api/portfolio/stock/{id}` - Update stock details
- Stock Data:
  - `GET /api/stocks/search/{symbol}` - Search/validate stock symbol
  - `GET /api/stocks/{symbol}/history` - Get historical data
  - `GET /api/stocks/{symbol}/current` - Get current price

**1.4 CORS Configuration**

- Add CORS middleware to allow React frontend communication
- Configure allowed origins for local development

### Phase 2: AI/ML - Trend Prediction Models

**2.1 Model Infrastructure**

Create `ml_models/` directory structure:

- `base_predictor.py` - Abstract base class for all prediction models
- `prophet_predictor.py` - Facebook Prophet time-series model
- `lstm_predictor.py` - LSTM neural network model
- `statistical_predictor.py` - Moving averages, linear regression, ARIMA
- `ensemble_predictor.py` - Combines predictions from all models
- `model_trainer.py` - Training and retraining logic
- `model_cache/` - Directory to store trained models

**2.2 Prediction Models Implementation**

**Prophet Model** (`prophet_predictor.py`):

- Use Facebook Prophet for seasonal trend analysis
- Train on 2+ years of historical data
- Predict next 30/60/90 days
- Include confidence intervals

**LSTM Model** (`lstm_predictor.py`):

- Build TensorFlow/Keras LSTM network
- Features: price, volume, moving averages (7, 30, 90 day)
- Sequence length: 60 days
- Predict next 1-30 days
- Save/load trained models

**Statistical Models** (`statistical_predictor.py`):

- Simple Moving Average (SMA): 7, 30, 90, 200 day
- Exponential Moving Average (EMA)
- Linear regression trend
- ARIMA model for time series
- Bollinger Bands for volatility

**Ensemble Predictor** (`ensemble_predictor.py`):

- Weighted average of all model predictions
- Confidence scoring based on historical accuracy
- Model selection based on stock volatility characteristics

**2.3 Prediction API Endpoints**

- `GET /api/predict/{symbol}` - Get predictions from all models
- `GET /api/predict/{symbol}/prophet` - Prophet-only prediction
- `GET /api/predict/{symbol}/lstm` - LSTM-only prediction
- `GET /api/predict/{symbol}/statistical` - Statistical models
- `GET /api/predict/{symbol}/ensemble` - Best combined prediction
- `POST /api/predict/train/{symbol}` - Trigger model training
- `GET /api/predict/history/{symbol}` - Get past predictions vs actuals

**2.4 Background Tasks**

- Create `tasks/` directory with Celery or APScheduler
- Schedule daily model retraining for portfolio stocks
- Cache predictions to reduce computation time
- Update prediction accuracy metrics

### Phase 3: AI Chatbot - RAG with LangChain

**3.1 Knowledge Base Setup**

Create `chatbot/` directory:

- `knowledge_base.py` - Build vector store from portfolio data
- `rag_chain.py` - LangChain RAG implementation
- `embeddings.py` - Generate embeddings (use sentence-transformers locally)
- `prompts.py` - System prompts and templates

**3.2 RAG Implementation**

- **Vector Store**: Use ChromaDB (local, lightweight)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (runs locally)
- **LLM Options**:
  - Primary: Ollama with Llama 3.2 or Mistral (runs locally)
  - Fallback: OpenAI API (if user has key)
- **Documents to embed**:
  - User's portfolio holdings
  - Stock descriptions and sector information
  - Historical performance data
  - Prediction results and trends
  - Financial news (optional)

**3.3 Chatbot Capabilities**

- Answer questions about portfolio composition
- Explain individual stock performance
- Discuss prediction results and trends
- Provide investment insights based on portfolio
- Compare stocks within portfolio
- Suggest rebalancing based on predictions

**3.4 Chatbot API Endpoints**

- `POST /api/chat/message` - Send message, get response
- `GET /api/chat/history` - Get conversation history
- `DELETE /api/chat/history` - Clear chat history
- `POST /api/chat/refresh-context` - Update vector store with latest portfolio data

**3.5 LangChain Chain Structure**

```python
# Retrieval chain with portfolio context
retriever = vector_store.as_retriever()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a financial advisor AI..."),
    ("system", "Portfolio context: {context}"),
    ("human", "{question}")
])
chain = create_retrieval_chain(retriever, llm)
```

### Phase 4: React Frontend

**4.1 Project Setup**

- Create `frontend/` directory with Vite + React + TypeScript
- Install dependencies:
  - React Router for navigation
  - Axios for API calls
  - Recharts for data visualization
  - TailwindCSS + shadcn/ui for styling
  - React Query for state management
  - date-fns for date handling

**4.2 Frontend Structure**

```
frontend/
├── src/
│   ├── components/
│   │   ├── Portfolio/
│   │   │   ├── StockCard.tsx
│   │   │   ├── AddStockForm.tsx
│   │   │   ├── PortfolioSummary.tsx
│   │   │   └── StockTable.tsx
│   │   ├── Predictions/
│   │   │   ├── PredictionChart.tsx
│   │   │   ├── ModelComparison.tsx
│   │   │   ├── TrendIndicators.tsx
│   │   │   └── PredictionCard.tsx
│   │   ├── Chatbot/
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ChatButton.tsx
│   │   └── Layout/
│   │       ├── Navbar.tsx
│   │       ├── Sidebar.tsx
│   │       └── Footer.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Portfolio.tsx
│   │   ├── StockDetails.tsx
│   │   ├── Predictions.tsx
│   │   └── Analytics.tsx
│   ├── services/
│   │   ├── api.ts (Axios config)
│   │   ├── portfolioService.ts
│   │   ├── predictionService.ts
│   │   └── chatService.ts
│   ├── types/
│   │   └── index.ts (TypeScript interfaces)
│   ├── hooks/
│   │   ├── usePortfolio.ts
│   │   ├── usePredictions.ts
│   │   └── useChat.ts
│   └── utils/
│       ├── formatters.ts
│       └── constants.ts
```

**4.3 Key Pages & Features**

**Dashboard Page**:

- Portfolio total value with gain/loss indicators
- Top performing stocks
- Recent predictions summary
- Quick stats (total invested, current value, returns)
- Quick access chatbot widget

**Portfolio Page**:

- Table view of all stocks with current prices
- Add/edit/delete stock functionality
- Real-time price updates
- Individual stock performance (gain/loss %)
- Export portfolio data

**Stock Details Page**:

- Historical price chart (line/candlestick)
- All prediction models visualized
- Model comparison table
- Key metrics (volatility, trend strength)
- Buy/sell signals based on predictions

**Predictions Page**:

- Multi-stock prediction comparison
- Filter by prediction model
- Confidence levels visualization
- Historical prediction accuracy
- Download prediction reports

**4.4 Chatbot Integration**

- Floating chat button (bottom-right corner)
- Collapsible chat window
- Typing indicators
- Message history
- Context awareness (knows current page)
- Quick question suggestions

**4.5 Charts & Visualizations**

Using Recharts:

- Line charts for price history and predictions
- Area charts for portfolio value over time
- Bar charts for model comparison
- Pie charts for portfolio allocation
- Candlestick charts for stock details
- Confidence interval bands for predictions

### Phase 5: Integration & Polish

**5.1 Backend Dependencies**

Update `pyproject.toml` with:

```toml
dependencies = [
    "fastapi>=0.116.2",
    "uvicorn>=0.30.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "yfinance>=0.2.40",
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "prophet>=1.1.5",
    "tensorflow>=2.16.0",
    "scikit-learn>=1.5.0",
    "statsmodels>=0.14.0",
    "langchain>=0.2.0",
    "langchain-community>=0.2.0",
    "chromadb>=0.4.0",
    "sentence-transformers>=2.7.0",
    "requests>=2.32.5",
    "python-multipart>=0.0.9",
    "apscheduler>=3.10.0",
]
```

**5.2 Configuration Management**

- Create `.env` file for configuration:
  - Database URL
  - API keys (optional OpenAI)
  - Model paths
  - CORS origins
- Create `config.py` with pydantic-settings

**5.3 Error Handling & Validation**

- Pydantic schemas for request/response validation
- Custom exception handlers in FastAPI
- Graceful error messages for frontend
- Logging system (file + console)

**5.4 Testing**

- Pytest tests for core portfolio logic
- API endpoint tests
- Mock stock data for testing
- Frontend unit tests with Vitest

**5.5 Documentation**

- Update README.md with:
  - Project description
  - Setup instructions (backend + frontend)
  - API documentation
  - Model descriptions
  - Screenshots
- API documentation with FastAPI's automatic Swagger UI
- Inline code documentation

**5.6 Docker Setup (Optional)**

- `Dockerfile` for backend
- `docker-compose.yml` for full stack
- Include Ollama container for local LLM

**5.7 Performance Optimization**

- Cache predictions (Redis or in-memory)
- Lazy load ML models
- Database query optimization (indexes)
- Frontend code splitting
- Debounce stock search API calls

## Key Files to Create/Modify

**Backend:**

- `database.py` - SQLAlchemy setup
- `models/stock.py`, `models/user.py`, etc. - Database models
- `schemas/` - Pydantic schemas
- `services/stock_data_service.py` - yfinance integration
- `ml_models/` - All prediction models (7-8 files)
- `chatbot/` - RAG implementation (4-5 files)
- `config.py` - Configuration management
- Update `app.py` - Add all API routes
- Update `portfolio.py` - Database integration

**Frontend:**

- Initialize React project in `frontend/`
- 20+ component files
- API service files
- Custom hooks
- Type definitions

## Technical Stack Summary

**Backend:**

- FastAPI + Uvicorn
- SQLAlchemy + SQLite
- yfinance for stock data
- Prophet, TensorFlow (LSTM), statsmodels (ARIMA)
- LangChain + ChromaDB + sentence-transformers
- Ollama (Llama 3.2) for local LLM

**Frontend:**

- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS + shadcn/ui
- Recharts for visualization
- React Query for state
- Axios for API calls

**AI/ML:**

- Facebook Prophet (seasonal trends)
- LSTM Neural Network (deep learning)
- ARIMA (statistical)
- Moving averages & regression
- Ensemble weighted predictions

**Chatbot:**

- RAG with LangChain
- ChromaDB vector store
- Local embeddings (sentence-transformers)
- Ollama with Llama 3.2 (local LLM)

## Estimated Implementation Scope

- **Backend Database & APIs**: 15-20 files, ~2000 lines
- **ML Models**: 8-10 files, ~1500 lines
- **Chatbot RAG**: 6-8 files, ~800 lines
- **Frontend**: 30-40 files, ~3000 lines
- **Total**: ~60-80 files, ~7500 lines of code

This is a comprehensive full-stack AI-powered application that will take significant development time but will result in a production-ready portfolio management system with advanced predictive capabilities.