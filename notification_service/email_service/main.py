import asyncio
from email.message import EmailMessage

import aiosmtplib

from auth_service.schemas import OTPSchema


class NotificationEmailService:
    async def send_email(self, user: OTPSchema):

        message = EmailMessage()
        message["From"] = "init@domain.com"
        message["To"] = user.email
        message["Subject"] = user.otp_code
        message.set_content(
            f"Подтверждение почты для регистрации пользователя {user.username} на сайте\n"
            f"Код подтверждения: {user.otp_code}"
        )

        await aiosmtplib.send(message, hostname="localhost", port=587, username="")


user = OTPSchema(email="example@example.com", otp_code="123456")

if __name__ == "__main__":
    asyncio.run(NotificationEmailService().send_email(user))
