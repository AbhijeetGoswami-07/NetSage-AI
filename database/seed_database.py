"""Initialize the database from the sample dataset."""
from database.db import connect
from data.seed_cases import seed
if __name__ == "__main__":
    with connect() as db: count = db.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
    print(f"Database ready; existing cases: {count}; imported: {seed()}")
