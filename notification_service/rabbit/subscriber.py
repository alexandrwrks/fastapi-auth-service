from faststream.rabbit import RabbitRouter

from notification_service.rabbit.queue import *
from notification_service.schemas import SendVerifyEmail

router = RabbitRouter()


@router.subscriber(queue=new_user)
async def new_user_subscriber():
    pass


@router.subscriber(queue=verify_email)
async def verify_email_subscriber(data: SendVerifyEmail):

    # await send_verify_email(data)
    print("Успешная отправка OTP кода")
