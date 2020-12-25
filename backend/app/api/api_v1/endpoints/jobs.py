from datetime import datetime
from enum import Enum
from uuid import uuid4

from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ....core.database import SessionLocal
from ....core.jobs import JobBase
from ....core.scheduler import my_scheduler
from ....schemas.job import ActionEnum, JobCreate
from ....utils import generate_uuid

router = APIRouter()
db: Session = SessionLocal()


@router.put("")
async def add_job(job: JobCreate):
    job_class = next(
        (
            j for j in JobBase.__subclasses__()
            if j.meta_info()["job_class"] == job.job_class
        ),
        None,
    )
    if not job_class:
        return "message: Job Class not found!"
    
    job_id = generate_uuid(8)
    job.created_time = datetime.now()
    if job.job_type == "cron":
        trigger = CronTrigger.from_crontab(job.crontab)
        my_scheduler.add_job(
            job_class.run,
            trigger,
            id=job_id,
            name=job.name,
            kwargs=job.dict()
        )
    else:
        my_scheduler.add_job(
            job_class.run,
            id=job_id,
            name=job.name,
            kwargs=job.dict(),
            next_run_time=None,
            misfire_grace_time=3600,
        )
    return {"message": f"Job {job.name} created!"}


@router.get("")
async def get_jobs():
    job_list = []
    for job in my_scheduler.get_jobs():
        job_list.append(
            {
                "id": job.id,
                "name": job.name,
                "job_class": job.kwargs["job_class"],
                "created_time": job.kwargs["created_time"].strftime(
                    "%a, %d %b %Y %H:%M:%S %Z"
                ),
                "nextrun": job.next_run_time.strftime(
                    "%a, %d %b %Y %H:%M:%S %Z" 
                ) if job.next_run_time else None,
                "schedule": job.kwargs["crontab"] if job.kwargs["job_type"] == "cron" else "SINGLE",
                "status": "RUNNING" if job.next_run_time else "PAUSED",
            }
        )
    
    return job_list


@router.post("/{job_id}")
async def modify_job_state(job_id: str, action: ActionEnum = Body(..., embed=True)):
    if action ==  ActionEnum.pause:
        job = my_scheduler.pause_job(job_id)
        return {"message": f"Job {job.name} paused!"}
    else:
        job = my_scheduler.resume_job(job_id)
        return {"message": f"Job {job.name} resumed!"}


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    job = my_scheduler.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not exists!")
    my_scheduler.remove_job(job_id)
    return {"message": f"Job {job.name} deleted!"}
