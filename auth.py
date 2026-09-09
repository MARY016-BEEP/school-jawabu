import bcrypt

from database import SessionLocal
from models import User


def hash_password(password):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, password_hash):

    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def create_default_users():

    db = SessionLocal()

    users = [

        ("director", "director123", "DIRECTOR"),

        ("accountant", "account123", "ACCOUNTANT"),

        ("teacher", "teacher123", "TEACHER"),

        ("receptionist", "reception123", "RECEPTIONIST")

    ]

    for username, password, role in users:

        existing_user = db.query(User).filter(
            User.username == username
        ).first()

        if not existing_user:

            user = User(
                username=username,
                password_hash=hash_password(password),
                role=role,
                active=True
            )

            db.add(user)

    db.commit()
    db.close()


def login_user(username, password):

    db = SessionLocal()

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user:

        if verify_password(
            password,
            user.password_hash
        ):

            role = user.role

            db.close()

            return {
                "username": username,
                "role": role
            }

    db.close()

    return None
