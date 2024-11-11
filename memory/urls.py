from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("send_image/", views.send_image),
    path("home_page/", views.home_page),
    path("send_reset_password_mail/", views.send_email),
    path("reset_password/<str:uidb64>/<str:token>/", views.reset_password),
    path("get_user/", views.get_user),
    path("profile_pic/", views.set_profil_pic),
]