# # app/db/database.py
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv
# import os

# load_dotenv()

# DATABASE_URL = os.getenv("SUPABASE_DB_URL")
# SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA", "public")  # default public

# # ✅ Create MetaData with global schema
# metadata = MetaData(schema=SUPABASE_SCHEMA)

# # ✅ Create Base using that metadata
# Base = declarative_base(metadata=metadata)

# # ✅ Setup engine and session
# engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL logs
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Load environment variables
DATABASE_URL = os.getenv("SUPABASE_DB_URL")
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA", "public")  # default: public

# ✅ Create MetaData with global schema
metadata = MetaData(schema=SUPABASE_SCHEMA)

# ✅ Create Base using that metadata
Base = declarative_base(metadata=metadata)

# ✅ Setup SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # show SQL in console (can disable in prod)
    pool_pre_ping=True,  # prevent stale connections
)

# ✅ Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Dependency for FastAPI routes
def get_db():
    """Provide a SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
