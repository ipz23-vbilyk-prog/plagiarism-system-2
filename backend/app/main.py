from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os

app = FastAPI(
    title="Plagiarism System",
    version="1.0.0"
)

# =====================================
# PATHS
# =====================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    "static"
)

if os.path.exists(STATIC_DIR):
    app.mount(
        "/static",
        StaticFiles(directory=STATIC_DIR),
        name="static"
    )

# =====================================
# ROUTERS
# =====================================

try:
    from backend.app.api.v1.auth import router as auth_router

    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["Auth"]
    )

except Exception as e:
    print("AUTH ROUTER ERROR:", e)

try:
    from backend.app.api.v1.documents import router as documents_router

    app.include_router(
        documents_router,
        prefix="/documents",
        tags=["Documents"]
    )

except Exception as e:
    print("DOCUMENTS ROUTER ERROR:", e)

# =====================================
# PAGES
# =====================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


@app.get("/check", response_class=HTMLResponse)
async def check_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="check.html"
    )

# =====================================
# TEST ROUTE
# =====================================

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }