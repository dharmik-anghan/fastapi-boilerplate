from datetime import datetime, timedelta
from fastapi import BackgroundTasks, HTTPException
from src.config import Config
from src.remote.db.otp.model import Otp
from src.utils.authenticate import get_user, otp_verified
from src.utils.send_otp import generate_OTP, send_otp_email
from src.remote.db.database import db


def sendOtp(request_data: dict):
    try:
        user = get_user(username_or_email=request_data.get("email"))

        otp_code = generate_OTP()
        send_otp_email(to_email=user.email, otp=otp_code)

        otp_data = db.query(Otp).filter_by(email=request_data.get("email")).first()

        if otp_data:
            otp_data.otp = otp_code
            otp_data.created_at = datetime.utcnow()
            db.commit()
        else:
            otp = Otp(otp=otp_code, email=user.email, created_at=datetime.utcnow())
            db.add(otp)
            db.commit()

        return {"message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )


def verify_account(request_data: dict):
    try:
        user = get_user(username_or_email=request_data.get("email"))

        if user.is_verified == True:
            raise Exception("User already verified")
        elif otp_verified(email=request_data.get("email"), otp=request_data.get("otp")):
            user.is_verified = True
            db.commit()
            return {"message": "Accouunt Verified!"}
        else:
            return {"message": "Could not validate account"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )
