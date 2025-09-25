import logging
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .middleware.auth import get_current_user
import time
import os
from pythonjsonlogger import jsonlogger

from .api import auth, applications, jobs, keywords
from .models.database import Base, engine, SessionLocal  # Import SessionLocal
from .middleware.metrics import MetricsMiddleware, metrics_endpoint
from .services.scraper import scrape_all_jobs  # Import scrape_all_jobs
from .models.user import User  # Import User model
from .services.auth_service import (
    AuthService,
    get_password_hash,
)  # Import AuthService for user creation

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup_event():
    logger.info("Running startup event: Scraping jobs...")
    db = SessionLocal()
    try:
        # Find the first user or create a placeholder user if none exists
        user = db.query(User).first()
        if not user:
            logger.info("No user found, creating a placeholder user for scraping.")
            auth_service = AuthService()
            user = auth_service.register_user(
                db, "scraper_user", "scraper@example.com", "scraper_password"
            )

        scrape_all_jobs(db, user.id)
        logger.info("Job scraping completed on startup.")
    except Exception as e:
        logger.error(f"Error during job scraping on startup: {e}")
    finally:
        db.close()


# Configure CORS
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost,http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000,http://192.168.2.201:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add metrics middleware
app.add_middleware(MetricsMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(
    applications.router,
    prefix="/api",
    tags=["applications"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    jobs.router,
    prefix="/api",
    tags=["jobs"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    keywords.router,
    prefix="/api",
    tags=["keywords"],
    dependencies=[Depends(get_current_user)],
)


@app.get("/metrics")
async def get_metrics(request: Request):
    return await metrics_endpoint(request)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        "Request processed",
        extra={
            "method": request.method,
            "url": str(request.url),
            "process_time": f"{process_time:.4f}s",
            "status_code": response.status_code,
        },
    )
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(
        "HTTPException occurred",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "method": request.method,
            "url": str(request.url),
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled Exception occurred",
        extra={
            "method": request.method,
            "url": str(request.url),
        },
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred."},
    )


@app.get("/")
def read_root():
    return {"message": "JobScraper API"}
