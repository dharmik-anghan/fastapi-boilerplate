from datetime import datetime , timedelta
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
    
def  verifyOtp(email : str , otp : int):
    try: 
        user = get_user(username_or_email=email)
        otp_data = db.query(Otp).filter_by(email = email).first()
            
        current_time = datetime.utcnow()
        expiry_time = otp_data.created_at + timedelta(minutes=3)

        if expiry_time < current_time :
            raise Exception("OTP is Expire!")
        elif otp_data.otp != otp :
            raise Exception("Invalid OTP entered")
        else:
            db.delete(otp_data)

            user.is_verified = True
            db.commit()

            return {"message" : "OTP verify successfully!"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )