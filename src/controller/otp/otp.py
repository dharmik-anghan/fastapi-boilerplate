from datetime import datetime
from fastapi import HTTPException
from src.remote.db.otp.model import Otp
from src.utils.authenticate import get_user
from src.utils.send_otp import generate_OTP , send_otp_email
from src.remote.db.database import db


def sendOtp(email : str):
    try:
        user = get_user(username_or_email=email)
        otp_code = generate_OTP()
        message = send_otp_email(to_email = user.email , otp = otp_code)

        otp = Otp(
            otp = otp_code,
            email = user.email,
            created_at = datetime.utcnow()
        )

        db.add(otp)
        db.commit()
        return message
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )