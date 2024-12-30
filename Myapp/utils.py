import pyotp
from datetime import datetime, timedelta


def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)  #in the encoded form 
    otp = totp.now()
    print(type(otp))
    request.session["otp_secret"] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=3)
    request.session["otp_valid_date"] = str(valid_date)

    print(f"Your one time password is {otp}")
 
