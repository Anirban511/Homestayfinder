"""Promote a user to admin: python make_admin.py you@example.com"""
import sys

from app.database import SessionLocal
from app.models import User

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <email>")
        sys.exit(1)
    db = SessionLocal()
    user = db.query(User).filter(User.email == sys.argv[1]).first()
    if not user:
        print(f"No user with email {sys.argv[1]}")
    else:
        user.role = "admin"
        db.commit()
        print(f"{sys.argv[1]} is now an admin.")
    db.close()
