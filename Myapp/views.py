from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View


from .forms import CreateUserForm


# Create your views here.
class register(View):
    form = CreateUserForm()
    errors = {}

    def get(self, request):
        return render(request, "registration.html", self.errors)

    def post(self, request):
        form = CreateUserForm(request.POST)  # Fill form with data from request
        email = request.POST.get("email")
        try:
            user_exists = User.objects.get(
                username=request.POST["username"]
            )  # check if user is already registered or not
            messages.info(request, "User already registered.")
            return redirect("loginpage")
        except:

            if form.is_valid():
                form.save()
                messages.info(request, "User Created Successfully!!")
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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("otp")
        else:
            messages.info(request, "Incorrect Credentials.")

        return render(request, "login.html")


def otp(request):
    return render(request, "otp.html")


@login_required(login_url="loginpage")
def logoutpage(request):
    logout(request)
    return render(request, "logout.html")
