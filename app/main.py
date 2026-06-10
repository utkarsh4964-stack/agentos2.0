from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.database import Base, engine
from app.models import user, pipeline  # noqa: F401 - register models with Base
from app.routers import auth

# Create all tables on startup (fine for early stage; switch to Alembic later)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgentOS API")

# CORS - wide open for now since frontend and backend are same origin on Railway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")


@app.get("/login")
def serve_login():
    return FileResponse("frontend/login.html")


@app.get("/signup")
def serve_signup():
    return FileResponse("frontend/signup.html")


@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("frontend/dashboard.html")
