import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from root .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()