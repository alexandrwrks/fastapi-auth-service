import smtplib
from email.message import EmailMessage

# Настройки подключения
sender = "koozma-alex@mail.ru"
password = "OQqVSHOv7RJHLuK0VPeC"
recipient = "recipient@example.com"

msg = EmailMessage()
msg.set_content("Привет! Это тестовое сообщение из Python.")
msg["Subject"] = "Тема письма"
msg["From"] = sender
msg["To"] = recipient

# Отправка через SSL (например, для Yandex, Mail.ru)
try:
    with smtplib.SMTP_SSL(host="smtp.mail.ru", port=465) as server:
        server.login(sender, password)
        server.send_message(msg)
    print("Письмо успешно отправлено!")
except Exception as e:
    print(f"Ошибка: {e}")
