from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- 1. IMPORT THIS
from app.api import auth, templates

app = FastAPI()

# --- 2. ADD THIS MIDDLEWARE BLOCK ---
# This block should be placed before you include your routers.

origins = [
    "http://localhost:4200",  # Your Angular frontend
    "http://localhost:4201",  # Add any other origins you might use
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins to make requests
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)
# ------------------------------------


# Your existing router includes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(templates.router, prefix="/templates", tags=["Templates"])


@app.get("/")
def home():
    return {"message": "Template Downloader Backend is running"}