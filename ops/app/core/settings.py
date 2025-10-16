import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = (os.getenv("database_url")).strip()
