# test_env.py
from decouple import config
import dj_database_url

print("DATABASE_URL:", config('DATABASE_URL', default='YOX'))
print("DEBUG:", config('DEBUG', default=True))

db_config = dj_database_url.config(
    default=config('DATABASE_URL', default='postgres://dropaz:P@ssw0rdO75@localhost:5432/dropaz_db')
)
print("Database config:", db_config)