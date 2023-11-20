from src.auth import router as auth_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API rararara!!"}
