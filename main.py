from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from admin_service.router import router as admin_service_router
from auth_service.routers.v1.router import router as auth_service_router
from notification_service.rabbit.broker.main import mq_router
from ai_service.routers.v1.router import router as ai_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Lifespan")
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_service_router)
app.include_router(admin_service_router)
# app.include_router(mq_router)
app.include_router(prefix="/ai/v1", router=ai_v1_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
