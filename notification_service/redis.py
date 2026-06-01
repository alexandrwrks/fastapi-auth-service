import asyncio
import secrets
import string

from redis.asyncio import ConnectionPool, Redis

SAFE_TIME_SECONDS = 300


def generate_otp_code(
    length: int = 6,
) -> str | None:  # Цифровой OTP-код для подтверждения почты состоящий из шести символов
    return "".join(secrets.choice(string.digits) for _ in range(length))


class RedisEmail:
    def __init__(self):
        self.connection = ConnectionPool(
            host="localhost", port=6379, db=0, decode_responses=True
        )
        self.client = Redis(connection_pool=self.connection)

    async def save_otp_code(self, username: str, otp_code: str):
        await self.client.set(username, otp_code, ex=SAFE_TIME_SECONDS)

    async def verify_otp_code(self, username: str, otp_code: str) -> bool:
        safed_otp_code = await self.client.get(username)
        if safed_otp_code is None:
            raise OTPExpiredError

        if safed_otp_code == otp_code:
            await self.client.delete(username)
            return True

        return False


redis = RedisEmail()


async def main():
    username1 = "test1"

    otp_code1 = generate_otp_code()

    await redis.save_otp_code(username1, otp_code1)

    print("Сохранение данных")
    try:
        verify = await redis.verify_otp_code(username1, otp_code1)
        print(verify)

    except OTPExpiredError:
        print("Время жизни OTP Code истекло")


class BaseError(Exception):
    pass


class OTPExpiredError(BaseError):
    pass


if __name__ == "__main__":
    asyncio.run(main())
