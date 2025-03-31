import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
               f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

MAX_RETRIES = 5
RETRY_DELAY = 5

Base = declarative_base()

for i in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        print("✅ Successfully connected to the database!")
        break
    except Exception as e:
        print(f"⚠️ Database connection failed. Retrying in {RETRY_DELAY} seconds... ({i+1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY)
else:
    print("❌ Could not connect to the database. Exiting.")
    exit(1)
