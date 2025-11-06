from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the database URL (e.g. postgresql://user:password@localhost/dbname)
DATABASE_URL = os.getenv("DATABASE_URL")

# Define base class for models
Base = declarative_base()

# Create SQLAlchemy engine and session factory
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Database connection is successful.")
except Exception as e:
    print("❌ Database connection failed:", str(e))


# Dependency to get DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
