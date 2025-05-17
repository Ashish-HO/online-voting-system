from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from datetime import datetime

import pyotp
from collections import defaultdict
from json import dumps, loads

from .forms import CreateUserForm, CandidateAddForm, PostAddForm, ElectionForm
from .utils import send_otp
from . import models
from .models import PasswordResetToken

from pprint import pprint


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
                print(errors)
        return render(request, "registration.html", {"errors": form.errors})


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
        email = User.objects.get(username=username).email
        return render(request, "otp.html", {"email": email})

    def post(self, request):
        otp = request.POST.get("otp")
        username = request.session["username"]
        otp_secret = request.session["otp_secret"]
        valid_date = request.session["otp_valid_date"]

        if otp_secret and valid_date is not None:
            valid_until = datetime.fromisoformat(valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret, interval=300)

                if pyotp.TOTP(otp_secret, interval=300).verify(otp):
                    user = User.objects.get(username=username)
                    login(request, user)

                    # del request.session["otp_secret"]
                    # del request.session["otp_valid_date"]
                    return redirect("homepage")
                else:
                    messages.info(request, "Invalid OTP")
            else:
                messages.info(request, "OTP expired")
        else:
            messages.info(request, "Internal error")
            return render(request, "loginpage")
        return render(request, "otp.html")


@method_decorator(login_required(login_url="loginpage"), name="dispatch")
class HomePage(View):

    def get(self, request):
        if request.user.is_staff:
            return redirect("adminsection")
        else:
            voter_id = models.User.objects.get(
                username=request.user
            ).id  # get the id of voter who submit the vote

            election_settings = (
                models.ElectionSetting.objects.all()
            )  # get the election data
            start_date = election_settings.values("startdate")[0][
                "startdate"
            ]  # get the first start date
            end_date = election_settings.values("enddate")[0][
                "enddate"
            ]  # get the end date
            today_date = timezone.now()
            print(start_date, end_date, today_date)

            if (
                start_date <= today_date and today_date <= end_date
            ):  # if voting time is remaining
                if not (
                    get_object_or_404(models.Voter, voter_id=voter_id)
                ).is_voted:  # check if voter has voted or not

                    candidates = models.Candidate.objects.select_related(
                        "post"
                    ).all()  # get queryset
                    data = [
                        {
                            "name": candidate.name,
                            "post": candidate.post.name,
                            "photo": candidate.photo,
                        }
                        for candidate in candidates  # loop through candidates
                    ]
                    # Convert the list into a dictionary grouped by 'post'

                    grouped_candidates = defaultdict(list)
                    for d in data:
                        grouped_candidates[d["post"]].append(
                            {"name": d["name"], "photo": d["photo"]}
                        )
                    grouped_candidates = dict(grouped_candidates)
                    print("_______________________________________________________")
                    print(grouped_candidates)

                    return render(
                        request, "mainpage.html", {"data": dumps(grouped_candidates)}
                    )  #

                else:
                    message = "You have already voted."
                    return render(
                        request,
                        "resultsoon.html",
                        {"message": message, "end_date": end_date},
                    )

            elif start_date > today_date:
                return render(request, "electionsoon.html", {"start_date": start_date})
            else:
                return render(request, "electionend.html")

    @csrf_exempt
    def post(self, request):
        data = request.POST.get("data")
        print(data)
        print("This is post method")
        return render(request, "voterresult.html")


def voterresult(request):
    if request.method == "POST":
        voter_id = models.User.objects.get(
            username=request.user
        ).id  # get the id of voter who submit the vote
        models.Voter.objects.filter(voter_id=voter_id).update(
            is_voted=True
        )  # makes the is_voted to True

        data = loads(request.body)
        print(data)
        votes = data["vote"]
        print("_____________________________________________________")
        print(votes)
        for post, vote_info in votes.items():
            candidate_name = vote_info["name"]

            if candidate_name == "No vote cast":
                continue  # Skip this post

            print(candidate_name)
            candidate = get_object_or_404(models.Candidate, name=candidate_name)
            candidate.votes += 1
            candidate.save()  # save the candidate data after increasing the vote count

    return render(request, "voterresult.html")


def candidateresult(request):
    positions = models.Post.objects.all()
    data = {}

    for position in positions:
        candidates = models.Candidate.objects.filter(post=position)
        data[position.name] = [
            {"name": candidate.name, "photo": candidate.photo, "votes": candidate.votes}
            for candidate in candidates
        ]
    dataJSON = dumps(data)
    return render(request, "candidateresult.html", {"data": dataJSON})


def request_password_reset(request):
    if request.method == "POST":
        username = (request.POST.get("username")).lower()
        try:
            user = User.objects.get(username=username)
            print(user)
            email = user.email  # get email from user
        except User.DoesNotExist:
            return render(
                request,
                "reset/password_reset_form.html",
                {"message": "User doesn't exist"},
            )

        # Create a new reset token
        reset_token = PasswordResetToken.objects.create(
            user=user
        )  # generate token for user

        # Generate reset link
        reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{reset_token.token}/"

        # Email content
        subject = "Reset Your Password"
        message = f"Click the link to reset your password: {reset_url}"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return render(request, "reset/PasswordResetDone.html")  # Show confirmation page

    return render(request, "reset/password_reset_form.html")  # Render email input form


