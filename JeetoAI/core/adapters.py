from django.shortcuts import resolve_url
from django.utils.text import slugify
from allauth.account.adapter import DefaultAccountAdapter
from .models import UsersData  # Adjust path if needed

class JeetoAIAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        
        # Create corresponding UsersData if not exists
        if not hasattr(user, 'usersdata'):
            slug = slugify(user.username)
            # Ensure uniqueness
            base_slug = slug
            counter = 1
            while UsersData.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            UsersData.objects.create(user=user, slug=slug)
        return user
    def get_login_redirect_url(self, request):
        # Ensure UsersData exists for the user (in case not created yet)
        user = request.user
        if user.is_authenticated:
            user_data = getattr(user, 'usersdata', None)
            if not user_data:
                slug = slugify(user.username)
                base_slug = slug
                counter = 1
                while UsersData.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                user_data = UsersData.objects.create(user=user, slug=slug)
            return resolve_url('core:profile', slug=user_data.slug)
        return resolve_url('core:index')

    def get_signup_redirect_url(self, request):
        return self.get_login_redirect_url(request)

    def get_logout_redirect_url(self, request):
        return resolve_url('core:index')

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        
        # Create corresponding UsersData if not exists
        if not hasattr(user, 'usersdata'):
            slug = slugify(user.username)
            # Ensure uniqueness
            base_slug = slug
            counter = 1
            while UsersData.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            UsersData.objects.create(user=user, slug=slug)
        return user