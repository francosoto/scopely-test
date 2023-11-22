import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "debug")
DB_HOST = os.getenv("DB_HOST", "db")
DB_USERNAME = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_DATABASE = os.getenv("DB_NAME", "dbname")
CACHE_HOST = os.getenv("CACHE_HOST", "redis")
CACHE_PASSWORD = os.getenv("CACHE_PASSWORD", "password")
CACHE_DB = os.getenv("CACHE_DB", "0")
MAX_CONCURRENT_REQUESTS = 25
MAX_REQUEST_DURATION = 4
