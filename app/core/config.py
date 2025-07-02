import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://mangeshbabansawant:mangeshbabansawant@telenliotemplate.t4aunrx.mongodb.net/?retryWrites=true&w=majority&appName=TelenlioTemplate")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
