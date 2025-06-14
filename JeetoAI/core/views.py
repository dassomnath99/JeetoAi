from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import *
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail


# Create your views here.
def get_user_data(request):
    if request.user.is_authenticated:
        try:
            return UsersData.objects.get(user=request.user)
        except UsersData.DoesNotExist:
            return None
    return None

def index(request):
    user_data = get_user_data(request)
    return render(request, "core/index.html", {"user_data": user_data})

def games(request):
    user_data = get_user_data(request)
    game_data = GameData.objects.all()  # Get all games
    return render(request, "core/games.html", {"user_data": user_data, "game_data": game_data })

def leaderboard(request):
    user_data = get_user_data(request)
    return render(request, "core/leaderboard.html", {"user_data": user_data})

@login_required(login_url='core:login')
def profile(request, slug):
    user_data = get_object_or_404(UsersData, slug=slug)
    if user_data.user != request.user:
        current_user_data = get_user_data(request)
        if current_user_data:
            return redirect("core:profile", slug=current_user_data.slug)
        return redirect("core:index")

    return render(request, "core/profile.html", {"user_data": user_data})

def faq(request):
    user_data = get_user_data(request)
    return render(request, "core/faq.html", {"user_data": user_data})


def login_view(request, slug=None):
    user_data = None

    if request.user.is_authenticated:
        try:
            user_data = UsersData.objects.get(user=request.user)
            return redirect("core:profile", slug=user_data.slug)
        except UsersData.DoesNotExist:
            pass

    if request.method == "POST":
        formtype = request.POST.get("id")

        if formtype == "login":
            phone = request.POST.get("phone")
            password = request.POST.get("password")
            
            try:
                ud = UsersData.objects.get(phone=phone)
                username = ud.user.username
            except UsersData.DoesNotExist:
                return render(request, "core/login.html", {
                    "error_login": "Invalid credentials"
                })
                
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                user_data = UsersData.objects.get(user=user)
                return redirect("core:profile", slug=user_data.slug)
            else:
                return render(request, "core/login.html", {
                    "error_login": "Invalid credentials"
                })

        elif formtype == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            print("Received signup data:", username, email, phone)

            if password != confirm_password:
                print("Password mismatch!")
                return render(request, "core/login.html", {
                    "password_error": "Passwords do not match"
                })

            if User.objects.filter(email=email).exists():
                print("Email already exists")
                return render(request, "core/login.html", {
                    "Email_error": "Email already registered"
                })

            if User.objects.filter(username=username).exists():
                print("Username already taken")
                return render(request, "core/login.html", {
                    "Username_error": "Username already taken"
                })

            if UsersData.objects.filter(phone=phone).exists():
                print("Phone number already exists")
                return render(request, "core/login.html", {
                    "Phone_error": "Phone number already registered"
                })

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                print("User created:", user)

                user_data = UsersData.objects.create(
                    user=user,
                    phone=phone,
                    slug=slugify(username),
                )
                print("UsersData created:", user_data)

                return redirect("core:profile", slug=user_data.slug)

            except Exception as e:
                print("Error during signup:", e)
                return render(request, "core/login.html", {
                    "signup_error": "Something went wrong during signup"
                })
    return render(request, "core/login.html", {
        "user_data": user_data,
    })
        
def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("core:index")

def terms(request):
    user_data = get_user_data(request)
    return render(request, "core/terms.html", {"user_data": user_data})

def privacy(request):
    user_data = get_user_data(request)
    return render(request, "core/privacy.html", {"user_data": user_data})

def forgot_password(request):
    error = None

    if request.method == "POST":
        step = request.POST.get("step")

        if step == "2":
            # Step 2: Verify OTP
            email = request.POST.get("email")
            otp_input = request.POST.get("otp")

            try:
                user = User.objects.get(email=email)
                otp_records = PasswordResetOTP.objects.filter(user=user).order_by('-created_at')

                if not otp_records.exists():
                    error = "No OTP found. Please request again."
                elif otp_records[0].is_expired():
                    error = "OTP expired. Please request again."
                elif otp_records[0].otp != otp_input:
                    error = "Invalid OTP"
                else:
                    return render(request, "core/forgotpassword.html", {"step": 3, "email": email})

            except User.DoesNotExist:
                error = "Invalid request"

            return render(request, "core/forgotpassword.html", {"step": 2, "error": error, "email": email})

        elif step == "3":
            # Step 3: Reset password
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                error = "Passwords do not match"
            elif len(password1) < 6:
                error = "Password must be at least 6 characters"
            else:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(password1)
                    user.save()
                    PasswordResetOTP.objects.filter(user=user).delete()
                    return redirect("core:login")
                except User.DoesNotExist:
                    error = "User not found"

            return render(request, "core/forgotpassword.html", {"step": 3, "error": error, "email": email})

        else:
            # Step 1: Send OTP
            email = request.POST.get("email")
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                PasswordResetOTP.objects.create(user=user, otp=otp)
                send_mail(
                    subject="Your OTP for Password Reset",
                    message=f"Your OTP is {otp}. It is valid for 5 minutes.",
                    from_email="somnathdas4848@gmail.com",
                    recipient_list=[email],
                )
                return render(request, "core/forgotpassword.html", {"step": 2, "email": email})
            except User.DoesNotExist:
                error = "Email not found"

            return render(request, "core/forgotpassword.html", {"step": 1, "error": error})

    # Default
    return render(request, "core/forgotpassword.html", {"step": 1})

@login_required(login_url='core:login')
def edit_profile(request, slug):
    user_data = get_object_or_404(UsersData, slug=slug)

    if user_data.user != request.user:
        return redirect("core:profile", slug=request.user.usersdata.slug)

    if request.method == "POST":
        phone = request.POST.get("phone")
        profile_picture = request.FILES.get("profile_picture")

        # Update only if provided
        if phone:
            user_data.phone = phone
        if profile_picture:
            user_data.profile_picture = profile_picture

        user_data.save()
        return redirect("core:profile", slug=user_data.slug)

    return render(request, "core/edit_profile.html", {"user_data": user_data})

def promptgeneratorgame(request):
    user_data = get_user_data(request)
    return render(request, "core/promptgeneratorgame.html", {"user_data": user_data})

@login_required(login_url='core:login')
def wallet(request, slug):
    return render(request, "core/wallet.html", {"user_data": get_user_data(request)})

@login_required(login_url='core:login')
def add_funds(request, slug):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        # logic to add amount to user wallet
        messages.success(request, f"${amount} added to your wallet.")
        return redirect('core:wallet', slug=slug)
        
@login_required(login_url='core:login')
def withdraw_funds(request, slug):
    if request.method == 'POST':
        amount = int(request.POST['withdraw_amount'])
        # logic to withdraw amount from user wallet
        messages.success(request, f"${amount} withdrawn from your wallet.")
        return redirect('core:wallet', slug=slug)

def game_details(request, slug):
    game = get_object_or_404(GameData, slug=slug)
    user_data = get_user_data(request)
    if not user_data:
        return redirect("core:login")
    if request.method == "POST":
        if request.POST.get("accept_rules") == "yes":
            # Here you can add logic to mark that the user accepted the rules, e.g., save to DB
            return redirect("core:play_game", slug=game.slug)
    return render(request, "core/game_details.html", {"game": game})
