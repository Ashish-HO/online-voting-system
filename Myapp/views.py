from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import pyotp
from json import dumps

from .forms import CreateUserForm
from .utils import send_otp

# vote form
from . import models


# Create your views here.
@login_required(login_url="loginpage")
def LogoutPage(request):
    logout(request)
    return redirect("loginpage")


class Register(View):
    form = CreateUserForm()
    errors = {}

    def get(self, request):
        return render(request, "registration.html", self.errors)

    def post(self, request):
        username = request.POST.get("username").lower()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = username.lower() + "@wrc.edu.np"

        info = {
            "username": username,
            "email": email,
            "password1": password1,
            "password2": password2,
        }
        form = CreateUserForm(info)
        try:
            username_exists = User.objects.get(
                username=request.POST["username"].lower()
            )
            messages.info(request, "User already registered.")
            return redirect("loginpage")
        except:
            if form.is_valid():
                user = form.save()
                voter = models.Voter(voter=user)
                voter.save()
                return redirect("loginpage")
            else:
                errors = {"errors": form.errors}  # FORM IS INVALID
        return render(
            request, "registration.html", self.errors
        )  # SHOW REGISTRATION PAGE WITH ERRORS


class LoginPage(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # SEND OTP TO USER....
            email = user.email
            send_otp(request, email)
            request.session["username"] = username
            return redirect("otp")
        else:
            messages.info(request, "Incorrect Credentials.")
        return redirect("loginpage")


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
            else:
                messages.info(request, "OTP expired")
        else:
            messages.info(request, "Internal error")
            return render(request, "loginpage")
        return render(request, "otp.html")


class HomePage(View):

    def get(self, request):
        president = models.Candidate.objects.filter(post__name="President").all()
        vice_president = models.Candidate.objects.filter(
            post__name="Vice President"
        ).all()
        treasurer = models.Candidate.objects.filter(post__name="Treasurer").all()
        secretary = models.Candidate.objects.filter(post__name="Secretary").all()
        joint_secretary = models.Candidate.objects.filter(
            post__name="Joint Secretary"
        ).all()
        member = models.Candidate.objects.filter(post__name="Member").all()

        president_data = [{"name": p.name, "photo": p.photo} for p in president]
        vice_president_data = [
            {"name": vp.name, "photo": vp.photo} for vp in vice_president
        ]

        treasurer_data = [{"name": t.name, "photo": t.photo} for t in treasurer]
        secretarydata = [{"name": s.name, "photo": s.photo} for s in secretary]
        joint_secretarydata = [
            {"name": js.name, "photo": js.photo} for js in joint_secretary
        ]
        member_data = [{"name": m.name, "photo": m.photo} for m in member]

        data = {
            "president": president_data,
            "vice_president": vice_president_data,
            "treasurer": treasurer_data,
            "secretary": secretarydata,
            "joint_secretary": joint_secretarydata,
            "member": member_data,
        }

        dataJSON = dumps(data)
        print(dataJSON)
        return render(request, "mainpage.html", {"data": dataJSON})

    # @csrf_exempt
    def post(self, request):
        print("This is post method")
