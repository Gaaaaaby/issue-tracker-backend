from datetime import timedelta

SECRET_KEY = "change_this_secret_key_for_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DB_URL = "sqlite:///./issues.db"
TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
