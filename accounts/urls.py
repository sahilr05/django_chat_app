from django.contrib.auth import views as auth_views
from django.urls import include  # NOQA
from django.urls import path

from accounts import views as accounts_views

app_name = "accounts"

urlpatterns = [
    path(
        "login", accounts_views.MyLoginView.as_view(), name="login"
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("signup", accounts_views.signup, name="signup"),
    path("toggle_status", accounts_views.toggle_status, name="toggle_status"),
    path("edit_user/<uuid:pk>/", accounts_views.edit_user, name="edit_user"),
    path("my_account", accounts_views.my_account, name="my_account"),
    path("change_password", accounts_views.change_password, name="change_password"),
    # path("list_interest", accounts_views.list_interest, name="list_interest"),
    path("add_interest", accounts_views.add_interest, name="add_interest"),
    path("delete_interest/<uuid:pk>", accounts_views.delete_interest, name="delete_interest"),
]
