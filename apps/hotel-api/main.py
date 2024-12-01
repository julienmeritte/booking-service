from fastapi import FastAPI

from app.routes import router


app = FastAPI()


@app.get("/", status_code=200)
async def root():
    return {"message": "welcome to hotel-api"}


app.include_router(router.router)
