from fastapi import FastAPI
from controller import root_router
app = FastAPI()

app.include_router(root_router)
