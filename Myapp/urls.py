from django.urls import path
from . import views, views

urlpatterns = [
    path("", views.LoginUser.as_view(), name="loginpage"),
    path("otp/", views.otp, name="otp"),
    path("registration/", views.register.as_view(), name="registration"),
    path("logout/", views.logoutpage, name="logoutpage"),
]
