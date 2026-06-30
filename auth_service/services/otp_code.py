import secrets
import string


def generate_otp_code(
    length: int = 6,
) -> str:
    # Цифровой OTP-код для подтверждения почты состоящий из шести символов
    return "".join(secrets.choice(string.digits) for _ in range(length))
