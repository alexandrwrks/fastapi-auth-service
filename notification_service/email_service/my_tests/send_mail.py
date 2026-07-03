import asyncio

from notification_service.email_service.email_service import email_service


async def main():
    print("sending email")
    await email_service.send_welcome_email(
        "koozma-alex@mail.ru",
        "kr00sh"
    )

    print("successfully sent email")



if __name__ == "__main__":
    asyncio.run(main())