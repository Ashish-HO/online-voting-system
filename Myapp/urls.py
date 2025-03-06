from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.LoginPage.as_view(), name="loginpage"),  # login page
    path("registration/", views.Register.as_view(), name="registration"),
    path("OtpView/", views.OtpView.as_view(), name="otp"),
    path("logout/", views.LogoutPage, name="logoutpage"),
    path("home/", views.HomePage.as_view(), name="homepage"),
    path("voterresult/", views.voterresult, name="yourvote"),
    path("result", views.candidateresult, name="result"),
    # reset password
    path(
        "reset-password/", views.request_password_reset, name="request_password_reset"
    ),
    path("reset-password/<uuid:token>/", views.reset_password, name="reset_password"),
    # Admin section
    path("section/", views.AdminSection.as_view(), name="adminsection"),
    # show candidate,post,voter
    path("show_candidate/", views.Candidate.as_view(), name="candidate"),
    path("show_post/", views.Post.as_view(), name="post"),
    path("show_voter/", views.Voter.as_view(), name="voter"),
    # add post ,candidate
    path("AddPost", views.AddPost, name="addpost"),
    path("AddCandidate", views.AddCandidate, name="addcandidate"),
    # edit post , candidate
    path("editpost/<int:id>", views.EditPost, name="editpost"),
    path("editcandidate/<int:id>", views.EditCandidate, name="editcandidate"),
    path("editelection/", views.EditElection, name="editelection"),
    # delete post ,candidate
    path("deletepost/<int:id>", views.DeletePost, name="deletepost"),
    path("deletecandidate/<int:id>", views.DeleteCandidate, name="deletecandidate"),
]
