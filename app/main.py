from fastapi import FastAPI
from app.api import auth, templates

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(templates.router, prefix="/templates", tags=["Templates"])

@app.get("/")
def home():
    return {"message": "Template Downloader Backend is running"}
