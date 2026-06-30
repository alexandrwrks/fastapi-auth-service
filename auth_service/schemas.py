from pydantic import BaseModel, EmailStr, Field


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RegisterSchema(BaseModel):
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Password")


class LoginSchema(BaseModel):
    username: str
    password: str


class RefreshSchema(BaseModel):
    refresh_token: str


class OTPSchema(BaseModel):
    username: str
    email: EmailStr
    otp_code: str
