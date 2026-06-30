from redis.asyncio import ConnectionPool, Redis

from auth_service.schemas import OTPSchema
from notification_service.exception import OTPExpiredError

SAFE_TIME_SECONDS = 300


class RedisEmail:
    def __init__(self):
        self.connection = ConnectionPool(
            host="localhost", port=6379, db=0, decode_responses=True
        )
        self.client = Redis(connection_pool=self.connection)

    async def save_otp_code(self, email: str, otp_code: str):
        await self.client.set(email, otp_code, ex=SAFE_TIME_SECONDS)

    async def verify_otp_code(self, email: str, otp_code: str) -> bool:
        safed_otp_code = await self.client.get(email)
        if safed_otp_code is None:
            raise OTPExpiredError

        if safed_otp_code == otp_code:
            await self.client.delete(email)
            return True

        return False


async def main(user: OTPSchema):
    await redis.save_otp_code(user.email, user.otp_code)

    print("Сохранение данных")
    try:
        verify = await redis.verify_otp_code(user.email, user.otp_code)
        print(verify)

    except OTPExpiredError:
        print("Время жизни OTP Code истекло")


redis = RedisEmail()
