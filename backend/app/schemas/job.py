from datetime import datetime
from datetime import datetime
from enum import Enum

from pydantic import BaseModel

class TypeEnum(str, Enum):
    cron = "cron"
    single = "single"


class ActionEnum(str, Enum):
    resume = "resume"
    pause = "pause"


class JobCreate(BaseModel):
    name: str
    job_class: str
    args: dict
    job_type: TypeEnum
    crontab: str
    created_time: datetime = None
