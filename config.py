import os
from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv("ENV", "prod")

# Для тестов может быть отдельный тестовый URL
if ENV == "test":
    DATABASE_URL = os.getenv("DB_URL_TESTS")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


