from argon2 import PasswordHasher


class HashingPassword:
    ph = PasswordHasher()

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.ph.hash(password)

    @classmethod
    def verify_password(cls, hashed: str, password: str) -> bool:
        return cls.ph.verify(hashed, password)
