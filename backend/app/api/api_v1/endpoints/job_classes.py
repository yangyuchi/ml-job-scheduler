from fastapi import APIRouter
from ....core.jobs import JobBase

router = APIRouter()

@router.get("")
async def get_job_classes():
    return [j.meta_info() for j in JobBase.__subclasses__()]
