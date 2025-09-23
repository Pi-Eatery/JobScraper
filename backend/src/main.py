import logging
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from .api import auth, applications
from .models.database import Base, engine # Import Base and engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # React frontend default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(applications.router, prefix="/api", tags=["applications"])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request: {request.method} {request.url} - Processed in {process_time:.4f}s - Status: {response.status_code}")
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail} for {request.method} {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled Exception for {request.method} {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred."},
    )

@app.get("/")
def read_root():
    return {"message": "JobScraper API"}