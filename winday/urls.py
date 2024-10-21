from django.urls import path
from . import views

app_name = 'winday'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),

    # API routes
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile_connections/<int:profile_id>/", views.profile_connections, name="profile_connections"),
    path("follow/<int:profile_id>/", views.follow_user, name="follow_user"),
    path("find_wind/<str:location>/", views.find_wind, name="find_wind"),
    

]