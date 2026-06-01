from faststream.rabbit.fastapi import RabbitRouter

mq_router = RabbitRouter()

send_user_event = mq_router.publisher("new_users")


@mq_router.subscriber("new_users")
async def handle_new_users(username: str):
    print(f"Успешная регистрация нового пользователя: {username}")
