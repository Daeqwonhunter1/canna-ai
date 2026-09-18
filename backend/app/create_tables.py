from db.db import engine
from db.db_models import Base

print("Creating tables")
Base.metadata.create_all(bind=engine)

print("Tables created")