from sqlalchemy.orm import Session

from app.db.models.user_model import User


# Retrieve a user from the database by username
def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


# Create a new user and save it to the database
def create_user(
    db: Session,
    username: str,
    hashed_password: str,
    role: str = "user",
) -> User:
    user = User(
        username=username,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
