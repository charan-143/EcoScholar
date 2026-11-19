"""Seed the starter learning modules after the database schema is migrated."""
from app.db.session import SessionLocal
from app.services.seed import seed_courses
def main():
    with SessionLocal() as db:
        seed_courses(db)
        print("EcoScholar starter courses seeded.")
if __name__=="__main__": main()
