import smtplib
from email.message import EmailMessage
import secrets

from app.settings import settings


class EmailService:
    def __init__(self, recipient: str, sender: str = "koozma-alex@mail.ru"):
        self.receiver = recipient
        self.sender = sender

    def create_message(
        self,
        subject: str,
        content: str,
    ) -> EmailMessage:
        msg = EmailMessage()

        msg["From"] = self.sender
        msg["To"] = self.receiver
        msg["Subject"] = subject
        msg.set_content(content)

        return msg


class OtpService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.password = settings.MAIL_PASSWORD

    def create_register_message(self):
        otp_code = secrets.randbelow(900_000) + 100_000

        msg = self.email_service.create_message(
            subject="Регистрация на сайте", content=f"Код подтверждения: {otp_code}"
        )

        return msg

    def send_otp(self):
        msg = self.create_register_message()
        try:
            with smtplib.SMTP_SSL(host="smtp.mail.ru", port=465) as smtp:
                smtp.login(self.email_service.sender, self.password)
                smtp.send_message(msg)
            print("Письмо успешно отправлено")
        except Exception as e:
            print(f"Ошибка: {e}")

    def send_login_notification(self):
        """
        Отправка сообщения об успешном входе
        """
        ...


if __name__ == "__main__":
    mail = "koozma-alex@mail.ru"

    otp_service = OtpService(email_service=EmailService(recipient=mail))

    otp_service.send_otp()
