import uvicorn
from fastapi import FastAPI
from .core.scheduler import my_scheduler
from .api.api_v1.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8443)
