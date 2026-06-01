import hashlib


class HashingToken:
    @staticmethod
    def hashing_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def check_token(token: str, hashed_token: str) -> bool:
        return HashingToken.hashing_token(token) == hashed_token
