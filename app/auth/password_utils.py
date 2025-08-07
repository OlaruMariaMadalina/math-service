from passlib.context import CryptContext


# Password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash a plain password using bcrypt.
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify a plain password against a hashed password.
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
