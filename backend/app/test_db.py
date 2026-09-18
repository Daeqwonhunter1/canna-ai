from db.db import engine

try:
    connection = engine.connect()

    print("Connected to PostgreSQL")

    connection.close()

except Exception as e:
    print("Database connection failed")
    print(e)