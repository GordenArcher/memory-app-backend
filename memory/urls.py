from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("register/", views.register),
    path("send_image/", views.send_image),
    path("home_page/", views.home_page),
    path("send_reset_password_mail/", views.send_email),
    path("reset_password/<str:uidb64>/<str:token>/", views.reset_password),
    path("get_user/", views.get_user),
    path("profile_pic/", views.set_profil_pic),
    path("get_profile_pic/", views.get_profilepic),
    path("delete_image/<str:pk>/", views.delete_image),
    path("generate_content/", views.generate_content)
]