import abc

from pydantic import BaseModel

class JobBase(BaseModel, abc.ABC):
    name: str
    description: str
    arguments: dict

    @classmethod
    def meta_info(cls):
        """Meta info of the job"""
        return {
            "job_class": f"{cls.__module__.split('.')[-1]}.{cls.__name__}",
            "args": cls.__fields__["arguments"].get_default(),
            "description": cls.__fields__["description"].get_default(),
        }

    @abc.abstractmethod
    async def run(**kwargs):
        """Each Job must has a run() method"""
        raise NotImplementedError("Job must has a run method!")
