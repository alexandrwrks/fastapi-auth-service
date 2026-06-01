from pydantic import BaseModel, EmailStr


class SendVerifyEmail(BaseModel):
    email: EmailStr
    username: str
    otp: int
