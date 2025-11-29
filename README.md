# All-in-One API Demo

A structured FastAPI project demonstrating multiple API styles and protocols:

- **REST API** - Standard HTTP endpoints for task CRUD
- **SOAP** - XML-based RPC-style endpoint
- **gRPC-sim** - Simulated gRPC over HTTP+JSON
- **GraphQL** - Query language for tasks (Strawberry)
- **WebHooks** - Receiver and event storage
- **WebSockets** - Multi-user chat rooms with persistence
- **WebRTC** - Fake signaling endpoint

## Project Structure

```
api_app/
  ├── __init__.py           # FastAPI app setup, middleware, startup
  ├── db.py                 # Database helpers (SQLite)
  ├── models.py             # Pydantic request/response models
  ├── rest.py               # REST endpoints
  ├── soap.py               # SOAP/XML endpoint
  ├── grpc_sim.py           # gRPC-sim endpoint
  ├── graphql_api.py        # GraphQL schema and router
  ├── webhooks.py           # Webhook receiver and listing
  ├── ws.py                 # WebSocket chat handlers
  ├── webrtc.py             # WebRTC signaling endpoint
  └── root.py               # Root endpoint with endpoint listing

main.py                      # Entry point (runs uvicorn)
sample_apis.py              # Compatibility shim (re-exports app)
smoke_all_endpoints.py      # Integration test suite
requirements.txt            # Python dependencies
```

## Setup

1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```powershell
   python .\main.py
   ```
   Or with uvicorn directly:
   ```powershell
   uvicorn api_app:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Access the API:**
   - Root: http://127.0.0.1:8000/
   - REST tasks: http://127.0.0.1:8000/rest/tasks
   - GraphQL: http://127.0.0.1:8000/graphql
   - WebSocket: `ws://127.0.0.1:8000/ws/chat/{room}/{username}`

## Testing

Run the integrated smoke test:
```powershell
python .\smoke_all_endpoints.py
```

This tests all endpoints (REST, SOAP, gRPC, GraphQL, webhooks, WebSocket, WebRTC) and validates they return expected responses.

## Database

Uses SQLite (`sample.db`) for:
- Tasks (seeded with sample data)
- Webhook events
- Chat history

Database is auto-initialized on startup if it doesn't exist.

## API Endpoints

### REST
- `GET /rest/tasks` — list all tasks
- `POST /rest/tasks` — create task
- `GET /rest/tasks/{task_id}` — get task by ID

### SOAP
- `POST /soap` — XML request/response (expects task id in `<id>` element)

### gRPC-sim
- `POST /grpc/add` — simulated gRPC add (request: `{a: int, b: int}`)

### GraphQL
- `POST /graphql` — GraphQL queries (e.g., `{ tasks { id title status } }`)

### Webhooks
- `POST /webhooks/receive` — receive webhook event
- `GET /webhooks/events` — list stored webhook events

### WebSocket
- `WS /ws/chat/{room}/{username}` — join a chat room, receive broadcasts, send messages
- `GET /chat/{room}` — get chat history for a room

### WebRTC
- `POST /webrtc/offer` — fake WebRTC signaling endpoint

### Root
- `GET /` — list all endpoints