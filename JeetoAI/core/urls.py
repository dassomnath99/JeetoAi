from django.contrib import admin
from django.urls import path
from . import views
app_name = "core"
    
urlpatterns = [
    path("", views.index, name="index"),
    path("games/", views.games, name="games"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("profile/<slug:slug>/", views.profile, name="profile"),
    path("faq/", views.faq, name="faq"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("terms-and-conditions/", views.terms, name="terms"),
    path("privacy-policy/", views.privacy, name="privacy"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("profile/<slug:slug>/edit/", views.edit_profile, name="edit_profile"),
    path("games/<slug:slug>/", views.game_details, name="game_details"),
    path("games/game_details/<slug:slug>/", views.game_details, name="game_details"),
    path("profile/<slug:slug>/wallet/", views.wallet, name="wallet"),
    path("profile/<slug:slug>/wallet/withdraw/", views.withdraw_funds, name="withdraw_funds"),
    path("profile/<slug:slug>/wallet/deposit/", views.add_funds, name="add_funds"),

]
