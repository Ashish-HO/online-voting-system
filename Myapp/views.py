from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from datetime import datetime
import pyotp
from json import dumps, loads

from .forms import CreateUserForm
from .utils import send_otp

# vote form
from . import models


def showvote(request):
    return render(request, "showvote.html")


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


class OtpView(View):

    def get(self, request):
        username = request.session["username"]
        email = models.User.objects.get(username=username).email
        return render(request, "otp.html", {"email": email})

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
                totp = pyotp.TOTP(otp_secret, interval=300)

                if pyotp.TOTP(otp_secret, interval=300).verify(otp):
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


# @method_decorator(login_required(login_url="loginpage"), name="dispatch")
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

    @csrf_exempt
    def post(self, request):
        data = request.POST.get("data")
        print(data)
        print("This is post method")
        return render(request, "result.html")


def result(request):
    if request.method == "POST":
        data = loads(request.body)
        print("______________________________________________________")
        votes = data["votes"]
        print(votes)
        print("______________________________________________________")

        for v in votes:
            post = v
            candidate_name = votes[post]["name"]
            candidate = models.Candidate.objects.get(name=candidate_name)
            candidate.votes += 1
            candidate.save()
            print(f"{post} {candidate_name}", end="/n")

    return render(request, "result.html")


"""
class CandidateAdd(View):

    def get(self, request):
        data = models.Candidate.objects.all()
        return render(request, "Addcandidate.html", {"data": data})

    def post(self, request):
        form = CandidateAddForm(request.POST)

        if form.is_valid():
            form.save()
            message = "Candidated added successfully."
            return render(request, "Addcandidate.html", {"message": message})
        else:
            error = form.errors
            return render(request, "Addcandidate.html", {"error": error})

    def delete(self, request, candidate_id):
        candidate = get_object_or_404(models.Candidate, id=candidate_id)
        candidate.delete()
        message = f"{post_id} successfully deleted."
        return render(request, "Addcandidate.html", {"message": message})

    def patch(self,request,candidate_id):
        post=get_object_or_404(models.Candidate,id=candidate_id)
        form=CandidateAddForm(request.POST,instance=post)

        if form.is_valid():
            form.save()
            message="Update successfully."
            return render(request,"Addcandidate.html",{"message":message})
        return render(request,"Addcandidate.html",{"error":form.errors})



class PostAdd(View):

    def get(self, request): #read method
        data = models.Post.objects.all() #get all the objects of post
        return render(request, "Addpost.html", {"data": data})

    def post(self, request): # Create method
        form = PostAddForm(request.POST) #get entered data 

        if form.is_valid():
            form.save() #data saved to database
            message = "Post added successfully."
            return render(request, "Addpost.html", {"message": message})
        else:
            error = form.errors
            return render(request, "Addpost.html", {"error": error})

    def delete(self, request, post_id): #delete method 
        post = get_object_or_404(models.Post, id=post_id) #get specific post to delete
        post.delete()
        message = f"{post_id} successfully deleted."
        return render(request, "Addpost.html", {"message": message})

    def patch(self,request,post_id): #update specific post
        post=get_object_or_404(models.Post,id=post_id) 
        form=PostAddForm(request.POST,instance=post) #update post with new data

        if form.is_valid():
            form.save()
            message="Update successfully."
            return render(request,"Addpost.html",{"message":message})
        return render(request,"Addpost.html",{"error":form.errors})
"""
