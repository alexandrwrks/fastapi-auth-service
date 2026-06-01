from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from admin_service.router import router as admin_service_router
from auth_service.router import router as auth_service_router
from broker.main import mq_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Lifespan")
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_service_router)
app.include_router(admin_service_router)
app.include_router(mq_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