def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return render(request, "reset/invalid_token.html")  # Show invalid token message

    if not reset_token.is_valid():

        return render(request, "reset/expired_token.html")  # Show expired token message

    if request.method == "POST":
        new_password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        user = reset_token.user
        user.password = make_password(new_password)  # Hash password before saving
        user.save()

        reset_token.delete()  # Delete token after successful reset
        return render(
            request, "reset/PasswordResetComplete.html"
        )  # Show success message

    return render(
        request, "reset/PasswordResetConfirm.html"
    )  # Render password input form

@method_decorator(login_required(login_url="loginpage"), name="dispatch")
class AdminSection(View):
    def get(self, request):
        positions = models.Post.objects.all()
        total_candidate = len(models.Candidate.objects.all())
        total_post = len(models.Post.objects.all())
        total_voter = len(models.Voter.objects.all())
        data = {}

        for position in positions:
            candidates = models.Candidate.objects.filter(post=position)
            data[position.name] = [
                {
                    "name": candidate.name,
                    "votes": candidate.votes,
                }
                for candidate in candidates
            ]
        dataJSON = dumps(data)

        return render(
            request,
            "dashboard/dashboard.html",
            {
                "data": dataJSON,
                "total_candidate": total_candidate,
                "total_post": total_post,
                "total_voter": total_voter,
            },
        )


class Candidate(View):
    def get(self, request):
        queryset = models.Candidate.objects.select_related("post").all()
        data = []
        print(queryset[0].post)

        for query in queryset:
            data.append(
                {
                    "id": query.id,
                    "name": query.name,
                    "photo": query.photo,
                    "phone": query.phone,
                    "email": query.email,
                    "post": query.post,
                }
            )

        pprint(data)

        return render(request, "dashboard/candidate_all.html", {"data": data})


class Post(View):
    def get(self, request):
        queryset = models.Post.objects.all()
        data = []
        for query in queryset:
            data.append(
                {"id": query.id, "name": query.name, "description": query.description}
            )
        pprint(data)
        return render(request, "dashboard/post_all.html", {"data": data})


class Voter(View):
    def get(self, request):
        queryset = models.Voter.objects.all()
        data = []
        for query in queryset:
            data.append(
                {
                    "id": query.id,
                    "name": query.voter,
                    "has_voted": query.is_voted,
                    "voted_time": query.voted_time,
                }
            )
        pprint(data)
        return render(request, "dashboard/voter_all.html", {"data": data})


def AddCandidate(request):
    post = models.Post.objects.all()
    post_name = [p.name for p in post]
    if request.method == "GET":
        form = CandidateAddForm()
        return render(
            request, "dashboard/add_candidate.html", {"post": post_name, "form": form}
        )

    if request.method == "POST":
        form = CandidateAddForm(request.POST)
        if form.is_valid():
            form.save()
            message = "candidate added successfully."
            return redirect("candidate")

        error = form.errors
        return render(
            request, "dashboard/add_candidate.html", {"post": post_name, "error": error}
        )


def AddPost(request):
    if request.method == "GET":
        form = PostAddForm()
        return render(request, "dashboard/add_post.html")

    elif request.method == "POST":
        form = PostAddForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Post added successfully."
            return redirect("post")

        error = form.errors
        return render(request, "dashboard/add_post.html", {"error": error})


def EditCandidate(request, id):
    candidate = get_object_or_404(models.Candidate, id=id)
    if request.method == "GET":
        form = CandidateAddForm(instance=candidate)
        return render(request, "dashboard/edit_candidate.html", {"form": form})

    elif request.method == "POST":
        form = CandidateAddForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            message = "candidate updated successfully."
            return redirect("candidate")
        error = form.errors
        return render(
            request, "dashboard/edit_candidate.html", {"form": form, "error": error}
        )


def EditPost(request, id):
    post = get_object_or_404(models.Post, id=id)
    print(post.name)
    print(post.description)

    if request.method == "GET":
        form = PostAddForm(instance=post)
        return render(request, "dashboard/edit_post.html", {"form": form})

    elif request.method == "POST":
        form = PostAddForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            message = "Post updated successfully."
            return redirect("post")

        error = form.errors
        return render(request, "dashboard/edit_post.html", {"error": error})


def EditElection(request):
    election_data = models.ElectionSetting.objects.all().first()
    if request.method == "GET":
        form = ElectionForm(instance=election_data)
        return render(request, "dashboard/edit_election.html", {"form": form})

    elif request.method == "POST":
        form = ElectionForm(request.POST, instance=election_data)
        if form.is_valid():
            form.save()
            message = "Election data updated successfully."
            return redirect("adminsection")
        pass


def DeletePost(request, id):
    post = get_object_or_404(models.Post, id=id)
    post.delete()
    message = "Post deleted successfully."
    return redirect("post")


def DeleteCandidate(request, id):
    candidate = get_object_or_404(models.Candidate, id=id)
    candidate.delete()
    message = "candidate deleted successfully."
    return redirect("candidate")


def resultsoon(request):
    election_settings = models.ElectionSetting.objects.all()
    end_date = election_settings.values("enddate")[0]["enddate"]
    return render(request, "resultsoon.html", {"end_date": end_date})
