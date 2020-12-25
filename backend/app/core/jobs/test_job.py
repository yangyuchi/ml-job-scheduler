import logging
from ._base import JobBase

logging.basicConfig(level=logging.INFO)

class PrintHello(JobBase):
    description: str = "Just for Test"
    arguments: dict = {
        "times": "How many hellos to print (int)",
    }

    @classmethod
    async def run(cls, **kwargs):
        args = kwargs["args"]
        for i in range(int(args["times"])):
            logging.info("Hello!")
