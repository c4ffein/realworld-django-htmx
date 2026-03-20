from articles.models import Article
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import LoginForm, RegisterForm, SettingsForm
from helpers.htmx import is_htmx

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("home")
            form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        email=form.cleaned_data["email"],
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password"],
                    )
                login(request, user)
                return redirect("home")
            except IntegrityError as err:
                err_str = str(err).lower()
                if "email" in err_str:
                    form.add_error("email", "This email has already been taken.")
                elif "username" in err_str:
                    form.add_error("username", "This username has already been taken.")
                else:
                    form.add_error(None, "Registration failed.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def settings_view(request):
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            if password:
                login(request, user)
            request.session.pop("jwt_token", None)  # clear stale JWT so context processor regenerates
            return redirect("profile", username=user.username)
    else:
        form = SettingsForm(instance=request.user)
    return render(request, "accounts/settings.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def profile_view(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "accounts/profile_404.html", {"username": username}, status=404)
    is_self = request.user == profile_user
    is_following = request.user.is_authenticated and request.user.is_following(profile_user)
    articles = Article.objects.with_favorites(request.user).filter(author=profile_user).order_by("-created")
    return render(
        request,
        "accounts/profile.html",
        {
            "profile_user": profile_user,
            "is_self": is_self,
            "is_following": is_following,
            "articles": articles,
            "tab": "my",
        },
    )


def profile_favorites_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_self = request.user == profile_user
    is_following = request.user.is_authenticated and request.user.is_following(profile_user)
    articles = Article.objects.with_favorites(request.user).filter(favorites=profile_user).order_by("-created")
    return render(
        request,
        "accounts/profile.html",
        {
            "profile_user": profile_user,
            "is_self": is_self,
            "is_following": is_following,
            "articles": articles,
            "tab": "favorites",
        },
    )


@login_required
def follow_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    if profile_user != request.user:
        if profile_user.followers.filter(pk=request.user.id).exists():
            profile_user.followers.remove(request.user)
        else:
            profile_user.followers.add(request.user)
    is_following = profile_user.followers.filter(pk=request.user.id).exists()
    if is_htmx(request):
        return render(
            request,
            "partials/follow_button.html",
            {
                "profile_user": profile_user,
                "is_following": is_following,
            },
        )
    return redirect("profile", username=username)
