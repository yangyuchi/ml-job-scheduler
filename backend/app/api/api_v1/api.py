from fastapi import APIRouter

from .endpoints import job_classes, jobs

api_router = APIRouter()
api_router.include_router(jobs.router, prefix="/jobs")
api_router.include_router(job_classes.router, prefix="/job_classes")
