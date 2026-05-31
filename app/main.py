import uvicorn
from fastapi import FastAPI

from app.routers import routers
app = FastAPI()



for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)