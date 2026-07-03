import aiosmtplib

from email.message import EmailMessage
from notification_service.utils.config import settings

class EmailService:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.email = settings.SMTP_EMAIL
        self.password = settings.SMTP_PASSWORD

    async def send_welcome_email(
        self,
        username: str,
        email: str,
    ) -> None:
        message = EmailMessage()

        message["From"] = self.email
        message["To"] = email
        message["Subject"] = "Добро пожаловать!"

        message.set_content(f"""
        Здравствуйте, {username}!
        
        Добро пожаловать в наш сервис.
        
        Ваш аккаунт успешно зарегистрирован.
        
        Желаем приятного использования!
        
        С уважением,
        Команда проекта.
        """.strip())

        try:
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.email,
                password=self.password,
                use_tls=True,
            )

        except Exception as e:
            print(e)
            raise

email_service = EmailService()