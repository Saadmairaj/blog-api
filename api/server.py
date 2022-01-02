from fastapi import FastAPI
from api.routes import blog_router

app = FastAPI()
app.include_router(router=blog_router, prefix="/api")
