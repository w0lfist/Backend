from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.users import user_route
from decouple import config

app = FastAPI()

print(config("FRONTEND_URL"))

origins = [
    config("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="https://timetoimprove.vercel.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def welcome():
    return {"message": "Welcome tu Time to Improve"}

app.include_router(user_route)
