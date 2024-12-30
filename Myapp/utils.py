import pyotp
from datetime import datetime, timedelta


def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  #in the encoded form 
    otp = totp.now()
    print(type(otp))
    request.session["otp_secret"] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session["otp_valid_date"] = str(valid_date)

    print(f"Your one time password is {otp}")
 
totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  #in the encoded form 
otp = totp.now()
print(type(otp))