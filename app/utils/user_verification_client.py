from passlib.context import CryptContext


class UserVerificationClient:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Get password hash."""
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_user(cls, user_password: str, password: str) -> bool:
        """Verify user."""
        return cls.verify_password(password, user_password)
