from django.urls import path
from . import views, views

urlpatterns = [
    path("", views.LoginUser.as_view(), name="loginpage"),
    path("registration/", views.register.as_view(), name="registration"),
    path("otp/", views.otp.as_view(), name="otp"),
    path("home/", views.homepage, name="homepage"),
    path("logout/", views.logoutpage, name="logoutpage"),
]
