from django.urls import path
from . import views

urlpatterns = [

    # Register
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Login
    path(
        "login/",
        views.login_user,
        name="login"
    ),

    # Logout
    path(
        "logout/",
        views.logout_user,
        name="logout"
    ),

    # Profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # Edit Profile
    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),

    # Change Password
    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),

]