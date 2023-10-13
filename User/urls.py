from django.urls import path
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView
from User import views

urlpatterns = [
    path("userdash", views.user_dash, name="userdash"),
    path("register", views.sign_up, name="signup"),
    # path("login", views.user_login, name="login"),
    path("profile", login_required(views.profile), name="profile"),
]
# urlpatterns = [
#     # path("new_order", views.new_order, name="order"),
# >>>>>>> main
# ]