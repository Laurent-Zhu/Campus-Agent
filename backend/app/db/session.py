# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from ..core.config import settings

# engine = create_engine(
#     settings.DATABASE_URL,
#     pool_pre_ping=True,
#     echo=settings.DEBUG
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)