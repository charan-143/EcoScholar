"""Bootstrap or promote an administrator from a trusted local shell."""
import argparse
from getpass import getpass
from app.db.session import SessionLocal
from app.models.user import User
from app.services.security import hash_password

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--email",required=True)
    parser.add_argument("--name",default="EcoScholar Administrator")
    args=parser.parse_args()
    email=args.email.strip().lower()
    with SessionLocal() as db:
        user=db.query(User).filter(User.email==email).first()
        if user:
            user.role="admin"
            db.commit()
            print(f"Promoted existing account {email} to admin.")
            return
        password=getpass("Set initial admin password (minimum 10 characters): ")
        if len(password)<10: raise SystemExit("Password must contain at least 10 characters.")
        confirm=getpass("Confirm password: ")
        if password!=confirm: raise SystemExit("Passwords do not match.")
        db.add(User(email=email,display_name=args.name,password_hash=hash_password(password),role="admin"))
        db.commit()
        print(f"Created administrator account for {email}.")

if __name__=="__main__": main()
