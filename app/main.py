"""Small notes service supplied as part of the platform engineering exercise."""

from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import threading
import time

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import psycopg
from psycopg.rows import dict_row
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, Info, generate_latest


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("notes")

REQUESTS = Counter(
    "notes_http_requests_total", "Application HTTP responses", ["method", "route", "status"]
)
DURATION = Histogram(
    "notes_http_request_duration_seconds", "Application request duration", ["method", "route"]
)
BUILD = Info("notes_build", "Application build information")
BUILD.info({"version": os.getenv("APP_BUILD", "starter")})
SCHEMA_LOCK = threading.Lock()
schema_ready = False


@asynccontextmanager
async def lifespan(application: FastAPI):
    environment = os.getenv("APP_ENV", "").strip()
    allowed_environments = {"local", "staging", "production"}
    if not environment:
        raise RuntimeError("APP_ENV is required; set it to one of: local, staging, production")
    if environment not in allowed_environments:
        raise RuntimeError("APP_ENV must be one of: local, staging, production")
    application.state.environment = environment
    state_dir = Path(os.getenv("APP_STATE_DIR", "/opt/notes/runtime"))
    state_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "pid": os.getpid(),
        "environment": environment,
    }
    (state_dir / "startup.json").write_text(json.dumps(state), encoding="utf-8")
    logger.info("application_start build=%s environment=%s", os.getenv("APP_BUILD", "starter"), environment)
    yield


app = FastAPI(title="Notes Lab", version="1.0.0", lifespan=lifespan)
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.middleware("http")
async def observe_requests(request: Request, call_next):
    if request.url.path in {"/livez", "/readyz", "/metrics", "/docs", "/openapi.json", "/redoc"}:
        return await call_next(request)
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        # Route templates bound label cardinality; never label using note IDs or user input.
        route = getattr(request.scope.get("route"), "path", "unmatched")
        if request.url.path.startswith("/static/"):
            route = "/static"
        REQUESTS.labels(request.method, route, str(status)).inc()
        DURATION.labels(request.method, route).observe(time.perf_counter() - started)


@contextmanager
def database():
    global schema_ready
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "notes"),
            user=os.getenv("DB_USER", "notes"),
            password=os.getenv("DB_PASSWORD", ""),
            connect_timeout=2,
            options="-c statement_timeout=2000",
            row_factory=dict_row,
        ) as connection:
            with SCHEMA_LOCK:
                if not schema_ready:
                    connection.execute(
                        "CREATE TABLE IF NOT EXISTS notes ("
                        "id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, "
                        "text TEXT NOT NULL, "
                        "created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP)"
                    )
                    connection.commit()
                    schema_ready = True
            yield connection
    except psycopg.Error as error:
        # Do not log connection strings, credentials, or note contents.
        logger.warning("database_operation_failed type=%s", type(error).__name__)
        raise HTTPException(status_code=503, detail="Database unavailable") from None


class NewNote(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@app.get("/", include_in_schema=False)
def homepage():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/livez")
def live():
    return {"status": "alive"}


@app.get("/readyz")
def ready():
    with database() as connection:
        connection.execute("SELECT 1")
    return {"status": "ready"}


@app.get("/version")
def version():
    return {"build": os.getenv("APP_BUILD", "starter"), "environment": app.state.environment}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})


@app.post("/notes", status_code=201)
def create_note(note: NewNote):
    with database() as connection:
        row = connection.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id, text, created_at", (note.text,)
        ).fetchone()
    return row


@app.get("/notes")
def list_notes():
    with database() as connection:
        rows = connection.execute(
            "SELECT id, text, created_at FROM notes ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return rows


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    with database() as connection:
        row = connection.execute(
            "SELECT id, text, created_at FROM notes WHERE id = %s", (note_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return row
