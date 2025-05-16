from dotenv import load_dotenv
from fastapi import FastAPI
load_dotenv()
from controller.root import router

app = FastAPI(
    title="DishFinder API",
    description="API for translating menu items and retrieving dish information",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)
