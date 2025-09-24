import logging
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .middleware.auth import get_current_user
import time
import os
from pythonjsonlogger import jsonlogger

from .api import auth, applications, jobs
from .models.database import Base, engine  # Import Base and engine
from .middleware.metrics import MetricsMiddleware, metrics_endpoint

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure CORS
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost,http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000",
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
