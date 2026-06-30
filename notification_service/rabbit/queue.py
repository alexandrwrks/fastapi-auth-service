from faststream.rabbit import RabbitQueue

new_user = RabbitQueue(
    "new_user"
)  # После того как новый пользователь полностью зарегистрировался
verify_email = RabbitQueue("verify_email")  # Подтверждение email
