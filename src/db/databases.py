from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.config import Settings

settings = Settings()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)

local_session = sessionmaker(
    autoflush=False, autocommit=False, bind=engine)
