from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View

from datetime import datetime
import pyotp

from .forms import CreateUserForm
from .utils import send_otp


# Create your views here.
@login_required(login_url="loginpage")
def logoutpage(request):
    logout(request)
    return redirect("loginpage")


class register(View):
    form = CreateUserForm()
    errors = {}

    def get(self, request):
        return render(request, "registration.html", self.errors)

    def post(self, request):
        form = CreateUserForm(request.POST)  # Fill form with data from request
        email = request.POST.get("email")
        try:
            username_exists = User.objects.get(username=request.POST["username"])
            email_taken = User.objects.get(email=request.POST["email"])
            print(email_taken)
            messages.info(request, "User already registered.")
            return redirect("loginpage")
        except:
            if form.is_valid():
                form.save()
                return redirect("loginpage")
            else:
                errors = {"errors": form.errors}  # FORM IS INVALID
        return render(
            request, "registration.html", self.errors
        )  # SHOW REGISTRATION PAGE WITH ERRORS


class LoginUser(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = User.objects.get(username=username).email
        print("from login page")
        print(email)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # SEND OTP TO USER.....
            send_otp(request, email)
            request.session["username"] = username
            return redirect("otp")
        else:
            messages.info(request, "Incorrect Credentials.")

        return render(request, "login.html")


class otp(View):

    def get(self, request):
        return render(request, "otp.html")

    def post(self, request):
        otp = request.POST.get("otp")
        username = request.session["username"]
        otp_secret = request.session["otp_secret"]
        valid_date = request.session["otp_valid_date"]

        print(f"username : {username}")
        print(f"valid_date:{valid_date}")

        if otp_secret and valid_date is not None:
            valid_until = datetime.fromisoformat(valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret, interval=60)

                if pyotp.TOTP(otp_secret, interval=60).verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session["otp_secret"]
                    del request.session["otp_valid_date"]
                    return redirect("homepage")
                else:
                    messages.info(request, "Invalid OTP")
                    return redirect("otp")
            else:
                messages.info(request, "OTP expired")
                return redirect("otp")

        else:
            messages.info(request, "Internal error")
            return render(request, "loginpage")


@login_required(login_url="loginpage")
def homepage(request):
    return render(request, "home.html")
