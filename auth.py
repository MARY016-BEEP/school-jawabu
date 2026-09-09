import bcrypt
from database import SessionLocal
from models import User


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed_password):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


def create_default_users():

    db = SessionLocal()

    users = [

        ("director", "director123", "DIRECTOR"),

        ("accountant", "account123", "ACCOUNTANT"),

        ("teacher", "teacher123", "TEACHER")

    ]

    for username, password, role in users:

        existing = db.query(User).filter(
            User.username == username
        ).first()

        if not existing:

            user = User(

                username=username,

                password_hash=hash_password(password),

                role=role

            )

            db.add(user)

    db.commit()

    db.close()


def login_user(username, password):

    db = SessionLocal()

    user = db.query(User).filter(
        User.username == username
    ).first()

    db.close()

    if user and verify_password(
        password,
        user.password_hash
    ):

        return user

    return None