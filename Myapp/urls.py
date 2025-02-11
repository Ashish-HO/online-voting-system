from django.urls import path

from . import views

urlpatterns = [
    path("", views.LoginPage.as_view(), name="loginpage"),  # login page
    path("registration/", views.Register.as_view(), name="registration"),
    path("OtpView/", views.OtpView.as_view(), name="otp"),
    path("logout/", views.LogoutPage, name="logoutpage"),
    path("home/", views.HomePage.as_view(), name="homepage"),
    path("home/result/", views.result, name="yourvote"),
]
