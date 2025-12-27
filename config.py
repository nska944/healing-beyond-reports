import os

SECRET_KEY = os.getenv("SECRET_KEY", "healing-beyond-reports-secret")

# Railway (and others) provide POSTGRES_URL or DATABASE_URL
# SQLAlchemy 1.4+ removed support for 'postgres://' URI scheme, it expects 'postgresql://'
database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
