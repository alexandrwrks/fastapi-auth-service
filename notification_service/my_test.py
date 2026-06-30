import asyncio

from auth_service.schemas import OTPSchema
from .redis.redis import main


user = OTPSchema(email="example@example.com", otp_code="123456")

if __name__ == "__main__":
    asyncio.run(main(user))
