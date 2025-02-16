from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.LoginPage.as_view(), name="loginpage"),  # login page
    path("registration/", views.Register.as_view(), name="registration"),
    path("OtpView/", views.OtpView.as_view(), name="otp"),
    path("logout/", views.LogoutPage, name="logoutpage"),
    path("home/", views.HomePage.as_view(), name="homepage"),
    path("home/result/", views.voterresult, name="yourvote"),
    path("result", views.candidateresult, name="result"),
    # reset password
     path('reset-password/', views.request_password_reset, name='request_password_reset'),
    path('reset-password/<uuid:token>/', views.reset_password, name='reset_password'),
    
]
