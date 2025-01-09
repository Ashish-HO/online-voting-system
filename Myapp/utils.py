import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings


def send_otp(request, email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)  # in the encoded form
    otp = totp.now()
    print(type(otp))
    request.session["otp_secret"] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=3)
    request.session["otp_valid_date"] = str(valid_date)
    print(f"email : {email}")
    print(f"Your one time password is: {otp}")

    # email sending
    # subject = "OTP for login"
    # message = f"Your one time password is {otp} and is valid for only 3 minutes."
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [email]

    # try:
    #     send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    # except:
    #     pass
