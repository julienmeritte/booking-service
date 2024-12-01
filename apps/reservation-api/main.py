from fastapi import FastAPI
from app.routes import router

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "welcome to reservation-api"}

app.include_router(router.router)

