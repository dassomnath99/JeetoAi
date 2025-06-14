from allauth.socialaccount.signals import social_account_updated
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.shortcuts import redirect
from django.urls import reverse
from core.models import UsersData

@receiver(user_logged_in)
def handle_social_login(request, user, **kwargs):
    print("User logged in:", user)
    print("Social account added:", sociallogin.account)
@receiver(social_account_added)
def social_account_added(request, sociallogin, **kwargs):
    user = sociallogin.user
    extra_data = sociallogin.account.extra_data