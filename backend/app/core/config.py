import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecoscholar.db")
APP_NAME = "EcoScholar API"
