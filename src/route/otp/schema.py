from pydantic import BaseModel, EmailStr


class OTPSchema(BaseModel):
    email: EmailStr

class OTPVerification(OTPSchema):
    otp : str
